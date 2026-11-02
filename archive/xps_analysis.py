"""Unused functions moved here from `scientific_utils/xps/analysis.py` (nothing in the repository called them)."""

from scipy import interpolate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import scipy
import scipy.signal

from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32
from scientific_utils.general.analysis import Round_Down_To_Odd


def Extract_XPS_DetailSpectra_From_Single_Scan(a, b):
    """Takes one region (e.g. 'C 1s') out of a CasaXPS export: x column, raw data ('CPS'), fitted components and background; empty rows dropped.
    a = dataframe of the export, b = string of the region in the column names. Returns the dataframe of the region."""
    # Define Parameters
    dataframe = a
    string_filter = b
    
    # Dataframe Column names into list
    column_names = list(dataframe.columns)
    
    ###
    # extract all y Columns
    y_column_names = [k for k in column_names if string_filter in k]
    
    # extract only raw data column
    raw_data_y_column = [k for k in column_names if string_filter in k and 'CPS' in k]
    
    # select the fitted component columns
    fit_components_column_names = [x for x in y_column_names  if x not in raw_data_y_column]
    
    ###
    # select background column
    if len(fit_components_column_names) == 0:
        background_column_name = column_names[(column_names.index( raw_data_y_column[0]) + 1)]
    else:
        background_column_name = column_names[(column_names.index(fit_components_column_names[-1]) + 1)]

    ###
    # select x axis column for carbon
    x_column_name = column_names[(column_names.index(y_column_names[0]) - 1)]
    
    ###
    # Transform background and x axis Column name into list
    background_column_name = [background_column_name]
    x_column_name = [x_column_name]
    
    ###
    #
    # Extract only the Data concering Oxygen Spectra
    extracted_column_names = x_column_name + raw_data_y_column + fit_components_column_names + background_column_name
    extracted_dataframe = dataframe[extracted_column_names]

    # Remove all columns without a value
    extracted_dataframe = extracted_dataframe.dropna(how='all')
    
    return extracted_dataframe


def Determine_Area_XPS(a, b, c, d, e=None, f=None):
    """Area between the raw data and the background (trapezoidal rule on the measured points, absolute value), optionally between two binding energies.
    a = dataframe, b = x column (binding energy in eV), c = data column, d = background column, e, f = limits in eV (any order; None = all).
    Unit: eV times the unit of the intensity (e.g. CPS eV). Returns 0.0 if no point is inside the limits."""
    dataframe = a
    x_values_column_name = b
    y_column_name_data = c
    y_column_name_background = d
    
    # Handle XPS limits (High to Low vs Low to High)
    # Pandas .between() fails if lower_limit > upper_limit.
    # We sort them to ensure we always search from Min to Max.
    if e is not None and f is not None:
        actual_lower = min(e, f)
        actual_upper = max(e, f)
        
        # Select data
        mask = dataframe[x_values_column_name].between(actual_lower, actual_upper)
        dataframe_short = dataframe[mask].copy() # .copy() avoids warnings
    else:
        dataframe_short = dataframe.copy()

    # Check if data exists after filtering
    if dataframe_short.empty:
        return 0.0

    # Define X and Y
    x = dataframe_short[x_values_column_name].values
    y1 = dataframe_short[y_column_name_data].values
    y2 = dataframe_short[y_column_name_background].values

    # Skip the heavy interpolation. 
    # Using Trapezoidal rule on the raw data is faster and mathematically equivalent 
    # to the area of the linear interpolation.
    
    # Calculate the area between curves (Raw - Background)
    # We use abs() to handle the High->Low binding energy direction automatically
    area = np.abs(np.trapezoid(y1 - y2, x))

    return area


