"""Unused functions moved here from `scientific_utils/general/analysis.py` (nothing in the repository called them)."""

from scipy import interpolate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.signal


def Extract_Dataframes_By_Index_From_List_Of_Lists(a, b):
    """Takes the same entries (by index) out of every inner list of a list of lists.
    a = list of lists of dataframes, b = list of indices.
    Returns a list of lists with only the selected dataframes."""

    ########## Define all Parameters
    list_of_list_with_dataframes =  a
    list_of_target_indices = b
    
    ##### Define empty list for extracted dataframes
    list_of_list_with_extracted_dataframes = []
    
    for i in range(len(list_of_list_with_dataframes)):
        dataframe_list = []
        for j in range(len(list_of_target_indices)):
            index = list_of_target_indices[j]
            dataframe_list.append(list_of_list_with_dataframes[i][index])
        list_of_list_with_extracted_dataframes.append(dataframe_list)
    
    return list_of_list_with_extracted_dataframes


def Scale_To_Max(a, b):
    """Divides a column by its maximum (values 0..1 for positive data) and adds it as a new column.
    a = dataframe, b = column name.
    Returns (dataframe, name of the new column '<b>_max_scaled')."""
    dataframe = a
    column_name = b
    
    new_column_name = column_name + '_max_scaled'
    
    dataframe[new_column_name] = dataframe[ column_name] / dataframe[column_name].max()
    
    return dataframe, new_column_name


def Scale_To_MinMax(dataframe, min_max_scaler_parameters):
    """Min-max scaling of a column to 0..1, added as the new column '<column_name>min_max_scaled'.
    dataframe = dataframe, min_max_scaler_parameters = dictionary with the key 'column_name'. Returns the dataframe."""
    dataframe = dataframe
    column_name = min_max_scaler_parameters.get('column_name')
    data = dataframe[column_name]
    dataframe[column_name + 'min_max_scaled'] = (data - data.min()) / (data.max() - data.min())
    
    return dataframe


def Resample_XY_Data(a, b, c, d):
    """Linear interpolation of y on equidistant x values (number_of_points steps between min and max of x).
    a = dataframe, b = x column name, c = y column name, d = number of points.
    Returns a new dataframe with the columns '<b>_interpolated' and '<c>_interpolated'."""
    
    dataframe = a
    x_values_column_name = b
    y_values_column_name = c
    number_of_points = d
    
    
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
    #plt.plot(x_new, y_new, color='red', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data Resampled', linestyle='-', linewidth=0.8)
   
    ##### Data into a new dataframe
    x_column_name_new = x_values_column_name + '_interpolated'
    y_column_name_new = y_values_column_name + '_interpolated'
    
    interpolated_data = pd.DataFrame({x_column_name_new: x_new, y_column_name_new: y_new})

    return interpolated_data


def Derive_XY_Data(a, b, c):
    """Derivative dY/dX from the differences of neighbouring points (x loses its last point).
    a = dataframe, b = x column name, c = y column name. Units: unit of y per unit of x.
    Rows with NaN are dropped; repeated x values give inf (resample first).
    Returns a new dataframe with the columns '<b>_X' and '<c>_dYdX'."""
        
    dataframe = a
    x_values_column_name = b
    y_values_column_name = c
    
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
    with np.errstate(divide='ignore', invalid='ignore'): # repeated x values (dX = 0) give inf in raw data, this is why the data is resampled before deriving
        dYdX = dY/dX
    
    ##### Shorten of the X-Arrays, because during derivation one point is lost
    X = np.delete(X, -1)
        
    ##### plotting
    #plt.plot(X, dYdX, color='orange', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data derived', linestyle='-', linewidth=0.8)
   
    ##### Data into a new dataframe
    x_column_name_new = x_values_column_name + '_X'
    y_column_name_new = y_values_column_name + '_dYdX'
    
    derived_data = pd.DataFrame({x_column_name_new: X, y_column_name_new: dYdX})

    derived_data =derived_data.dropna()
    
    return derived_data


