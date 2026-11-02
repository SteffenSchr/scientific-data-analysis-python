"""Unused functions moved here from `scientific_utils/tof_sims/analysis.py` (nothing in the repository called them)."""

import numpy as np
import pandas as pd


def Transfer_Multiple_Dataframes_To_One_Dataframe(a, b, c, d):
    """Takes one row (after transposing) of every dataframe and puts them together into one dataframe.
    a = list of dataframes (changed), b = column number used as new column names, c = text added in front of the column names,
    d = number (1, 2, ...) of the row that is taken from every dataframe. Returns the new dataframe."""
    ### This Funtion .....
    
    list_of_dataframes = a
    column_number_to_column_names = b
    addition_to_column_name = c
    column_number_as_transferred_data = d

    ### Change the Indizes of the Dataframe
    for i in range(len(list_of_dataframes)):
        print('Name of Column which is transformed to Index for Dataframe ', i , ' : ', list_of_dataframes[i].columns[column_number_to_column_names])
        list_of_dataframes[i] = list_of_dataframes[i].set_index(list_of_dataframes[i].columns[column_number_to_column_names])
    
    ### Transpose Dataframe
    for i in range(len(list_of_dataframes)):
        list_of_dataframes[i] = list_of_dataframes[i].T
    
    ### Rename Column Names
    for j in range(len(list_of_dataframes)):
        list_of_new_column_names = []
        for i in range(len(list_of_dataframes[j].columns)):
            list_of_new_column_names.append(addition_to_column_name + list_of_dataframes[j].columns[i])
        list_of_dataframes[j].columns = list_of_new_column_names
    
    ### create list indizes of the datafr
    pandas_series_list = []
    for i in range(len(list_of_dataframes)):
        indizes_list = list(list_of_dataframes[i].index.values)
        column_index = column_number_as_transferred_data -1
        #print('Name of Column which data is transferred for Dataframe ', i , ' : ', list_of_dataframes[i].columns[column_index])
        series = list_of_dataframes[i].loc[indizes_list[column_index]]
        pandas_series_list.append(series)
    
    ### contact the pandas series into one dataframe and transpose
    data = pd.concat(pandas_series_list, axis=1).T
    
    return data


def Transform_ColumnBased_To_RowBased_Dataframe(a, b):
    """Transposes every dataframe of a list (column b becomes the column names) and drops the first and the last two rows.
    a = list of dataframes (changed), b = column number used as new column names. Returns the list."""
    # This Function transforms The Columns of an Dataframe to Rows. This is possible for multiple Dataframes fiven as a List as Input. The second Parameter b gives the Column by Index which should be the new Column Names.
    list_of_dataframes = a
    column_number_to_column_names = b

    ### Transform one column to the index of the dataframe
    for i in range(len(list_of_dataframes)):
        print('Name of Column which is transformed to Index for Dataframe ', i , ' : ', list_of_dataframes[i].columns[column_number_to_column_names])
        list_of_dataframes[i] = list_of_dataframes[i].set_index(list_of_dataframes[i].columns[column_number_to_column_names])
    
    ### transpose the dataframe --> Rows to columns and Columns to rows
    for i in range(len(list_of_dataframes)):
        list_of_dataframes[i] = list_of_dataframes[i].T
    
    ### Delete all unknown rows by indes name/number
    for j in range(len(list_of_dataframes)):
        list_of_dataframes[j] = list_of_dataframes[j].drop(list_of_dataframes[j].index[[0, -2, -1]])
    
    return list_of_dataframes