def Resample_XY_Data_With_Plot(dataframe, x_values_column_name, y_values_column_name, number_of_points):
    """Like general.analysis.Resample_XY_Data, but the resampled curve is drawn into the current figure.
    Returns [x_new, y_new] instead of a dataframe."""
    ##############################################################################
    ########## defines the x and y values and Parameters for Resampling ##########
    ##############################################################################
    x = dataframe[x_values_column_name]
    y = dataframe[y_values_column_name]
    number_of_points = number_of_points
        
    ##### calculating the equidistant step size
    x_delta = (x.max() - x.min())/number_of_points
    ##### new numpy array with equidistand y values
    x_new = np.arange(x.min(), x.max(), x_delta)
        
    ##### linear interpolation
    linear_interpolation = interpolate.interp1d(x, y, axis=0, fill_value="extrapolate")
    ##### resample of x with the linear interpolation model
    y_new = linear_interpolation(x_new)
      
    ##### plotting
    plt.plot(x_new, y_new, color='red', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data Resampled', linestyle='-', linewidth=0.8)
   
    return [x_new, y_new]


def Derive_XY_Data_With_Plot(dataframe, x_values_column_name, y_values_column_name):
    """Like general.analysis.Derive_XY_Data (without removing NaN), the derivative is drawn into the current figure.
    Returns [X, dYdX]."""
    ################################################
    ########## defines the x and y values ##########
    ################################################
    x = dataframe[x_values_column_name]
    y = dataframe[y_values_column_name]

    ##### Measurement data converted in numpy array
    X = x.to_numpy() 
    Y = y.to_numpy()
    
    ##### Calculation of the derivation
    dX = np.diff(X)
    dY = np.diff(Y)
    dYdX = dY/dX
    
    ##### Shorten of the X-Arrays, because during derivation one point is lost
    X = np.delete(X, -1)
        
    ##### plotting
    plt.plot(X, dYdX, color='orange', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data derived', linestyle='-', linewidth=0.8)
   
    return [X, dYdX ]


def Smooth_XY_Data_With_Plot(dataframe, x_values_column_name, y_values_column_name, ratio_of_points_used_for_smoothing):
    """Savitzky-Golay filter (2nd order, without the moving average of general.analysis.Smooth_XY_Data); adds '<y> smoothed'
    and draws it into the current figure. d = ratio of the points used for the filter window (0..1). Returns the dataframe."""
    #############################################################################
    ########## defines the x and y values  and Parameters for Smoothig ##########
    #############################################################################
    x = dataframe[x_values_column_name]
    y = dataframe[y_values_column_name]
    ratio_of_points = ratio_of_points_used_for_smoothing
    
    ########################################
    ########## Smoothing the Data ##########
    ########################################
    print('----------------- \nstarting smoothing')
    ##### Calculation of the number of points used for Savitzky Golay Filter
    number_of_points_for_smoothing = int(Round_Down_To_Odd(len(y) * ratio_of_points))
    ##### Calculation of the Smoothed data with the Savitzky Golay Filter and a Polynomial of second order
    y_savgol = scipy.signal.savgol_filter(y, number_of_points_for_smoothing, 2)
    ##### Saving the smoothed Data in the Input Dataframe
    dataframe[y_values_column_name + ' smoothed'] = y_savgol
    
    print('finished smoothing\n------------------')
    
    ########################################
    ########## Plotting the Data ##########
    ########################################
    
    #plt.plot(x, y, color='blue', alpha=1, marker='.', markersize=10, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data', linestyle='-', linewidth=1)
    plt.plot(x, y_savgol, color='yellow', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data Smoothed', linestyle='-', linewidth=0.8)
   
    return dataframe


def Determine_Area_Between_Two_Curves(dataframe, x_values_column_name, y1_values_column_name, y2_values_column_name, x_lower_limit, x_upper_limit):
    """Area between two curves (y1 - y2) between x_lower_limit and x_upper_limit: interpolated on a 10x finer x step, summed up as rectangles,
    filled green in the current figure, printed. Unit: unit of x times unit of y. Returns the area."""
    ############################################################
    ########## defines the x and y values  and limits ##########
    ############################################################
    x = dataframe[x_values_column_name]
    y1 = dataframe[y1_values_column_name]
    y2 = dataframe[y2_values_column_name]
    x_lower = x_lower_limit
    x_upper = x_upper_limit
    
    ##### extracting the selected range of data by the upper and lower limit
    boolean_variables = x.between(x_lower_limit,x_upper_limit)              # returns 'True' for the rows where the value (potential) is in the given range (lower_limit to upper_limit)
    dataframe_short = dataframe[boolean_variables]                          # returns all rows of the dataframe marked with 'True'
        
    ##### redefining x and y new in the selected x range
    x = dataframe_short[x_values_column_name]
    y1 = dataframe_short[y1_values_column_name]
    y2 = dataframe_short[y2_values_column_name]
        
    #plt.plot(x, y1, alpha=0.75, marker='.', markersize=7, markeredgecolor='black', markeredgewidth=0.1, label='Y1-Data', linestyle='-', linewidth=0.5)
    #plt.plot(x, y2, alpha=0.75, marker='.', markersize=7, markeredgecolor='black', markeredgewidth=0.1, label='Y2-Data', linestyle='-', linewidth=0.5)

    ###################################
    ########## Interpolation ##########
    ###################################
    ##### linear interpolation
    linear_interpolation_y1 = interpolate.interp1d(x, y1, axis=0, fill_value="extrapolate")
    linear_interpolation_y2 = interpolate.interp1d(x, y2, axis=0, fill_value="extrapolate")
    ##### resample of x with the linear interpolation model
    x_stepsize = (x.iloc[1] - x.iloc[0])/10
    x_interpol = pd.Series(np.arange(x.iloc[0], x.iloc[-1], x_stepsize))
    y1_interpol = pd.Series(linear_interpolation_y1(x_interpol))
    y2_interpol = pd.Series(linear_interpolation_y2(x_interpol))

    area_y1 = 0
    area_y2 = 0
    #for i in range(y_corrected.index[0], y_corrected.index[-2]):
    for i in range(0, len(y1_interpol)-1):
        plt.fill_between([x_interpol.iloc[i],x_interpol.iloc[i+1]], y2_interpol.iloc[i], y1_interpol.iloc[i], facecolor="green", alpha=0.5)
        area_y1 += y1_interpol.iloc[i] * (x_interpol.iloc[i+1] - x_interpol.iloc[i])
        area_y2 += y2_interpol.iloc[i] * (x_interpol.iloc[i+1] - x_interpol.iloc[i])
    
    area = area_y1 - area_y2
          
    print('The area of Y1 is: %s' %(area_y1))
    print('The area of Y2 is: %s' %(area_y2))
    print('The area of the summed up points are: %s' %(area))
        
    return area
