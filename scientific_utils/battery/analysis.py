"""Evaluation of cycling and rate test data: steps, capacities, potential drops, dQ/dV peaks."""

from numpy import diff
from scipy.interpolate import interp1d
import matplotlib as mpl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.signal

from scientific_utils.general.analysis import Round_Down_To_Odd
from scientific_utils.general.plotting import my_colormap
from scientific_utils.general.plotting import pgf_with_latex
from scientific_utils.general.plotting import Matplotlib_Legend_Above_And_Save, Matplotlib_New_Figure_With_Frame, Set_Scientific_Tick_Labels


def Resample_Equidistant(list_of_dataframes, x_values_column_name, y_values_column_name):
    """Resamples every curve on equidistant y values (same number of points, from the first to the last y value);
    x (relative to its first value) is linearly interpolated as a function of y.
    list_of_dataframes, x_values_column_name, y_values_column_name = column names (e.g. capacity and potential).
    Returns a list of dataframes with the two columns."""
    # definition of a list for the new equidistant dataframes
    list_of_equidistant_data = []
    
    for i in range(0, len(list_of_dataframes)):
        # defining x and y values
        x = list_of_dataframes[i][x_values_column_name]
        y = list_of_dataframes[i][y_values_column_name]
        
        # calculating the relative x values from the absolute values
        x_relative = list_of_dataframes[i][x_values_column_name] - list_of_dataframes[i].iloc[0][x_values_column_name]
        # reseten of the indices of the dataframe
        x_relative = x_relative.reset_index(drop=True)
        
        # Calculating the number of equidistant points for the y variable
        number_of_points = len(list_of_dataframes[i])
        y_max = list_of_dataframes[i].iloc[-1][y_values_column_name]
        y_min = list_of_dataframes[i].iloc[0][y_values_column_name]
        # calculating the equidistant step size
        y_delta = (y_max - y_min)/number_of_points
        # new numpy array with equidistand y values
        y_new = np.arange(y_min, y_max, y_delta)
        
        # linear interpolation
        linear_interpolation = interp1d(list_of_dataframes[i][y_values_column_name], x_relative, axis=0, fill_value="extrapolate")
        # resample of x with the linear interpolation model
        x_new = linear_interpolation(y_new)
        
        # saving the numpy array with the equidistant data in a dataframe
        data_equidistant = pd.DataFrame({x_values_column_name: x_new, y_values_column_name: y_new}, columns=[x_values_column_name, y_values_column_name])
        # saving the dataframe in a list
        list_of_equidistant_data.append(data_equidistant)
        
    return list_of_equidistant_data