def Smooth_XY_Data(a, b, c, d):
    """Smooths y with a moving average and then a Savitzky-Golay filter (2nd order polynomial).
    a = dataframe, b = x column name, c = y column name, d = ratio of the points used for the filter window (0..1).
    Adds the column '<c> smoothed' and returns the dataframe."""
    
    dataframe = a
    x_values_column_name = b
    y_values_column_name = c
    ratio_of_points_used_for_smoothing = d
    
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
    
    # smooth the curve with a moving average
    window_size = number_of_points_for_smoothing/2
    window_size = int(Round_Down_To_Odd(window_size))
    y_ma = np.convolve(y, np.ones(window_size)/window_size, mode='same')
    
    #y_ma = y
    
    # ##### Calculation of the Smoothed data with the Savitzky Golay Filter and a Polynomial of second order
    # window_size = int(round_down_to_odd(number_of_points_for_smoothing/4))
    # y_ma = scipy.signal.savgol_filter(y, window_size, 2)
    
    ##### Calculation of the Smoothed data with the Savitzky Golay Filter and a Polynomial of second order
    y_savgol = scipy.signal.savgol_filter(y_ma, number_of_points_for_smoothing, 2)
    ##### Saving the smoothed Data in the Input Dataframe
    dataframe[y_values_column_name + ' smoothed'] = y_savgol
    
    print('finished smoothing\n------------------')
    
    ########################################
    ########## Plotting the Data ##########
    ########################################
    
    #plt.plot(x, y, color='blue', alpha=1, marker='.', markersize=10, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data', linestyle='-', linewidth=1)
    #plt.plot(x, y_savgol, color='yellow', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data Smoothed', linestyle='-', linewidth=0.8)
   
    return dataframe


def Determine_Area(a, b, c, d, e= None, f = None):
    """Area between a data column and a background column (data minus background), optionally only between two x values.
    a = dataframe, b = x column name, c = data column, d = background column, e, f = lower and upper x limit (None = whole range).
    The curves are interpolated on a 1000x finer x step and summed up (rectangles). Unit: unit of x times unit of y."""
    ############################################################
    ########## defines the x and y values  and limits ##########
    ############################################################
    dataframe = a
    x_values_column_name = b
    y_column_name_data = c
    y_column_name_background = d
    x_lower_limit = e
    x_upper_limit = f
    
    ##### extracting the selected range of data by the upper and lower limit, if there is a upper and Lower range given
    if x_lower_limit != None:
        boolean_variables = dataframe[x_values_column_name].between(x_lower_limit, x_upper_limit)              # returns 'True' for the rows where the value (potential) is in the given range (lower_limit to upper_limit)
        dataframe_short = dataframe[boolean_variables]  # returns all rows of the dataframe marked with 'True'
    else: 
        dataframe_short = dataframe
        
    ##### redefining x and y new in the selected x range
    x = dataframe_short[x_values_column_name]
    y1 = dataframe_short[y_column_name_data]
    y2 = dataframe_short[y_column_name_background]

    ###################################
    ########## Interpolation ##########
    ###################################
    ##### linear interpolation
    linear_interpolation_y1 = interpolate.interp1d(x, y1, axis=0, fill_value="extrapolate")
    linear_interpolation_y2 = interpolate.interp1d(x, y2, axis=0, fill_value="extrapolate")
    ##### resample of x with the linear interpolation model
    x_stepsize = (x.iloc[1] - x.iloc[0])/1000
    x_interpol = pd.Series(np.arange(x.iloc[0], x.iloc[-1], x_stepsize))
    y1_interpol = pd.Series(linear_interpolation_y1(x_interpol))
    y2_interpol = pd.Series(linear_interpolation_y2(x_interpol))

    area_y1 = 0
    area_y2 = 0
    #for i in range(y_corrected.index[0], y_corrected.index[-2]):
    
    #######################################################
    ########## Calculate Area + Plotting Results ##########
    #######################################################    
    # Assuming y1_interpol, y2_interpol, and x_interpol are pandas Series
    x_interpol = x_interpol.to_numpy()
    y1_interpol = y1_interpol.to_numpy()
    y2_interpol = y2_interpol.to_numpy()
    
    # Sort the arrays based on x_interpol
    sorted_indices = np.argsort(x_interpol)
    x_interpol = x_interpol[sorted_indices]
    y1_interpol = y1_interpol[sorted_indices]
    y2_interpol = y2_interpol[sorted_indices]
    
    # Calculate the differences between consecutive x values
    dx = np.diff(x_interpol)

    # Calculate the area under y1 and y2
    area_y1 = np.sum(y1_interpol[:-1] * dx)
    area_y2 = np.sum(y2_interpol[:-1] * dx)

    # Total area between the curves
    total_area = area_y1 - area_y2

    # Optionally, plot the area between the curves
    # plt.plot(x, y1, alpha=0.75, marker='.', markersize=7, markeredgecolor='black', markeredgewidth=0.1, label='Y1-Data', linestyle='-', linewidth=0.5)
    # plt.plot(x, y2, alpha=0.75, marker='.', markersize=7, markeredgecolor='black', markeredgewidth=0.1, label='Y2-Data', linestyle='-', linewidth=0.5)
    # plt.fill_between(x_interpol, y2_interpol, y1_interpol, facecolor='green', alpha=0.3)
    # plt.show()
        
    return total_area


