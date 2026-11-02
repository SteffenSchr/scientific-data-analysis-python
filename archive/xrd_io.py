"""Unused functions moved here from `scientific_utils/xrd/io.py` (nothing in the repository called them)."""

import os
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.io import Find_Start_Row_Of_Data
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Read_XRD_Diffractogram_With_Header(a, b, c , d, e, f):
    """Reads diffractograms with a header: table from the row that begins with d, values converted with pd.to_numeric(errors='ignore')
    (deprecated in pandas 2.2). a = folder, b = filter strings, c = file format, d = start string, e = separator, f = decimal sign.
    Returns the list of dataframes."""
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
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object)
        
        ### Transform obejct in the dataframe to numeric values
        file = file.apply(pd.to_numeric, errors='ignore')#.info()
        
        data_complete.append(file)
        
    return data_complete