def Derive_Smooth_And_Find_Peaks(list_of_dataframes, x_values_column_name, y_values_column_name, percent_of_points_used_for_smoothing, prominence_min_max_for_peakfind, percent_of_points_used_for_peakfind, positv_or_negativ_peak, dYdX_column_name_new, list_of_labels=None):
    """dY/dX of every curve (e.g. dQ/dV), smoothed with a Savitzky-Golay filter (2nd order), and its peaks.
    list_of_dataframes, x/y_values_column_name = columns; per curve lists: percent_of_points_used_for_smoothing (filter window, ratio 0..1),
    prominence_min_max_for_peakfind (prominence in the unit of dY/dX), percent_of_points_used_for_peakfind (minimum peak width, ratio 0..1);
    positv_or_negativ_peak = 1 (maxima) or -1 (minima), dYdX_column_name_new = name of the derivative column,
    list_of_labels = None -> curves are numbered as cycles, else the rates.
    Returns (list of dataframes with x, dY/dX and 'Savgol-Filter <name>', list of lists of peak dataframes, one dataframe with all peaks)."""
    # Definiton of lists and dataframe, in which the Data of the "DerivationSmoothingPeakfind" function is saved
    # cycles are counted, rates are taken from the list of labels
    if list_of_labels is None:
        label_column = 'Cycle'
    else:
        label_column = 'Rate'

    list_of_dataframes_of_dYdX_and_smoothed_curve = []
    list_of_dataframes_of_dYdX_peak_values = []
    dataframe_of_dYdX_peaks_for_every_cycle = pd.DataFrame(columns=['Peak Savgol-Filter ' + dYdX_column_name_new, 'Peak Savgol-Filter ' + x_values_column_name, label_column])
    
    for i in range(0, len(list_of_dataframes)):
        # defining x and y values
        x = list_of_dataframes[i][x_values_column_name]
        y = list_of_dataframes[i][y_values_column_name]
    
        # Measurement data converted in numpy array
        X = x.to_numpy() 
        Y = y.to_numpy()
    
        # Calculation of the derivation
        dX = diff(X)
        dY = diff(Y)
        with np.errstate(divide='ignore', invalid='ignore'): # repeated voltage values (dX = 0) give inf in raw data, this is why the curves are resampled before (see 04b)
            dYdX = dY/dX
    
        # Shorten of the X-Arrays, because during derivation one point is lost
        X = np.delete(X, -1)
    
        # Points with the same x value give an infinite derivative (only in raw, not equidistant data) -> these points are removed
        finite_points = np.isfinite(dYdX)
        X = X[finite_points]
        dYdX = dYdX[finite_points]
    
        # Calculation of the number of points used for Savitzky Golay Filter
        number_of_points_for_smoothing = int(Round_Down_To_Odd(len(dYdX) * percent_of_points_used_for_smoothing[i]))
        # Calculation of the Smoothed data with the Savitzky Golay Filter and a Polynomial of second order
        dYdX_savgol = scipy.signal.savgol_filter(dYdX, number_of_points_for_smoothing, 2)
    
        # Calculation of the number of points used for the Peak extract function
        number_of_points_for_peakfind = int(len(dYdX_savgol) * percent_of_points_used_for_peakfind[i])
        
        # Peak extract from the smoothed data
        dYdX_peak = scipy.signal.find_peaks((positv_or_negativ_peak)*dYdX_savgol,                            # Returns the indices of the minimum values, that is why there is a "-" in front of the data name
                                         #height = 15,                              # minimum height a peak must have
                                         #threshold = None,                         # Required threshold of peaks, the vertical distance to its neighbouring samples
                                         #distance=0.2,                             # number of data points a peak must contain
                                         prominence=prominence_min_max_for_peakfind[i],
                                         width=number_of_points_for_peakfind
                                        ) 
        
        
        # Peak extract from the smoothed data
        #dYdX_peak = scipy.signal.find_peaks((positv_or_negativ_peak)*dYdX_savgol,                            # returns the indices of the minimum values, that is why there is a "-" in front of the data name
        #                                 #height = 15,                              # minimum height a peak must have
         #                                #threshold = None,                         # Required threshold of peaks, the vertical distance to its neighbouring samples
        #                                 #distance=0.2,                             # number of data points a peak must contain
        #                                 prominence=(0.0005, 8.0),
         #                                width=number_of_points_for_peak_find
         #                               ) 
    
        # Convert the array in a float64
        dYdX_peak = dYdX_peak[0]                                                    
    
        # if no peak is found the peak data is set to "Nan"
        if len(dYdX_peak) == 0:                                                      
            peak_Y = np.nan
            peak_X = np.nan
        else:
            peak_Y = dYdX_savgol[dYdX_peak]                                             # Returns the y values for the indices
            peak_X = X[dYdX_peak]                                                       # Returns the x values for the indices
    
        # defining new empty arrays for saving the peak values
        dYdX_peaks = np.empty([1,0])
        X_peaks = np.empty([1,0])
        cycle = np.empty([1,0])
    
        # saving the peak values in a pre defined array
        dYdX_peaks = np.append(dYdX_peaks, peak_Y)
        X_peaks = np.append(X_peaks, peak_X)
        if list_of_labels is None:
            cycle = np.append(cycle, (i+1))
        else:
            cycle = np.append(cycle, list_of_labels[i])
        
        # saving all derivativ curves in a dataframe
        dYdX_smoothed = pd.DataFrame({x_values_column_name: X, dYdX_column_name_new: dYdX, 'Savgol-Filter '+ dYdX_column_name_new : dYdX_savgol}, columns=[x_values_column_name, dYdX_column_name_new, 'Savgol-Filter ' + dYdX_column_name_new])
        list_of_dataframes_of_dYdX_and_smoothed_curve.append(dYdX_smoothed)
        
        # Saving the extracted peak values from the smoothed function in a datatframe
        dYdX_peaks_list = [[] for i in range(0, (len(dYdX_peaks)))] # empty list of lists for the extracted peaks
        dataframe_of_dYdX_peaks_for_one_cycle = pd.DataFrame(columns=['Peak Savgol-Filter ' + dYdX_column_name_new, 'Peak Savgol-Filter ' + x_values_column_name, label_column])
        for i in range(0, (len(dYdX_peaks))): # length of the array for checking how many peaks are extracted
            length = len(dYdX_peaks)
            splitted_dYdX_peaks = np.split(dYdX_peaks, length)[i] # splitting the array in subarrays. The amount of subarrays is equal to the amount of extracted peaks
            splitted_X_peaks = np.split(X_peaks, length)[i]
            dYdX_peaks_list[i] = pd.DataFrame({'Peak Savgol-Filter ' + dYdX_column_name_new : splitted_dYdX_peaks, 'Peak Savgol-Filter ' + x_values_column_name: splitted_X_peaks, label_column : cycle}, columns=['Peak Savgol-Filter ' + dYdX_column_name_new, 'Peak Savgol-Filter ' + x_values_column_name, label_column]) # saving every extracted peak in a seperate dataframe. All dataframes in one lsit
            
        for i in range(0, len(dYdX_peaks)): # list of dataframes contacting to one dataframe with all peak values
            dataframe_of_dYdX_peaks_for_one_cycle = pd.concat([dataframe_of_dYdX_peaks_for_one_cycle, dYdX_peaks_list[i]], ignore_index=True, sort=False)
            
        # Saving the extracted peaks in a list of lists
        list_of_dataframes_of_dYdX_peak_values.append(dYdX_peaks_list)
        #saving all extracted peaks in one dataframe
        dataframe_of_dYdX_peaks_for_every_cycle = pd.concat([dataframe_of_dYdX_peaks_for_every_cycle, dataframe_of_dYdX_peaks_for_one_cycle], ignore_index=True, sort=False)

    #print(dataframe_of_dYdX_peaks_for_one_rate)
    #print(list_of_dataframes_of_dYdX_peak_values)
    #print(dataframe_of_dYdX_peaks_for_every_rate)
        
    return list_of_dataframes_of_dYdX_and_smoothed_curve , list_of_dataframes_of_dYdX_peak_values , dataframe_of_dYdX_peaks_for_every_cycle