def Remove_Outliers_MAD(a, b, c, d):
    """
    Remove outliers from noisy data using median absolute deviation (MAD) method.
    
    Parameters
    ----------
    data : array_like
        The input data from which to remove outliers.
    thresh : float, optional
        The threshold for outlier detection. Data points that are `thresh` times 
        farther from the median than the median absolute deviation will be 
        considered outliers. Default == 3.5.
        
    Returns
    -------
    array_like
        A new array containing the input data with outliers removed.
    """
    
    #############################################################################
    ########## defines the x and y values  and Parameters for Smoothig ##########
    #############################################################################
    dataframe = a
    x_values_column_name = b
    y_values_column_name = c
    thresh = d
    
    ##### define Data
    x = dataframe[x_values_column_name]
    y = dataframe[y_values_column_name]
    
    ##### calculate outliers
    median = np.median(y)
    mad = np.median(np.abs(y - median))
    z_score = 0.6745 * (y - median) / mad
    good = np.abs(z_score) < thresh
    
    ##### Extract rows by index
    dataframe = dataframe.loc[y[good].index]
    
    ##### reset index
    dataframe = dataframe.reset_index()
    
    return dataframe
    
#     a = dataframe = derived_data
#     b = x_values_column_name = 'Voltage (V)_interpolated_X'
#     c = y_values_column_name = 'specific Capacity (mAh/g)_interpolated_dYdX'
#     d = thresh = 2

#     data_cleaned = remove_outliers(a, b, c, d)
    
    ########################################
    ########## Plotting the Data ##########
    ########################################
    
    #plt.plot(x, y, color='blue', alpha=1, marker='.', markersize=10, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data', linestyle='-', linewidth=1)
    #plt.plot(x, y_savgol, color='yellow', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data Smoothed', linestyle='-', linewidth=0.8)
   
    return dataframe


def Remove_Local_Outliers(a, b, c, d):
    """Removes points that are far from the local mean (rolling window, centred).
    a = dataframe, b = window size (rows), c = column name, d = threshold of the local z-score.
    Adds the helper columns Rolling_Mean, Rolling_Std, Z_Score, Is_Local_Outlier. Returns the filtered dataframe."""
    ########## Define all Parameters
    dataframe =  a
    window_size = b
    column_name = c
    local_outlier_threshold = d

    # Calculate the mean values and standard deviations with a rolling window
    dataframe['Rolling_Mean'] = dataframe[column_name].rolling(window=window_size, center=True).mean()
    dataframe['Rolling_Std'] = dataframe[column_name].rolling(window=window_size, center=True).std()

    # Calculate the z-scores from the mean value and standard deviation
    dataframe['Z_Score'] = np.abs((dataframe[column_name] - dataframe['Rolling_Mean']) / dataframe['Rolling_Std'])

    # Mark points as outliers based on the local z-score threshold
    dataframe['Is_Local_Outlier'] = dataframe['Z_Score'] > local_outlier_threshold

    # Filter the data to remove local outliers
    filtered_data = dataframe[dataframe['Is_Local_Outlier'] != True]

    return filtered_data


