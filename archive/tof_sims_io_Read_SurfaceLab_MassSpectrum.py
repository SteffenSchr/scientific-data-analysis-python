"""Archived copy of tof_sims/io.py:Read_SurfaceLab_MassSpectrum (same as Read_SurfaceLab_ColumnBased_AreaList without the 'Mass (u)' line)."""

import numpy as np
import os
import pandas as pd


def Read_SurfaceLab_MassSpectrum(a, b, c , d, e, f):
    ### This Function Reads the Area Lists given by SurfaceLab and transforms them into a Dataframe
    
    ### Define Variables ###
    path = a 
    FilterByNameList = b 
    FileFormat = c  
    StartString_of_the_wanted_Row= d 
    seperation_of_the_values = e 
    decimal_sign = f

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
     
    ### Find the row at which the file will start to be red
    # define an empty list for the dataframes of the different measurements
    data_complete = []     
    
    for i in range(len(list_of_Measurements)):
        # start a row count for the i-th file
        row_count = -1
        # open the i-th file in the list
        with open(os.path.join(path, list_of_Measurements[i]), 'r', encoding='unicode_escape') as infile:
            # iterate through the row of the file
            for line in infile:
                # add +1 for every row in the file
                row_count += 1
                # stop the for loop when the row starts with the defined string
                if line.startswith(StartString_of_the_wanted_Row):
                    break
        print('------------------------------------------')
        print('reading files beginning at row %s' %(row_count))
        print('------------------------------------------')
        
        ### read the file with pandas starting from the row count ###
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object)
        
        ### Clean the generated dataframe from unnecessary entries and change some parameters
        # change the commas in the columns to dots
        file = file.apply(lambda x: x.str.replace(',','.'))
        # Check if all columns have numeric values
        #bool_list = file.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
        bool_list = []
        for k in range(len(file.columns)):
            column = file.columns[k]
            bool_entry = pd.to_numeric(file[column], errors='coerce').notnull().all()
            bool_list.append(bool_entry)
        
        # changing the datatype of the columns from string to float
        for h in range(len(bool_list)):
            print(bool_list[h])
            if bool_list[h] == True:
                print(file.columns[h])
                file[file.columns[h]] = pd.to_numeric(file[file.columns[h]], downcast="float")
                print(file[file.columns[h]].dtypes)  
            else:
                pass
        
        # save the dataframe in a list
        data_complete.append(file)
        #print(data_complete[i])
    
    return data_complete