def Extract_Charge_Discharge_Capacities(list_of_dataframes_charging_steps, values_column_name_charge, list_of_dataframes_discharging_steps, values_column_name_discharge, list_of_labels=None, active_mass_g=(12*0.7)/1000):
    """Charge and discharge capacity of every step (last minus first value) in mAh and in mAh/g.
    mAh/g uses the active material mass active_mass_g in g (default (12*0.7)/1000 g = 8.4 mg, the cells of this repository).
    list_of_dataframes_charging/discharging_steps, values_column_name_charge/discharge = capacity column;
    list_of_labels = None -> 'Cycle' 1, 2, ..., else 'Rate / C'. Returns one dataframe."""
    # defining new dataframe for the extracted values
    dataframes_of_charge_discharge_capacities_per_cycle = pd.DataFrame()
    # extract the values from charging cycles
    for i in range(0, len(list_of_dataframes_charging_steps)):
        charge_capacity = list_of_dataframes_charging_steps[i].iloc[-1][values_column_name_charge] - list_of_dataframes_charging_steps[i].iloc[0][values_column_name_charge]
        dataframes_of_charge_discharge_capacities_per_cycle.loc[i, 'Charge Capacity / mAh'] = charge_capacity
        if list_of_labels is None:
            dataframes_of_charge_discharge_capacities_per_cycle.loc[i, 'Cycle'] = (i+1)
        else:
            dataframes_of_charge_discharge_capacities_per_cycle.loc[i, 'Rate / C'] = list_of_labels[i]
    # extract the values from discharging cycles
    for i in range(0, len(list_of_dataframes_discharging_steps)):
        discharge_capacity = list_of_dataframes_discharging_steps[i].iloc[-1][values_column_name_discharge] - list_of_dataframes_discharging_steps[i].iloc[0][values_column_name_discharge]
        dataframes_of_charge_discharge_capacities_per_cycle.loc[i, 'Discharge Capacity / mAh'] = discharge_capacity
    
    dataframes_of_charge_discharge_capacities_per_cycle['Charge Capacity / mAh/g'] = (dataframes_of_charge_discharge_capacities_per_cycle['Charge Capacity / mAh']/active_mass_g)
    dataframes_of_charge_discharge_capacities_per_cycle['Discharge Capacity / mAh/g'] = (dataframes_of_charge_discharge_capacities_per_cycle['Discharge Capacity / mAh']/active_mass_g)
    
    return dataframes_of_charge_discharge_capacities_per_cycle