def Offset_Dataframes(a, b, c):
    """Waterfall offset: every column is divided by its first value and then shifted up.
    a = list of dataframes (changed in place), b = column name per dataframe,
    c = offset: one number -> (i+1)*c for the i-th dataframe, or a list with one offset per dataframe.
    Returns the list of dataframes."""
    list_of_dataframes = a
    list_of_list_of_column_names = b
    offset_config = c # Can now be a single float OR a list of floats
    
    for i in range(len(list_of_dataframes)):
        # Check if c is a list or a single value
        if isinstance(offset_config, list):
            # Use specific value from list if available, else fallback to index math
            current_offset = offset_config[i] if i < len(offset_config) else (i + 1) * 1.0
        else:
            current_offset = (i + 1) * offset_config
            
        col_name = list_of_list_of_column_names[i]
        # Applying the offset
        list_of_dataframes[i][col_name] = (list_of_dataframes[i][col_name] / list_of_dataframes[i][col_name].iloc[0]) + current_offset
            
    return list_of_dataframes


def Offset_Dataframes_Without_Normalization(list_of_dataframes, list_of_column_names, offset_config):
    """
    Adds a vertical offset to specific columns in a list of DataFrames 
    for waterfall plotting, without normalizing the intensities.
    """
    for i in range(len(list_of_dataframes)):
        # Determine the offset for the current spectrum
        if isinstance(offset_config, list):
            # Use specific value from list if available
            current_offset = offset_config[i] if i < len(offset_config) else (i + 1) * 1.0
        else:
            # Multiply the scalar offset by the index (i + 1) to stack them
            current_offset = (i + 1) * offset_config
            
        col_name = list_of_column_names[i]
        
        # Applying ONLY the offset (removed the division by iloc[0])
        list_of_dataframes[i][col_name] = list_of_dataframes[i][col_name] + current_offset
            
    return list_of_dataframes


def Offset_Dataframes_Automatic(list_of_dataframes, list_of_column_names, spacing_factor=0.1):
    """
    Automates waterfall offsets based on the data's scale.
    
    Args:
        list_of_dataframes: List of pd.DataFrames.
        list_of_column_names: List of strings (Y-axis columns).
        spacing_factor: How much 'white space' to put between spectra 
                        (0.1 = 10% of the max peak height).
    """
    # 1. Find the maximum peak height across all dataframes to set a scale
    all_max_values = [df[col].max() for df, col in zip(list_of_dataframes, list_of_column_names)]
    global_max = max(all_max_values)
    
    # 2. Define the step size based on that max
    # We use a fraction of the max height so the offset scales with your data
    step_size = global_max * (1 + spacing_factor)

    for i in range(len(list_of_dataframes)):
        col_name = list_of_column_names[i]
        
        # 3. Apply the automated offset
        # The first spectrum (i=0) stays at 0, the second shifts by one step, etc.
        current_offset = i * step_size
        
        list_of_dataframes[i][col_name] = list_of_dataframes[i][col_name] + current_offset
            
    return list_of_dataframes


