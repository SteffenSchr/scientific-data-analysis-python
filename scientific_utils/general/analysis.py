"""Data handling used by every measurement technique: normalising, scaling, resampling, smoothing, offsets."""

from scipy import interpolate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.signal


def Convert_DataframeColumns_To_Float32(a):
    """Changes every column that contains only numbers (as text or objects) to float (downcast, mostly float32); other columns stay.
    a = dataframe (changed in place). Returns the dataframe."""
    # define parameters
    dataframe = a

    #bool_list = file.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
    bool_list = []
    for k in range(len(dataframe.columns)):
        column = dataframe.columns[k]
        bool_entry = pd.to_numeric(dataframe[column], errors='coerce').notnull().all()
        bool_list.append(bool_entry)
        
    # changing the datatype of the columns from string to float
    for h in range(len(bool_list)):
        #print(bool_list[h])
        if bool_list[h] == True:
            #print(file.columns[h])
            dataframe[dataframe.columns[h]] = pd.to_numeric(dataframe[dataframe.columns[h]], downcast="float")
            #print(file[file.columns[h]].dtypes)  
        else:
            pass
    
    return dataframe


def Extract_MaxMinValues_From_List_Of_Dataframes(a, b):
    """Maximum and minimum of one column in every dataframe of a list.
    a = list of dataframes, b = column index (position, not name).
    Returns (list of maxima, list of minima)."""
    list_of_dataframes = a
    selected_index = b
    
    ##### Getting highest value out of all dataframes in the list
    list_of_max_values = []
    list_of_min_values = []
    
    for i in range(0, len(list_of_dataframes)):
        column_name = list_of_dataframes[i].columns[selected_index]
        
        max_value = list_of_dataframes[i][column_name].max()
        list_of_max_values.append(max_value)
        min_value = list_of_dataframes[i][column_name].min()
        list_of_min_values.append(min_value)
    
    return list_of_max_values, list_of_min_values


def Extract_List_Of_DataSeries_From_List_Of_Dataframes(a, b):
    """One column out of every dataframe of a list (the column must be in every dataframe).
    a = list of dataframes, b = column name. Returns a list of series."""
    ### The extracted Column Name has to be present in every Dataframe
    
    ### Define Parameters
    list_of_dataframes = a
    name_of_extracted_column = b
    
    ### Define Empty List for the output
    list_of_DataSeries = []
    
    ### Extract the Columns
    for i in range(len(list_of_dataframes)):
        DataSerie = list_of_dataframes[i][name_of_extracted_column]
        list_of_DataSeries.append(DataSerie)
    
    return list_of_DataSeries


def Extract_List_Of_DataSeries_From_List_Of_Dataframes_And_Normalize(a, b, c):
    """Like Extract_List_Of_DataSeries_From_List_Of_Dataframes, but every series is divided by a second column of the same dataframe.
    a = list of dataframes, b = column name, c = column name used for the normalisation (e.g. total counts).
    Returns a list of normalised series."""
    ### Define Parameters
    list_of_dataframes = a
    name_of_extracted_column = b
    name_of_column_for_normalization = c
    
    List_of_DataSeries = Extract_List_Of_DataSeries_From_List_Of_Dataframes(list_of_dataframes, name_of_extracted_column)
    
    for j in range(len(List_of_DataSeries)):
        List_of_DataSeries[j] = List_of_DataSeries[j]/list_of_dataframes[j][name_of_column_for_normalization]
        
    return List_of_DataSeries


def Round_Down_To_Odd(f):
    """Odd number below f: np.ceil(f) // 2 * 2 - 1 (e.g. 10.2 -> 9, 12 -> 11, 11 -> 9).
    Used for the window length of the Savitzky-Golay filter, which must be odd."""
    return np.ceil(f) // 2 * 2 - 1


def Normalize_Column_To_Reference_Column(a, b, c):
    """Divides one column by a reference column (e.g. ion counts / total counts) and adds the result as a new column.
    a = dataframe, b = column name, c = name of the reference column.
    Returns (dataframe, name of the new column '<b>_normalized_to_<c>')."""
    dataframe = a
    column_name1 = b
    column_name2 = c
    
    new_column_name = column_name1 + '_normalized_to_' + column_name2
    
    dataframe[new_column_name] = dataframe[column_name1] / dataframe[column_name2]
    
    return dataframe, new_column_name


def Find_First_NaN_Sequence_Start(df, column_name):
    """Position (row number, not index label) from which all remaining values of the column are NaN.
    df = dataframe, column_name = column. Returns -1 if the column does not end with NaN."""
    # Go through the series of the column
    for index in range(len(df[column_name])):
        # If all values from this point on are NaN, return the index
        if df[column_name].iloc[index:].isna().all():
            return index
    return -1


def Add_Columns_To_Dataframe(dataframe, dictionary_of_new_columns):
    """Adds many columns with one value each (in row 0) at once; existing columns with the same name are replaced.
    dataframe = dataframe, dictionary_of_new_columns = {column name: value}. Returns the new dataframe."""
    ########## Add many new columns (one value each, in row 0) at once ##########
    # adding the columns one by one with dataframe.loc[0, column_name] = value fragments the dataframe (PerformanceWarning)
    # columns which already exist are replaced by the new values
    dataframe_of_new_columns = pd.DataFrame(dictionary_of_new_columns, index=[0])
    dataframe = dataframe.drop(columns=[k for k in dictionary_of_new_columns if k in dataframe.columns])
    dataframe = pd.concat([dataframe, dataframe_of_new_columns], axis=1)
    return dataframe
