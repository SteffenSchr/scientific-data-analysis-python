"""Reading the exports of IONTOF SurfaceLab (mass spectra, depth profiles, area lists)."""

import numpy as np
import os
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.io import Find_Start_Row_Of_Data
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Read_SurfaceLab_DepthProfil_Separate_Header(a, b, c , d):
    """Reads SurfaceLab depth profile exports whose column names are split over two header lines (lines 2 and 3; lines 1 and 4 are skipped).
    a = folder, b = list of filter strings for the file names, c = file format, d = column separator.
    Returns (list of dataframes with numbered columns, file names, header line 2, header line 3 of the last file)."""
    ### This Function Reads the Area Lists given by SurfaceLab and transforms them into a Dataframe
    
    ### Define Variables ###
    path = a 
    FilterByNameList = b 
    FileFormat = c
    seperation_of_the_values = d 

    ### Select the files in the given directory by name and file format (scientific_utils.general.io) ###
    list_of_Measurements = Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat)
     
    ### Find the row at which the file will start to be red
    # define an empty list for the dataframes of the different measurements
    data_complete = []     
    
    for i in range(len(list_of_Measurements)):
        # Specify the file path
        file_path = os.path.join(path, list_of_Measurements[i])

        # Initialize an empty list to store the data
        lines_in_file = []

        # Initialize a variable to keep track of the line number
        line_number = -1

        # Initialize two empty lists to store column names
        column_names = []
        column_names2 = []

        # Specify the delimiter you want to use (e.g., comma or semicolon or tab)
        delimiter = seperation_of_the_values  # Change this to the desired delimiter

        # Read the file line by line, skipping lines 2 and 4
        with open(file_path, 'r') as file:
            for line in file:
                line_number += 1
                # Skip lines 0 and 2
                if line_number == 0 or line_number == 3:
                    continue 
                # Store line 1 as first part of column names
                elif line_number == 1:
                    # remove withe space between entries and split it with defined delimter
                    column_names.extend(line.strip().split(delimiter))
                    #print(line.strip().split(delimiter))
                elif line_number == 2:
                    # remove withe space between entries and split it with defined delimter
                    column_names2.extend(line.strip().split(delimiter))
                    #print(line.strip().split(delimiter))
                elif line_number == 15:
                    # remove withe space between entries and split it with defined delimter
                    row = line.strip().split(delimiter)
                    lines_in_file.append(row)
                    print(row)
                else:
                    # remove withe space between entries and split it with defined delimter
                    row = line.strip().split(delimiter)
                    lines_in_file.append(row)

        # If column_names is shorter than column_names2, it is mostly because the last mass in the SurfaceLab area list has no fragment assigned, so the last entry of the fragment columns is missing
        if len(column_names) == len(column_names2)-1:
            column_names.append('')
        #print(len(column_names))
        #print(len(column_names2))

        # Create a DataFrame from the collected data with the custom column names
        data = pd.DataFrame(lines_in_file)
        #print(data)
        
        # change the commas in the columns to dots
        data = data.apply(lambda x: x.str.replace(',','.'))
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        data = Convert_DataframeColumns_To_Float32(data)
        
        data_complete.append(data)
    
    return data_complete, list_of_Measurements, column_names, column_names2