def Extract_Potential_Drop_Applied_Current(list_of_dataframes_charging_cycles, column_names_charging, list_of_dataframes_discharging_cycles, column_names_discharging, list_of_dataframes_OCV_after_charging, column_names_ocv_charging, list_of_dataframes_OCV_after_discharging, column_names_ocv_discharging, list_of_labels=None):
    """Potential drop in V between the end of every CP step and the start of the following OCV step (charge and discharge).
    The cycling evaluation (list_of_labels = None) leaves out the last charging step; the rate test uses every rate.
    Inputs: the lists of CP and OCV step dataframes and their potential column names.
    Returns a dataframe with 'DeltaV CP charge to OCV', 'DeltaV CP discharge to OCV' and 'Cycle' or 'Rate / C'."""
    #defining new empty dataframe for the extracted values
    dataframes_of_potential_drop_between_CP_and_OCV_per_cycle = pd.DataFrame()
    ### Ladekurven -> OCV
    # the cycling evaluation leaves out the last cycle, the rate test uses every rate (as in the original notebooks)
    if list_of_labels is None:
        number_of_charging_steps = len(list_of_dataframes_charging_cycles)-1
    else:
        number_of_charging_steps = len(list_of_dataframes_charging_cycles)
    for i in range(0, number_of_charging_steps):
        #print(list_of_dataframes_of_CP_charge_equidistant_cycling[i].iloc[-1]['<Ewe>/V'])
        #print(list_of_dataframes_OCV_after_CP_step_charge_cycling[i].iloc[0]['Voltage (V)'])
        #print(i)
        dataframes_of_potential_drop_between_CP_and_OCV_per_cycle.loc[i, 'DeltaV CP charge to OCV'] = list_of_dataframes_charging_cycles[i].iloc[-1][column_names_charging]-list_of_dataframes_OCV_after_charging[i].iloc[0][column_names_ocv_charging] # A new value is saved in the dataframe by index and column name. If the index and column already exist, the value is replaced, otherwise a new column is created

    ### Entladekurven -> OCV
    for i in range(0, len(list_of_dataframes_discharging_cycles)):
        dataframes_of_potential_drop_between_CP_and_OCV_per_cycle.loc[i, 'DeltaV CP discharge to OCV'] = list_of_dataframes_discharging_cycles[i].iloc[-1][column_names_discharging]-list_of_dataframes_OCV_after_discharging[i].iloc[0][column_names_ocv_discharging] # A new value is saved in the dataframe by index and column name. If the index and column already exist, the value is replaced, otherwise a new column is created
        if list_of_labels is None:
            dataframes_of_potential_drop_between_CP_and_OCV_per_cycle.loc[i, 'Cycle'] = (i+1)
        else:
            dataframes_of_potential_drop_between_CP_and_OCV_per_cycle.loc[i, 'Rate / C'] = list_of_labels[i]
    
    return dataframes_of_potential_drop_between_CP_and_OCV_per_cycle


