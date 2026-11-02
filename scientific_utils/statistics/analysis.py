"""Fourier transform and autocorrelation of measurement data."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


def Calculate_Autocorrelation_Time_Constant(dataframe, y_values_column_name, time_column_name, lower_limit, upper_limit):
    """Autocorrelation function (ACF) of a relaxation curve (e.g. OCV after charging) and two estimates of its time constant.
    dataframe, y_values_column_name = potential column, time_column_name = time in s,
    lower_limit, upper_limit = window in which the ACF value exp(-1) = 0.37 is searched (should contain one value).
    Returns (ACF, lags, time constant in min from ACF = exp(-1), time constant in lags from -1/ln(ACF(1)))."""
    ########## Autocorrelation of a relaxation curve (e.g. OCV after charging) and its time constant #########
    # lower_limit, upper_limit: window in which the ACF value exp(-1) = 0.37 is searched (should contain only one value)
    array_OCV = dataframe[y_values_column_name].to_numpy() # Converts one column of the dataframe to a numpy array

    ##### Autocorrelation function with the statsmodel package
    acf_array_OCV = sm.tsa.stattools.acf(array_OCV, nlags=len(array_OCV)) # Calculation of the autocorrelation function

    acf_array_lag_OCV = range(1, len(acf_array_OCV)+1) # Calculation of the lags, equal to the length of the array

    ##### Calculating the time constant
    ### 1. Variant (T = v , r(v) = exp(-1) = 0,37)
    delta_t = dataframe.iloc[1][time_column_name] - dataframe.iloc[0][time_column_name] # Calculation of the time between two measurement points

    acf_dataframe_OCV = pd.DataFrame.from_records({'ACF': acf_array_OCV}) # Converts the array of the autocorrelation function to a dataframe

    acf_dataframe_OCV_value = acf_dataframe_OCV['ACF'].between(lower_limit, upper_limit) # Search values in the dataframe between the two given values
    acf_dataframe_OCV_value = acf_dataframe_OCV[acf_dataframe_OCV_value] # Keeps only the values where the entry in 'acf_dataframe_OCV' is equal to the entry in 'acf_dataframe_OCV_value' (should be only one value)
    acf_dataframe_OCV_value_index = acf_dataframe_OCV[acf_dataframe_OCV['ACF']==acf_dataframe_OCV_value.iloc[0]['ACF']].index.values # Index of the filtered value, which is the 'lag' here
    time_constant_in_min = (acf_dataframe_OCV_value_index  * delta_t)/60 # Calculation of the time constant from delta_t between two measurement points and the index/lag

    ### 2. Variant (v = 1 , T = - (1/ln(r(1))))
    r_1_value = acf_dataframe_OCV.iloc[1]['ACF'] # Takes the value with index 1 (first value of the lag)

    T = - (1/(np.log(r_1_value))) # Calculation of the time constant (in lags)

    return acf_array_OCV, acf_array_lag_OCV, time_constant_in_min, T
