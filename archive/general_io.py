"""Unused functions moved here from `scientific_utils/general/io.py` (nothing in the repository called them)."""

from datetime import datetime
import numpy as np
import os
import pandas as pd
import pickle


def Extract_FilePaths_Advanced(a, b, c, d):
    """Like Extract_FilePaths, but files whose name contains a second string are left out.
    a = folder to search, b = string in the file name, c = string that must NOT be in the file name, d = file format.
    Returns the list of full file paths."""
    path_for_searching = a
    filter_string = b
    filter_string_not_in = c
    file_format = d
    
    list_of_file_paths = []
    
    for root, dirs, files in os.walk(path_for_searching):
        for file in files:
             if filter_string in file and file.endswith(file_format) and filter_string_not_in not in file:
                print("Found File!")
                found_path = os.path.join(root, file)
                found_path = r'{}'.format(found_path)
                list_of_file_paths.append(found_path)
    
    return list_of_file_paths


def Log_Last_Used_Notebook(a):
    """Appends date, time and the folder of the running notebook to a log file.
    a = path of the log file (created if it does not exist)."""
    # define parameters
    path_notebook_log_file = a
    
    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get the current file path of the Jupyter notebook
    current_notebook = os.path.abspath('')

    # Create the log entry
    log_entry = f"{current_datetime} - Last used notebook: {current_notebook}\n"

    # Write the log entry into the log file
    with open(path_notebook_log_file, 'a') as file:
        file.write(log_entry)


def Read_PklFiles_Via_FilePath(a):
    """Loads pickle (.pkl) files.
    a = list of file paths.
    Returns (list of the loaded objects, list of file names; the name is the part of the path after a 'saved_data' folder, Windows paths only)."""
    #### Parameter definieren
    list_of_file_paths = a
    
    ########## Path of the folder with the measurement files ##########
    print('-------------------')
    print('The following Path is selected:')
    for i in range(len(list_of_file_paths)):
        print(list_of_file_paths[i])
    print('-------------------')
    
    # define an empty list for the dataframes of the different measurements
    data_complete = [] 
    data_filenames = []
    
    for i in range(len(list_of_file_paths)):
        with open(list_of_file_paths[i], 'rb') as f:
            pkl_data = pickle.load(f)    
            data_complete.append(pkl_data)
        
        print('reading file %s complete' %(i+1))
        
        # extract file name from path
        file_path = list_of_file_paths[i]
        filter_start = '\\saved_data\\'
        filter_end ='.pkl'
        substring_result = file_path[file_path.find(filter_start)+len(filter_start):file_path.rfind(filter_end)]
        print('Extracted Filename:', substring_result)
        print('------------------------------------------')
        
        # save name of the file
        data_filenames.append(substring_result)
        
    return data_complete, data_filenames
