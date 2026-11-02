"""Equivalent circuit models and the residual functions used for fitting impedance spectra."""

import numpy as np
import pandas as pd


def Restructure_Dataframe_By_Frequency(list_of_dataframes, x_values_column_name, y_values_column_name, z_values_column_name, list_RateTest_labels):
    """Puts Re and -Im of every frequency and rate into one row ('Real / Ohm at Frequency <f> Hz and Rate <r> C', '-Imag / Ohm at ...').
    list_of_dataframes, x/y/z_values_column_name = Re, -Im and frequency column, list_RateTest_labels = rate per dataframe. Returns the one-row dataframe."""
    # Defining of a Dataframe for all Frequencies just changed structure
    dictionary_of_all_frequencies = {} # the values are collected first and put in the dataframe at once (adding the columns one by one fragments the dataframe)
    
    for i in range(0, len(list_of_dataframes)):
        # x values
        X = list_of_dataframes[i][x_values_column_name]

        # y values
        Y = list_of_dataframes[i][y_values_column_name]
        
        # Z value
        Z = list_of_dataframes[i][z_values_column_name]

        list_of_selected_frequencies = [x for x in range(len(list_of_dataframes[i]))]

        for n in list_of_selected_frequencies:
            frequency = Z.iloc[n]
            frequency = round(frequency, 3)
            resistance_real = X.iloc[n]
            resistance_imag = Y.iloc[n]
            rate = list_RateTest_labels[i]
    
            dictionary_of_all_frequencies['Real / Ohm at Frequency %s Hz and Rate %s C' %(frequency, rate)] = resistance_real
            dictionary_of_all_frequencies['-Imag / Ohm at Frequency %s Hz and Rate %s C' %(frequency, rate)] = resistance_imag

        data = pd.DataFrame(dictionary_of_all_frequencies, index=[0])
        
    return data


def Impedance_RQ_Element(omega, R, Q, n):
    """Impedance of one R||Q element (resistor parallel to a constant phase element).
    omega = angular frequency 2*pi*f, R in Ohm, Q in F s^(n-1), n = 0..1. Returns the complex Z in Ohm."""
    return ((R)/(1+np.power((1j*omega), n)*Q*R))


def Impedance_RC_Element(omega, R, C):
    """Impedance of one R||C element. omega = 2*pi*f, R in Ohm, C in F. Returns the complex Z in Ohm."""
    return ((R)/(1+1j*omega*C*R))


def Impedance_CPE_Element(omega, Q, n):
    """Impedance of a constant phase element (CPE). omega = 2*pi*f, Q in F s^(n-1), n = 0..1. Returns the complex Z in Ohm."""
    return (1)/(np.power((1j*omega), n)*Q)


def Calculate_Impedance_RQ_Model(f, ModelValues, PhaseAngle=True):
    """Impedance of 1, 2 or 3 R||Q elements in series, optionally + CPE.
    f = frequencies in Hz; ModelValues = [R1, Q1, n1, ...] with 3, 6 or 9 values, or 11 values (+ Q4, n4 of the CPE); R in Ohm, Q in F s^(n-1), n = 0..1.
    Returns the phase angle in degree (PhaseAngle=True) or the complex impedance Z in Ohm (PhaseAngle=False)."""
    if len(ModelValues) not in (3, 6, 9, 11): # RQ, RQ-RQ, RQ-RQ-RQ or RQ-RQ-RQ-CPE model
        return None

    omega = 2*np.pi*f
    # the R||Q elements in series: every three values are R, Q and n of one element
    Z = Impedance_RQ_Element(omega, ModelValues[0], ModelValues[1], ModelValues[2])
    for k in range(3, min(len(ModelValues), 9), 3):
        Z = Z + Impedance_RQ_Element(omega, ModelValues[k], ModelValues[k+1], ModelValues[k+2])
    # 11 values: the last two are Q4 and n4 of the CPE
    if len(ModelValues) == 11:
        Z = Z + Impedance_CPE_Element(omega, ModelValues[9], ModelValues[10])

    if PhaseAngle is True: # If "PhaseAngle=True" is given, the phase angle is returned instead of the impedance Z
        phase = np.arctan(Z.imag/Z.real)
        phaseangle = np.rad2deg(phase)
        return phaseangle

    return Z