def Read_SurfaceLab_DepthProfil_Combined_Header(a, b, c , d):
    """Reads SurfaceLab depth profile exports and builds the column names from header lines 2 and 4 (joined; shifted by one entry if the lines differ in length).
    a = folder, b = list of filter strings, c = file format, d = column separator. Returns (list of dataframes, file names)."""
    ### This Function Reads the Area Lists given by SurfaceLab and transforms them into a Dataframe
   
    ### Define Variables ###
    path = a 
    FilterByNameList = b 
    FileFormat = c  
    seperation_of_the_values = d 

    ### Select the files in the given directory by name and file format (scientific_utils.general.io) ###
    list_of_Measurements = Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat)
    
    ### Find the row at which the file will start to be red
    # define an empty list for the dataframes of the different measurements
    data_complete = []     
   
    for i in range(len(list_of_Measurements)):
        # Specify the file path
        file_path = os.path.join(path, list_of_Measurements[i])

        # Initialize an empty list to store the data
        lines_in_file = []

        # Initialize a variable to keep track of the line number
        line_number = -1

        # Initialize two empty lists to store column names
        column_names1 = []
        column_names2 = []

        # Specify the delimiter you want to use (e.g., comma or semicolon or tab)
        delimiter = seperation_of_the_values  # Change this to the desired delimiter

        # Read the file line by line, skipping lines 2 and 4
        with open(file_path, 'r') as file:
            for line in file:
                line_number += 1
                # Skip lines 0 and 2
                if line_number == 0 or line_number == 2:
                    continue 
                # Store line 1 as first part of column names
                elif line_number == 1:
                    # remove withe space between entries and split it with defined delimter
                    column_names1.extend(line.strip().split(delimiter))
                    print(line.strip().split(delimiter))
                # Store line 3 as first part of column names
                elif line_number == 3:
                    # remove withe space between entries and split it with defined delimter
                    column_names2.extend(line.strip().split(delimiter))
                    print(line.strip().split(delimiter))
                elif line_number == 15:
                    # remove withe space between entries and split it with defined delimter
                    row = line.strip().split(delimiter)
                    lines_in_file.append(row)
                    print(row)
                else:
                    # remove withe space between entries and split it with defined delimter
                    row = line.strip().split(delimiter)
                    lines_in_file.append(row)

        print(len(column_names1))
        print(len(column_names2))
                   
        if len(column_names1) == len(column_names2):
            # combine both list to one list
            column_names_combined = [str(item1) + str(item2) for item1, item2 in zip(column_names1, column_names2)]
            # Create a DataFrame from the collected data with the custom column names
            data = pd.DataFrame(lines_in_file, columns=column_names_combined)
        else:
            # add emtpy entrie to first column name list
            column_names1.append('')
       
            # loop reversed through the column names of list 1
            for i in reversed(range(len(column_names1))):
                # skip last line
                if i == len(column_names1)-1:
                    continue
                # skip lines smaller than 2
                elif i <= 2: 
                    continue
                # add all other list entries to the index +1 greater
                else:
                    column_names1[i+1] = column_names1[i] + column_names1[i+1]

            # combine both list to one list
            column_names_combined = [str(item1) + str(item2) for item1, item2 in zip(column_names1, column_names2)]
            print(column_names_combined)
           
            # Create a DataFrame from the collected data with the custom column names
            data = pd.DataFrame(lines_in_file, columns=column_names_combined)
       
        # change the commas in the columns to dots
        data = data.apply(lambda x: x.str.replace(',','.'))
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        data = Convert_DataframeColumns_To_Float32(data)
       
        data_complete.append(data)
   
    return data_complete, list_of_Measurements


def Read_SurfaceLab_ColumnBased_AreaList(a, b, c , d, e, f):
    """Reads SurfaceLab area lists with one column per measurement (commas -> dots, number columns -> float; the last 'Mass (u)' entry is set to 0).
    a = folder, b = filter strings, c = file format, d = start string of the table row, e = separator, f = decimal sign. Returns the list of dataframes."""
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
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object)
        
        ### Clean the generated dataframe from unnecessary entries and change some parameters
        # change the las colum entry to a string value
        file.loc[file.index[-1], 'Mass (u)'] = "0,00"
        #file.loc[file.index[-1], 'Mean'] = file[file.columns[2]].iloc[-1]
        
        # change the commas in the columns to dots
        file = file.apply(lambda x: x.str.replace(',','.'))
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        file = Convert_DataframeColumns_To_Float32(file)
        
        # save the dataframe in a list
        data_complete.append(file)
        #print(data_complete[i])
    
    return data_complete


