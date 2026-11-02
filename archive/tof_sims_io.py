"""Unused functions moved here from `scientific_utils/tof_sims/io.py` (nothing in the repository called them)."""

import numpy as np
import os
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.io import Find_Start_Row_Of_Data
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Read_SurfaceLab_SputterProfil(a, b, c , d, e, f):
    """Reads SurfaceLab sputter profiles (whitespace separated, starting at the row that begins with d, the first two rows dropped).
    a = folder, b = filter strings, c = file format, d = start string, e = separator (not used), f = decimal sign.
    Note: uses error_bad_lines, which pandas >= 2 does not know any more. Returns (list of dataframes, file names)."""
    ### This Function Reads the Area Lists given by SurfaceLab and transforms them into a Dataframe
    
    ### Define Variables ###
    path = a 
    FilterByNameList = b 
    FileFormat = c  
    StartString_of_the_wanted_Row= d 
    seperation_of_the_values = e 
    decimal_sign = f

    ### Select the files in the given directory by name and file format (scientific_utils.general.io) ###
    list_of_Measurements = Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat)
     
    ### Find the row at which the file will start to be red
    # define an empty list for the dataframes of the different measurements
    data_complete = []     
    
    for i in range(len(list_of_Measurements)):
        # find the row at which the data of the i-th file starts (scientific_utils.general.io)
        row_count = Find_Start_Row_Of_Data(os.path.join(path, list_of_Measurements[i]), StartString_of_the_wanted_Row)
        print('------------------------------------------')
        print('reading files beginning at row %s' %(row_count))
        print('------------------------------------------')
        
        ### read the file with pandas starting from the row count ###
        #file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object)
        
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object, sep=r'\s+', error_bad_lines=False)
        
        #file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=np.float64, sep=r'\s+', error_bad_lines=False)
        
        print(file.index)
        
        # Using iloc[] to drop first n rows
        file = file.iloc[2:]
        
        # change the commas in the columns to dots
        file = file.apply(lambda x: x.str.replace(',','.'))
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        file = Convert_DataframeColumns_To_Float32(file)
        
        # save the dataframe in a list
        data_complete.append(file)
    
    return data_complete, list_of_Measurements