def Calculate_Impedance_RC_Model(f, ModelValues, PhaseAngle=True):
    """Impedance of 1, 2 or 3 R||C elements in series, optionally + CPE.
    f = frequencies in Hz; ModelValues = [R1, C1, ...] with 2, 4 or 6 values, or 8 values (+ Q1, n1 of the CPE); R in Ohm, C in F.
    Returns the phase angle in degree (PhaseAngle=True) or the complex impedance Z in Ohm."""
    if len(ModelValues) not in (2, 4, 6, 8): # RC, RC-RC, RC-RC-RC or RC-RC-RC-CPE model
        return None

    omega = 2*np.pi*f
    # the R||C elements in series: every two values are R and C of one element
    Z = Impedance_RC_Element(omega, ModelValues[0], ModelValues[1])
    for k in range(2, min(len(ModelValues), 6), 2):
        Z = Z + Impedance_RC_Element(omega, ModelValues[k], ModelValues[k+1])
    # 8 values: the last two are Q1 and n1 of the CPE
    if len(ModelValues) == 8:
        Z = Z + Impedance_CPE_Element(omega, ModelValues[6], ModelValues[7])

    if PhaseAngle is True: # If "PhaseAngle=True" is given, the phase angle is returned instead of the impedance Z
        phase = np.arctan(Z.imag/Z.real)
        phaseangle = np.rad2deg(phase)
        return phaseangle

    return Z


def Fit_Z_Real_Imag_RQRQRQCPE(pars, f, Z_real_imag_measurement=None):
    """Residual function for lmfit: RQ-RQ-RQ-CPE model minus measurement, real and imaginary parts one after the other.
    pars = lmfit Parameters R1, Q1, n1, ..., Q4, n4; f in Hz; Z_real_imag_measurement = np.append(Z.real, Z.imag) (None -> the complex model Z is returned)."""
    # The values of the entries "R1", "Q1", ... in the dictionary pars are used as model values
    ModelValues = [pars[name].value for name in ['R1', 'Q1', 'n1', 'R2', 'Q2', 'n2', 'R3', 'Q3', 'n3', 'Q4', 'n4']]
    Z = Calculate_Impedance_RQ_Model(f, ModelValues, PhaseAngle=False)
    Z_real_imag_model = np.append(Z.real, Z.imag)

    if Z_real_imag_measurement is None:     # If Z_real_imag_measurement=None is set, the model data is returned instead of the residuals
        return Z

    return Z_real_imag_model - Z_real_imag_measurement


def Fit_Z_Real_Imag_Phase_RQRQRQCPE(pars, f, Z_real_imag_phaseangle_measurement=None):
    """Like Fit_Z_Real_Imag_RQRQRQCPE, but the phase angle (degree) is fitted as well: measurement = concatenate([Z.real, Z.imag, phase angle])."""
    # The values of the entries "R1", "Q1", ... in the dictionary pars are used as model values
    ModelValues = [pars[name].value for name in ['R1', 'Q1', 'n1', 'R2', 'Q2', 'n2', 'R3', 'Q3', 'n3', 'Q4', 'n4']]
    Z = Calculate_Impedance_RQ_Model(f, ModelValues, PhaseAngle=False)
    phase = np.arctan(Z.imag/Z.real)
    phaseangle = np.rad2deg(phase)

    Z_real_imag_phaseangle_model = np.concatenate([Z.real, Z.imag, phaseangle])

    if Z_real_imag_phaseangle_measurement is None:     # If Z_real_imag_measurement=None is set, the model data is returned instead of the residuals
        return Z

    return Z_real_imag_phaseangle_model - Z_real_imag_phaseangle_measurement


def Fit_Z_Real_Imag_RCRCRCCPE(pars, f, Z_real_imag_measurement=None):
    """Like Fit_Z_Real_Imag_RQRQRQCPE for the RC-RC-RC-CPE model (pars R1, C1, R2, C2, R3, C3, Q1, n1)."""
    # The values of the entries "R1", "C1", ... in the dictionary pars are used as model values
    ModelValues = [pars[name].value for name in ['R1', 'C1', 'R2', 'C2', 'R3', 'C3', 'Q1', 'n1']]
    Z = Calculate_Impedance_RC_Model(f, ModelValues, PhaseAngle=False)
    Z_real_imag_model = np.append(Z.real, Z.imag)

    if Z_real_imag_measurement is None:     # If Z_real_imag_measurement=None is set, the model data is returned instead of the residuals
        return Z

    return Z_real_imag_model - Z_real_imag_measurement