def Extract_Potential_Drop_During_OCV(list_of_dataframes_OCV_after_charge, column_names_ocv_charging,list_of_dataframes_OCV_after_discharge, column_names_ocv_discharging, list_of_labels=None):
    """Potential at the start and at the end of every OCV step and their difference (in V), after charging and after discharging.
    Inputs: lists of OCV step dataframes and their potential column names; list_of_labels = None -> 'Cycle', else 'Rate / C'.
    Returns one dataframe."""
    dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle = pd.DataFrame()
    for i in range(0, len(list_of_dataframes_OCV_after_charge)):
        #print(list_of_dataframes_of_CP_charge_equidistant_cycling[i].iloc[-1]['<Ewe>/V'])
        #print(list_of_dataframes_OCV_after_CP_step_charge_cycling[i].iloc[0]['Voltage (V)'])
        #print(i)
        dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Potential OCV charge at start'] = list_of_dataframes_OCV_after_charge[i].iloc[0][column_names_ocv_charging]# A new value is saved in the dataframe by index and column name. If the index and column already exist, the value is replaced, otherwise a new column is created
        dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Potential OCV charge at end'] = list_of_dataframes_OCV_after_charge[i].iloc[-1][column_names_ocv_charging]
        dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Potential Difference OCV charge at end'] = list_of_dataframes_OCV_after_charge[i].iloc[0][column_names_ocv_charging] - list_of_dataframes_OCV_after_charge[i].iloc[-1][column_names_ocv_charging]
    
    ### Entladekurven -> OCV
    for i in range(0, len(list_of_dataframes_OCV_after_discharge)):
        dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Potential OCV discharge at start'] = list_of_dataframes_OCV_after_discharge[i].iloc[0][column_names_ocv_discharging]# A new value is saved in the dataframe by index and column name. If the index and column already exist, the value is replaced, otherwise a new column is created
        dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Potential OCV discharge at end'] = list_of_dataframes_OCV_after_discharge[i].iloc[-1][column_names_ocv_discharging]
        dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Potential Difference OCV discharge at end'] = list_of_dataframes_OCV_after_discharge[i].iloc[0][column_names_ocv_discharging] - list_of_dataframes_OCV_after_discharge[i].iloc[-1][column_names_ocv_discharging]
        if list_of_labels is None:
            dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Cycle'] = (i+1)
        else:
            dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle.loc[i, 'Rate / C'] = list_of_labels[i]
    
        #print(dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle)
    return dataframes_of_potential_drop_beginning_OCV_and_end_OCV_per_cycle


