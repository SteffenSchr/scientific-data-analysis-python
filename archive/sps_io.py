"""Reading spark plasma sintering (SPS) exports.

Moved here from `scientific_utils/sps/io.py` (nothing in the repository called these functions)."""

import os
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Read_SPS_CSV_Files_And_Filenames(a, b, c, d, e, f):
    """Reads SPS (spark plasma sintering) csv exports (latin1): table from the row that begins with d, last three rows dropped,
    first column renamed to 'Time', second column dropped, number columns -> float.
    a = folder, b = list of filter strings, c = file format, d = start string, e = separator, f = decimal sign. Returns (list of dataframes, file names)."""
    ########## Define all Parameters
    path =  a
    FilterByNameList = b
    FileFormat = c
    StartString_of_the_wanted_Row = d
    seperation_of_the_values = e
    decimal_sign = f
    
    ### Select the files in the given directory by name and file format (scientific_utils.general.io) ###
    list_of_Measurements = Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat)
    
    print('-------------------')
    print('Beginning reading at the String:', StartString_of_the_wanted_Row)
    print('Column Separation sign:', seperation_of_the_values)
    print('Decimal Sign:', decimal_sign)
    print('-------------------')
    ########## read the files ##########
    # define an empty list for the dataframes of the different measurements
    data_complete = [] 
    data_filenames = []
    
    for i in range(len(list_of_Measurements)):
        # start a row count for the i-th file
        row_count = -1
        # open the i-th file in the list
        with open(os.path.join(path, list_of_Measurements[i]), 'r') as infile:
        #with open(os.path.join(path, list_of_Measurements[i]), 'r', encoding='HTML Escape') as infile:
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
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='latin1', skiprows=row_count, decimal=decimal_sign, dtype=object)
        
        # delete last three row
        file = file[:-3]
        
        # rename column 1 of the dataframe
        file.columns = file.columns.str.replace(file.columns[0], 'Time')

        # delete second column
        file = file.drop(file.columns[1], axis=1)
        
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        file = Convert_DataframeColumns_To_Float32(file)
        
        # save the dataframe in a list
        data_complete.append(file)
        # save name of the file
        data_filenames.append(list_of_Measurements[i])
        print('reading file %s complete' %(i+1))
        print('------------------------------------------')
    
    #print('------------------------------------------')
    #print('Extracted Data From Files: %s' %(data_complete))
    #print('------------------------------------------')
        
    return data_complete, data_filenames