def Offset_Dataframes_By_Range(list_of_dataframes, list_of_column_names):#, gap_ratio=0.05):
    """
    Automates waterfall offsets based on the 'Peak-to-Peak' range of the data.
    
    Args:
        list_of_dataframes: List of pd.DataFrames.
        list_of_column_names: List of strings for the Y-axis.
        gap_ratio: The size of the empty space between spectra as a percentage 
                   of the largest peak height (0.1 = 10% gap).
    """
    # 1. Calculate the 'Span' (Max - Min) for each spectrum
    spans = []
    for df, col in zip(list_of_dataframes, list_of_column_names):
        span = df[col].max() - df[col].min()
        print('Span Min Max is', span)
        spans.append(span)
    
    # 2. Use the largest span found as the universal 'Step'
    # This ensures even the tallest peak has enough room.
    max_span = max(spans)
    step_size = max_span #*(1 + gap_ratio)

    for j in range(len(list_of_dataframes)):
        col_name = list_of_column_names[j]
        
        # 3. Apply the offset
        # We also subtract the local minimum to 'zero' the baseline 
        # before adding the waterfall step.
        current_offset = (j+0.5) * step_size
        
        # Expert Move: (Value - Min) 'zeros' the baseline, then we add the step.
        list_of_dataframes[j][col_name] = (list_of_dataframes[j][col_name] - list_of_dataframes[j][col_name].min()) + current_offset
        #list_of_dataframes[j][col_name] = list_of_dataframes[j][col_name] + current_offset
            
    return list_of_dataframes


def Normalize_Dataframes_For_Overlay(list_of_dataframes, list_of_column_names):
    """
    Normalizes multiple spectra to a 0-1 scale to allow for direct overlay 
    and visualization of X-axis shifts.
    
    Args:
        list_of_dataframes: List of pd.DataFrames.
        list_of_column_names: List of strings for the Y-axis.
    """
    for df, col in zip(list_of_dataframes, list_of_column_names):
        # 1. Identify the minimum and maximum values
        y_min = df[col].min()
        y_max = df[col].max()
        
        # 2. Prevent division by zero if the column is empty or constant
        if y_max - y_min == 0:
            df[col] = 0
            continue
            
        # 3. Apply Min-Max Normalization: (Value - Min) / (Max - Min)
        # This 'zeros' the baseline and sets the highest peak to 1.0
        df[col] = (df[col] - y_min) / (y_max - y_min)
            
    return list_of_dataframes


def Offset_One_Column_In_List_Of_Dataframes(a, b, c):
    """Like Offset_Dataframes with one offset number, but on copies (the input dataframes stay unchanged).
    a = list of dataframes, b = column name per dataframe, c = offset step: the i-th column is divided by its first value + (i+1)*c.
    Returns the list of new dataframes."""
    # Define Parameters
    list_of_dataframes = a
    list_of_column_names = b
    offset_value = c
    
    # copy list of dataframe to not change initial data
    new_list_of_dataframes = []
    for i in list_of_dataframes:
        new_list_of_dataframes.append(i.copy()) 
    
    # getting offset in the data
    for i in range(len(list_of_column_names)):
        column_name = list_of_column_names[i]
        new_list_of_dataframes[i][column_name] = (new_list_of_dataframes[i][column_name] / new_list_of_dataframes[i][column_name].iloc[0]) + ((i+1) * offset_value)
            
    return new_list_of_dataframes


def Normalize_And_Offset_One_Column_In_List_Of_Dataframes(a, b, c, d):
    """Divides the column of the i-th dataframe by its own value and adds its own offset (changed in place).
    a = list of dataframes, b = column name per dataframe, c = list of normalisation values, d = list of offsets (i-th offset is multiplied by i+1).
    Returns the list of dataframes."""
    # Define Parameters
    list_of_dataframes = a
    list_of_column_names = b
    list_of_norm_values = c
    list_of_offset_values = d
    
    # getting offset in the data
    for i in range(len(list_of_dataframes)):
        column_name = list_of_column_names[i]
        list_of_dataframes[i][column_name] = ((list_of_dataframes[i][column_name] / list_of_norm_values[i]) + + ((i+1) * list_of_offset_values[i]))
            
    return list_of_dataframes


def Delete_List_Entries(list_of_dataframes):
    """Deletes the entries with index 4 and 2 from a list (fixed indices for one data set).
    Returns the shortened list."""
    del list_of_dataframes[4] # deleteing the fouth list entry (important is to first delete the higher index entry)
    del list_of_dataframes[2] # deleting teh second list entry
    return list_of_dataframes


