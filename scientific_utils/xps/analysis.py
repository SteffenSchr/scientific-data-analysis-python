"""Extracting detail spectra and peak areas from XPS data."""

from scipy import interpolate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import scipy
import scipy.signal

from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32
from scientific_utils.general.analysis import Round_Down_To_Odd


def Extract_XPS_DetailSpectra_From_Multiple_Scans(a, b):
    """Splits a CasaXPS export with several scans into blocks (a block ends at an 'Unnamed' column)
    and keeps the blocks whose column names contain b; empty rows dropped, number columns -> float.
    a = dataframe of the export, b = string of the region. Returns the list of dataframes."""
    
    # Define Parameters
    dataframe = a
    string_filter = b
    
    
    # get boolean array where all entries are true which contain the substring
    array = dataframe.columns.str.contains('Unname')

    # Get which indices are True in the boolean array
    indices = np.where(array)

    # transfrom the tuple into a list
    indices = list(indices[0])

    # Extract the Subdataframes based on the extracted indices via the column names
    list_of_subdataframes = []

    for i in range(len(indices)):
        if i == 0:
            column_names = dataframe.columns[:indices[i]+1]
            df_extracted = dataframe[column_names]
            list_of_subdataframes.append(df_extracted)
        elif i != 0 and i < len(indices):
            column_names = dataframe.columns[indices[i-1]+1:indices[i]+1]
            df_extracted = dataframe[column_names]
            list_of_subdataframes.append(df_extracted)
        elif i == len(indices):
            column_names = dataframe.columns[indices[i-1]+1:]
            df_extracted = dataframe[column_names]
            list_of_subdataframes.append(df_extracted)

    # Extract from the list of dataframes all indices where the column names of the dataframe contain a certain substring
    boolean_list = []

    for i in range(len(list_of_subdataframes)):
        if any(list_of_subdataframes[i].columns.str.contains(string_filter)) == True:
            boolean_list.append(i)
        
    extracted_dataframes = [list_of_subdataframes[i] for i in boolean_list]
    
    for i in range(len(extracted_dataframes)):
        # Remove all columns without a value
        extracted_dataframes[i] = extracted_dataframes[i].dropna(how='all')

        # Change Datatype of the Columns to Float32 for Plotting
        a = dataframe = extracted_dataframes[i]

        extracted_dataframes[i] = Convert_DataframeColumns_To_Float32(a)
        
    return extracted_dataframes


def Extract_Sputter_Time_From_Name(sample_name):
    """First number in a sample name as float (e.g. '600 s sputtered' -> 600.0; note: 'NCM831205_600s' -> 831205.0), 0.0 if there is none."""
    # Pattern searches for numbers (\d+)
    match = re.search(r'(\d+)', str(sample_name))
    if match:
        return float(match.group(1))
    else:
        return 0.0

