"""Reading XRD diffractograms."""

import os
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.io import Find_Start_Row_Of_Data
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Read_XRD_XY_Diffractogram(a, b, c):
    """Reads .xy diffractograms: the column names are in line 7 (without its first two characters), lines 1-6 and 8 are skipped,
    the values are separated by whitespace; number columns -> float.
    a = folder, b = list of filter strings for the file names, c = file format (e.g. '.xy'). Returns (list of dataframes, file names)."""
    ### Define Variables ###
    path = a 
    FilterByNameList = b 
    FileFormat = c  

    ### Select the files in the given directory by name and file format (scientific_utils.general.io) ###
    list_of_Measurements = Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat)
     
    ### Find the row at which the file will start to be red
    # define an empty list for the dataframes of the different measurements
    data_complete = []     
    data_filenames = []
    
    for i in range(len(list_of_Measurements)):
        # Specify the file path
        file_path = os.path.join(path, list_of_Measurements[i])

        # Initialize an empty list to store the data
        lines_in_file = []

        # Initialize a variable to keep track of the line number
        line_number = -1

        # Initialize two empty lists to store column names
        column_names = []

        # Read the file line by line, skipping lines 2 and 4
        with open(file_path, 'r') as file:
            for line in file:
                line_number += 1
                # Skip lines 8 and smaller than 7
                if line_number == 7 or line_number < 6:
                    continue 
                # Store line 1 as first part of column names
                elif line_number == 6:
                    # remove withe space between entries and split it with defined delimter
                    column_names.extend(line[2:].strip().split())
                    print(column_names)
                else:
                    # remove withe space between entries and split it with defined delimter
                    row = line.strip().split()
                    lines_in_file.append(row)

        #print(len(column_names))
            
        # Create a DataFrame from the collected data with the custom column names
        data = pd.DataFrame(lines_in_file, columns=column_names)
        
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        data = Convert_DataframeColumns_To_Float32(data)
        
        data_complete.append(data)
        data_filenames.append(list_of_Measurements[i])
        
    return data_complete, data_filenames