def Sort_Peaks_Manually(dataframe_with_unsorted_peaks, charge_or_discharge, index_01C_first_peak_value, index_01C_second_peak_value, index_01C_third_peak_value, index_01C_fourth_peak_value, index_033C_first_peak_value, index_033C_second_peak_value, index_033C_third_peak_value, index_10C_first_peak_value):
    """Puts the dQ/dV peaks of the rate test into fixed columns: four peaks for 0.10 C, three for 0.33 C, one for 1.0 C.
    dataframe_with_unsorted_peaks = peak dataframe of Derive_Smooth_And_Find_Peaks, charge_or_discharge = text added to the column names,
    index_... = row index of the peak in the unsorted dataframe (None -> NaN). Returns a dataframe with one row."""
    # Dataframe for sorted Peaks
    dataframe_with_sorted_Peaks = pd.DataFrame()
    
    # Indices for 0.1 C rate
    a = index_01C_first_peak_value
    b = index_01C_second_peak_value
    c = index_01C_third_peak_value
    d = index_01C_fourth_peak_value
    
    # Indices for 0.33 C rate
    e = index_033C_first_peak_value
    f = index_033C_second_peak_value
    g = index_033C_third_peak_value
    
    # Indices for 1.0 C rate
    h = index_10C_first_peak_value
    
    
    # for 0.1 C Rate
    if a == None:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 1. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 1. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 1. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[a]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 1. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[a]['Peak Savgol-Filter <Ewe>/V']
    
    if b == None:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 2. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 2. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 2. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[b]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 2. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[b]['Peak Savgol-Filter <Ewe>/V']
        
    if c == None:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 3. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 3. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 3. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[c]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 3. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[c]['Peak Savgol-Filter <Ewe>/V']
    
    if d == None:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 4. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 4. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 4. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[d]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '0.10 C 4. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[d]['Peak Savgol-Filter <Ewe>/V']
        
       
    # for 0.33 C Rate
    if e == None:
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 1. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 1. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 1. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[e]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 1. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[e]['Peak Savgol-Filter <Ewe>/V']
    
    if f == None:
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 2. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 2. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 2. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[f]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 2. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[f]['Peak Savgol-Filter <Ewe>/V']
        
    if g == None:
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 3. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 3. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 3. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[g]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '0.33 C 3. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[g]['Peak Savgol-Filter <Ewe>/V']
    
    
    # for 1.0 C Rate
    if h == None:
        dataframe_with_sorted_Peaks.loc[0, '1.0 C 1. dQdV peak charge / mAh/V' + charge_or_discharge] = np.nan
        dataframe_with_sorted_Peaks.loc[0, '1.0 C 1. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = np.nan
    else:
        dataframe_with_sorted_Peaks.loc[0, '1.0 C 1. dQdV peak charge / mAh/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[h]['Peak Savgol-Filter dQ/dV / mAh/V']
        dataframe_with_sorted_Peaks.loc[0, '1.0 C 1. Peak Savgol-Filter <Ewe>/V' + charge_or_discharge] = dataframe_with_unsorted_peaks.iloc[h]['Peak Savgol-Filter <Ewe>/V']
          
        
    return dataframe_with_sorted_Peaks


def Extract_X_Values_At_Specific_Y_Value(list_of_dataframes, x_values_column_name, y1_values_column_name, y2_values_column_name, y_cap_for_comparison, y_ax_label, y_ax_limits, x_ax_label, x_ax_limits, save, name_figure, legend_title, list_RateTest_labels, active_mass_g=(12*0.7)/1000, potential_offset_2p=0.6, colorbar_ticks=None, colorbar_ticklabels=None):
    """Capacity at which the potential reaches a given value, for the 3-electrode (y1) and the 2-electrode (y2 + potential_offset_2p, default 0.6 V) potential of every rate.
    The x values of all points within +-0.1 % of y_cap_for_comparison are averaged (NaN if none); both curves are plotted.
    Capacity in mAh and in mAh/g (active_mass_g in g, default (12*0.7)/1000 g = 8.4 mg). save = 1 -> ./images/<name_figure>.png.
    colorbar_ticks/colorbar_ticklabels = positions (0..1) and labels of the colour bar (default the rates 0.10, 0.33, 1.00 C).
    Returns (dataframe 3-electrode, dataframe 2-electrode) with 'Capacity / mAh', 'Capacity / mAh/g', 'Rate / C'."""
    # Solution according to: https://stackoverflow.com/questions/43805821/matplotlib-add-colorbar-to-non-mappable-object
    fig, frame = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig.set_size_inches(cm2inch(8, 4))

    
    number_of_points = len(list_of_dataframes)
    
    dataframe_of_capacity_until_potential_cap_3p = pd.DataFrame(columns=['Capacity / mAh', 'Capacity / mAh/g', 'Rate / C'])
    dataframe_of_capacity_until_potential_cap_2p = pd.DataFrame(columns=['Capacity / mAh', 'Capacity / mAh/g', 'Rate / C'])

    cmap = my_colormap.resampled(number_of_points) # defining which colormap is used and how many colorpoints are collected

    for n,i in enumerate(range(0, len(list_of_dataframes))):
        x = (list_of_dataframes[i][x_values_column_name] - list_of_dataframes[i].iloc[0][x_values_column_name])
        y1 = list_of_dataframes[i][y1_values_column_name]   
        y2 = list_of_dataframes[i][y2_values_column_name] + potential_offset_2p
        cycle = 'Rate %s' %(list_RateTest_labels[i])
        datapoints = '; number of datat points: %s ; ' %(len(list_of_dataframes[i]))
        #y_max = list_of_dataframes[i].iloc[-1][y_values_column_name]
        #y_min = list_of_dataframes[i].iloc[0][y_values_column_name]
        #y_range = '%s from %s to %s' %(r' $ Potential $ / V  ', y_min, y_max)
        #label = cycle + datapoints + y_range
        
        # Calculation the range in which the values in the dataframe are searched
        lower_bound = y_cap_for_comparison - (y_cap_for_comparison * 0.001)
        upper_bound = y_cap_for_comparison + (y_cap_for_comparison * 0.001)
        
        # Gives the lines, which are in between the calculated boundaries as 'True'
        y1_potentials = y1.between(lower_bound, upper_bound)                                                                                              #   
        y2_potentials = y2.between(lower_bound, upper_bound)
        
        # Gives all line of the Dataframe which are before set to 'True'
        y1_potentials = list_of_dataframes[i][y1_potentials]
        y2_potentials = list_of_dataframes[i][y2_potentials]
        
        # Extracteing the specific values of the 'True' lines and convert them to a numpy array
        y1_potentials = y1_potentials[x_values_column_name].to_numpy()
        y2_potentials = y2_potentials[x_values_column_name].to_numpy()
        
        # Calculate the average value of the extracted values (Sum up all elements of the numpy array and devide trouhg the length of the array)
        # NaN if no value is found in the range
        y1_potetnials_average = np.sum(y1_potentials)/np.int64(len(y1_potentials)) if len(y1_potentials) > 0 else np.nan
        y2_potetnials_average = np.sum(y2_potentials)/np.int64(len(y2_potentials)) if len(y2_potentials) > 0 else np.nan
        
        dataframe_of_capacity_until_potential_cap_3p.loc[i, 'Capacity / mAh'] = y1_potetnials_average
        dataframe_of_capacity_until_potential_cap_3p.loc[i, 'Capacity / mAh/g'] = (y1_potetnials_average/active_mass_g) 
        dataframe_of_capacity_until_potential_cap_3p.loc[i, 'Rate / C'] = list_RateTest_labels[i]
        
        dataframe_of_capacity_until_potential_cap_2p.loc[i, 'Capacity / mAh'] = y2_potetnials_average
        dataframe_of_capacity_until_potential_cap_2p.loc[i, 'Capacity / mAh/g'] = (y2_potetnials_average/active_mass_g) 
        dataframe_of_capacity_until_potential_cap_2p.loc[i, 'Rate / C'] = list_RateTest_labels[i]
        
        
        
        print('Capacities for Potential cap at Rate %s C' %(list_RateTest_labels[i]))
        print('3p measurement:', y1_potetnials_average)
        print('2p measurement:', y2_potetnials_average)
        
        plt.plot(x, y1, c=cmap(n), linestyle='None', alpha=1.0, marker='.', label='3p ; WE vs REF', linewidth=1.5)
        plt.plot(x, y2, c=cmap(n), linestyle='None', alpha=0.3, marker='.', label='2p ; WE vs CE', linewidth=1.5)

        
    plt.hlines(y_cap_for_comparison, x_ax_limits[0], x_ax_limits[1])
    
    
    # Defining that a colorbar is plotted according to the defined colormap
    sm = plt.cm.ScalarMappable(cmap=cmap) # defining that the colomap is used for mappable
    sm.set_array([])
    if colorbar_ticks is None: # default: the three rates of the rate test
        colorbar_ticks = [0.17, 0.50, 0.83]
        colorbar_ticklabels = [0.10, 0.33, 1.00]
    cbar = plt.colorbar(sm, ax=plt.gca(), ticks=colorbar_ticks, label=r'$Rate$ / C') # defining which mappable is plottet as colorbar and which ticks and label
    cbar.ax.set_yticklabels(colorbar_ticklabels) # changes the label of the ticks
    

    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame, (-3,3))

    # Defining the axis
    frame.set_ylabel(y_ax_label)				                # Label of the y axis
    frame.set_ylim(y_ax_limits)                                                             # minimum and maximum value shown on the y axis
    #frame.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    
    frame.set_xlabel(x_ax_label)                                              # Label of the x axis
    #frame.set_xscale('log')
    frame.set_xlim(x_ax_limits)                                                         # minimum and maximum value shown on the x axis
    #frame.set_xticks([])                               # which values are shown on the x axis
    
    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame, name_figure, save, './images/%s.png' %(name_figure))
    
    plot = plt.show(block=False)
    
    return (dataframe_of_capacity_until_potential_cap_3p, dataframe_of_capacity_until_potential_cap_2p)

