"""Unused functions moved here from `scientific_utils/xps/io.py` (nothing in the repository called them)."""

import numpy as np
import os
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.io import Find_Start_Row_Of_Data
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Read_XPS_Files(input_parameters):
    """Reads XPS text exports (UTF-8, float64), starting at the row that begins with the start string.
    input_parameters = dictionary with 'path', 'FilterByNameList', 'FileFormat', 'StartString_of_the_wanted_Row',
    'seperation_of_the_values', 'decimal_sign' (defaults if missing). Returns the list of dataframes."""
########## Path of the folder with the measurement files ##########
    path = input_parameters.get('path', './data/raw')
    print(path)
    print('-------------------')
    print('The following Path is selected:', path)
    print('-------------------')
    
    FilterByNameList = input_parameters.get('FilterByNameList', [''])
    FileFormat = input_parameters.get('FileFormat', '')
    ### Select the files in the given directory by name and file format (scientific_utils.general.io) ###
    list_of_Measurements = Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat)
    

    StartString_of_the_wanted_Row = input_parameters.get('StartString_of_the_wanted_Row', '')
    seperation_of_the_values = input_parameters.get('seperation_of_the_values', '	')
    decimal_sign = input_parameters.get('decimal_sign', '.')
    print('-------------------')
    print('Beginning reading at the String:', StartString_of_the_wanted_Row)
    print('Column Separation sign:', seperation_of_the_values)
    print('Decimal Sign:', decimal_sign)
    print('-------------------')
    ########## read the files ##########
    # define an empty list for the dataframes of the different measurements
    data_complete = [] 
    
    for i in range(len(list_of_Measurements)):
        # start a row count for the i-th file
        row_count = -1
        # open the i-th file in the list
        with open(os.path.join(path, list_of_Measurements[i]), 'r', encoding='UTF-8') as infile:
            #infile = infile.readlines()[1:]
            # iterate through the row of the file
            for line in infile:
                # add +1 for every row in the file
                row_count += 1
                print(row_count)
                # stop the for loop when the row starts with the defined string
                if line.startswith(StartString_of_the_wanted_Row):
                    break
        print('------------------------------------------')
        print('reading files beginning at row %s' %(row_count))
        # read the file with pandas starting from the row count
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='UTF-8', skiprows=row_count, decimal=decimal_sign, dtype=np.float64)
        # save the dataframe in a list
        data_complete.append(file)
        print('reading file %s complete' %(i+1))
        print('------------------------------------------')
    
    #print('------------------------------------------')
    #print('Extracted Data From Files: %s' %(data_complete))
    #print('------------------------------------------')
        
    return data_complete