def Read_SurfaceLab_RowBased_AreaList(a, b, c , d, e, f):
    """Reads SurfaceLab area lists with one row per measurement (commas -> dots, number columns -> float).
    a = folder, b = filter strings, c = file format, d = start string of the table row, e = separator, f = decimal sign. Returns the list of dataframes."""
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
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object)
        
        # change the commas in the columns to dots
        file = file.apply(lambda x: x.str.replace(',','.'))
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        file = Convert_DataframeColumns_To_Float32(file)
        
        # save the dataframe in a list
        data_complete.append(file)
        #print(data_complete[i])
    
    return data_complete


def Read_SputterProfile_Files(parameters_ReadSputterProfileFile):
    """Reads sputter profile text files (float64), starting at the row that begins with the start string.
    parameters_ReadSputterProfileFile = dictionary with 'path', 'FileNameFilter', 'FileFormat', 'StartStringData', 'ColumnSeperationSign', 'DecimalSign'.
    Returns the list of dataframes."""
########## Path of the folder with the measurement files ##########
    path = parameters_ReadSputterProfileFile.get('path')
    print('-------------------')
    print('The following Path is selected:', path)
    print('-------------------')
    
    FilterByNameList = parameters_ReadSputterProfileFile.get('FileNameFilter')
    FileFormat = parameters_ReadSputterProfileFile.get('FileFormat')
    ### Select the files in the given directory by name and file format (scientific_utils.general.io) ###
    list_of_Measurements = Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat)
    

    StartString_of_the_wanted_Row = parameters_ReadSputterProfileFile.get('StartStringData')
    seperation_of_the_values = parameters_ReadSputterProfileFile.get('ColumnSeperationSign')
    decimal_sign = parameters_ReadSputterProfileFile.get('DecimalSign')
    print('-------------------')
    print('Beginning reading at the String:', StartString_of_the_wanted_Row)
    print('Column Separation sign:', seperation_of_the_values)
    print('Decimal Sign:', decimal_sign)
    print('-------------------')
    ########## read the files ##########
    # define an empty list for the dataframes of the different measurements
    data_complete = [] 
    
    for i in range(len(list_of_Measurements)):
        # row at which the table of the i-th file starts (scientific_utils.general.io)
        row_count = Find_Start_Row_Of_Data(os.path.join(path, list_of_Measurements[i]), StartString_of_the_wanted_Row, encoding='UTF-8')
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


def Read_PeakList_Files(input_parameters):
    """Reads SurfaceLab peak lists (last row: 'Mass (u)' = 0, 'Mean' = third column).
    input_parameters = dictionary with 'path', 'FilterByNameList', 'FileFormat', 'StartString_of_the_wanted_Row',
    'seperation_of_the_values' (default tab) and 'decimal_sign' (default ',') (defaults if missing).
    Returns the list of dataframes."""
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
    seperation_of_the_values = input_parameters.get('seperation_of_the_values', '\t')
    decimal_sign = input_parameters.get('decimal_sign', ',')
    print('-------------------')
    print('Beginning reading at the String:', StartString_of_the_wanted_Row)
    print('Column Separation sign:', seperation_of_the_values)
    print('Decimal Sign:', decimal_sign)
    print('-------------------')
    # define an empty list for the dataframes of the different measurements
    data_complete = []     
    
    for i in range(len(list_of_Measurements)):
        # row at which the table of the i-th file starts (scientific_utils.general.io)
        row_count = Find_Start_Row_Of_Data(os.path.join(path, list_of_Measurements[i]), StartString_of_the_wanted_Row)
        print('------------------------------------------')
        print('reading files beginning at row %s' %(row_count))
        print('------------------------------------------')
        # read the file with pandas starting from the row count
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object)
        # change the las colum entry to a string value
        file.loc[file.index[-1], 'Mass (u)'] = "0,00"
        file.loc[file.index[-1], 'Mean'] = file[file.columns[2]].iloc[-1]
        
        # change the commas in the columns to dots
        file = file.apply(lambda x: x.str.replace(',','.'))
        # Check if all columns have numeric values and change them from string to float (scientific_utils.general.analysis)
        file = Convert_DataframeColumns_To_Float32(file)
        
        # save the dataframe in a list
        data_complete.append(file)
        #print(data_complete[i])
    
    
    return data_complete