def Extract_Range_Of_Column_Names(dataframe_for_extraction, column_name_beginning, column_name_end, string1_as_filter, string2_as_filter):
    """Column names between two columns (both included), filtered by two strings.
    dataframe_for_extraction = dataframe, column_name_beginning / column_name_end = first and last column,
    string1_as_filter / string2_as_filter = strings the names must contain.
    Returns (names with string 1, names with string 2)."""
    # Get index of the Columns
    index_column_name_beginning = dataframe_for_extraction.columns.get_loc(column_name_beginning)
    index_column_name_end = 1 + dataframe_for_extraction.columns.get_loc(column_name_end)

    # list of all column names between the indices
    list_of_column_names = dataframe_for_extraction.columns[index_column_name_beginning:index_column_name_end]

    # filter the list by two different strings
    list_of_column_names_with_string1_as_filter = [k for k in list_of_column_names if string1_as_filter in k]
    list_of_column_names_with_string2_as_filter = [k for k in list_of_column_names if string2_as_filter in k]

    return (list_of_column_names_with_string1_as_filter, list_of_column_names_with_string2_as_filter)


def Find_Peaks_In_XY_Data(dataframe, x_values_column_name, y_values_column_name, ratio_of_points_used_for_peaksearch, prominence_for_peaksearch):
    """Peak search with scipy.signal.find_peaks; the peaks are also drawn as red crosses into the current Matplotlib figure.
    dataframe, x/y_values_column_name = columns, ratio_of_points_used_for_peaksearch = minimum peak width as ratio of all points (0..1),
    prominence_for_peaksearch = prominence (number or (min, max)) in the unit of y.
    Returns a dataframe with the columns '<x> peak values' and '<y> peak values'."""
    ################################################################################
    ########## defines the x and y values  and Parameters Peak Extraction ##########
    ################################################################################
    x = dataframe[x_values_column_name]
    y = dataframe[y_values_column_name]
    ratio_of_points = ratio_of_points_used_for_peaksearch
    prominence = prominence_for_peaksearch
    
    ################################################################################
    ################################# Peak Extraction ##############################
    ################################################################################
    print('----------------- \nstarting peak extraction ')
    
    ##### Calculation of the number of points used for the Peak extract function
    number_of_points = int(len(y) * ratio_of_points)
        
    ##### Peak extract from the smoothed data
    y_peak = scipy.signal.find_peaks(y,                                        
                                    #height = 0.01,                  # returns the indices of the minimum values, that is why there is a "-" in front of the data name
                                    #threshold = None,               # minimum height a peak must have
                                    #distance=0.2,                   # Required threshold of peaks, the vertical distance to its neighbouring samples
                                    prominence=prominence,           # Number of data points a peak must contain
                                    width=number_of_points
                                    )
    #print(y_peak)
    #print('-----------------')
    ##### Convert the array of the find peaks function into a one float 
    y_peak = y_peak[0]        # y_peak[0] = Index of the line where the peak is found
    print(y_peak)
    
    ##### if no peak is found the peak data is set to "Nan"
    if len(y_peak) == 0:                                                      
        peak_Y = np.nan
        peak_X = np.nan
    else:
        peak_Y = y[y_peak]               # Returns the y values for the indices
        peak_X = x[y_peak]               # Returns the x values for the indices
    
    ##### Saving the extraceted Peaks in a Dataframe
    peaks_dataframe = pd.DataFrame()
    peaks_dataframe[x_values_column_name + ' peak values'] = peak_X
    peaks_dataframe[y_values_column_name + ' peak values'] = peak_Y
    
    #print('-----------------')
    #print(peaks_dataframe)
    print('ending peak extraction \n -----------------')
    
    ########################################
    ########## Plotting the Data ##########
    ########################################
    
    #plt.plot(x, y, color='blue', alpha=1, marker='.', markersize=10, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data', linestyle='-', linewidth=1)
    plt.plot(peak_X, peak_Y, color='red', alpha=0.80, marker='X', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Peaks', linestyle='', linewidth=0)
   
    
    return peaks_dataframe
