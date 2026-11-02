"""Finding, reading and logging files."""

from datetime import datetime
import numpy as np
import os
import pandas as pd
import pickle


def Extract_FilePaths(a, b, c):
    """Finds all files below a folder (also in subfolders) whose name contains a string and ends with a file format.
    a = folder to search, b = string in the file name, c = file format (e.g. '.txt').
    Returns the list of full file paths."""
    path_for_searching = a
    filter_string = b
    file_format = c
    
    list_of_file_paths = []
    
    print('Path for searching: ', path_for_searching)
    
    for root, dirs, files in os.walk(path_for_searching):
        #print('root;', root)
        #print('dirs;', dirs)
        #print('files;', files)
        for file in files:
            #print(file)
            if filter_string in file and file.endswith(file_format):
                print("Found File!")
                found_path = os.path.join(root, file)
                found_path = r'{}'.format(found_path)
                list_of_file_paths.append(found_path)
    
    return list_of_file_paths


def Read_Files_Via_FilePath(a, b, c, d):
    """Reads text files into dataframes (float64), starting at the first row that begins with a given string.
    a = list of file paths, b = start string of the table row, c = column separator, d = decimal sign.
    Returns (list of dataframes, list of file names; the name is the part of the path after a 'saved_data' folder, Windows paths only)."""
    #### Parameter definieren
    list_of_file_paths = a
    StartString_of_the_wanted_Row = b
    seperation_of_the_values = c
    decimal_sign = d
    
    ########## Path of the folder with the measurement files ##########
    print('-------------------')
    print('The following Path is selected:')
    for i in range(len(list_of_file_paths)):
        print(list_of_file_paths[i])
    print('-------------------')
    
    ######### Pandas Read Options
    print('Beginning reading at the String:', StartString_of_the_wanted_Row)
    print('Column Separation sign:', seperation_of_the_values)
    print('Decimal Sign:', decimal_sign)
    print('-------------------')
          
    ########## read the files ##########
    # define an empty list for the dataframes of the different measurements
    data_complete = [] 
    data_filenames = []
    
    for i in range(len(list_of_file_paths)):
        # row at which the table of the i-th file starts
        row_count = Find_Start_Row_Of_Data(list_of_file_paths[i], StartString_of_the_wanted_Row, encoding='UTF-8')
        print('------------------------------------------')
        print('reading files beginning at row %s' %(row_count))
        # read the file with pandas starting from the row count
        file = pd.read_csv(list_of_file_paths[i], sep=seperation_of_the_values, encoding='UTF-8', skiprows=row_count, decimal=decimal_sign, dtype=np.float64)
        # save the dataframe in a list
        data_complete.append(file)
        
        print('reading file %s complete' %(i+1))
        print('------------------------------------------')
        
        # extract file name from path
        file_path = list_of_file_paths[i]
        filter_start = '\\saved_data\\'
        filter_end ='.txt'
        substring_result = file_path[file_path.find(filter_start)+len(filter_start):file_path.rfind(filter_end)]
        print('Extracted Filename:', substring_result)
        
        # save name of the file
        data_filenames.append(substring_result)
        
    return data_complete, data_filenames


def Select_Files_By_Name_And_Format(path, FilterByNameList, FileFormat):
    """Lists the files in the folder `path` (no subfolders) whose name contains one of the strings in
    FilterByNameList and ends with FileFormat (e.g. '.TXT'). Returns the list of file names (sorted per filter string).
    Same code as before in the SurfaceLab, CasaXPS and XRD readers."""
    ### Looking for all files in the given directory ###
    dataframe_of_allfiles = pd.DataFrame(list(os.walk(path)))  # First column: directory/path ; second column: directories in the given directory/path ; third column: files in the given directory/path
                                                                  # os.walk('path') returns triples (dirpath, dirnames, files) -> list(os.walk('.')) puts these triples in a list
    list_of_filenames = []
    list_of_filenames = dataframe_of_allfiles[2][0]  # only lists the files in the selected directory
    
    print('-------------------')
    print('Following Files found in the chosen directory: %s', list_of_filenames)
    print('-------------------')
    
    list_of_selected_names = []
    
    list_of_Measurements = [] # define a empty list for all selected measurements
    
    ### Found Files filtern by strings in a list ###
    for i in range(0, len(FilterByNameList)):
        # only files with the selected names (in the List: FilterByNameList) are extracted from all the files in the selected directory
        list_of_selected_names = sorted([k for k in list_of_filenames if FilterByNameList[i] in k])
        # adds the selected file name to the list of files which will be plotted
        for n in range(0, len(list_of_selected_names)):
            print(list_of_Measurements)
            list_of_Measurements.append(list_of_selected_names[n])
    print('Files found:', list_of_Measurements)
    print('-------------------')

    ### Filter by file format ###
    for i in range(len(list_of_Measurements)):
        list_of_Measurements = [i for i in list_of_Measurements if i.endswith(FileFormat)]
    
    print('In total %s files are selected. \nThe name of the files are: \n%s' %(len(list_of_Measurements), list_of_Measurements))
    print('-------------------')
    
    return list_of_Measurements


def Find_Start_Row_Of_Data(file_path, StartString_of_the_wanted_Row, encoding='unicode_escape'):
    """Returns the number of the first row of the text file that starts with StartString_of_the_wanted_Row
    (= number of rows to skip with pd.read_csv(skiprows=...)). Used by all readers that search for the start of the table.
    encoding = the same encoding as in pd.read_csv of the file ('unicode_escape' turns a written '\\n' in the header into a new row)."""
    # start a row count for the file
    row_count = -1
    # open the file
    with open(file_path, 'r', encoding=encoding) as infile:
        # iterate through the row of the file
        for line in infile:
            # add +1 for every row in the file
            row_count += 1
            # stop the for loop when the row starts with the defined string
            if line.startswith(StartString_of_the_wanted_Row):
                break
    
    return row_count
