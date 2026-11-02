"""Unused functions moved here from `scientific_utils/battery/io.py` (nothing in the repository called them)."""

import os
import numpy as np
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Rename_Biologic_Columns_To_Maccor_Names(dataframe, step_type):
    """Renames the columns of a Biologic dataframe to the Maccor names ('TestTime (seconds)', 'Current (mA)', 'Capacity (mAh)', 'Voltage (V)', ...).
    dataframe, step_type = 'CP charge', 'CP discharge' or 'OCV'. Returns the dataframe."""
    ########## Rename the columns of a Biologic dataframe to match them with the names of the Maccor files ##########
    # step_type: 'CP charge', 'CP discharge' or 'OCV'
    # Columns in the Maccor file = [Rec#, Cyc#, Step, TestTime (seconds), StepTime (seconds), Capacity (mAh), Current (mA), Voltage (V), ACR]
    if step_type == 'CP charge':
        dataframe.columns = ['mode', 'ox/red', 'error', 'control changes', 'Ns changes', 'counter inc.', 'Ns', 'TestTime (seconds)', 'control/mA', '<Ewe>/V', 'Current (mA)', 'dQ/C', '(Q-Qo)/C', 'half cycle', 'Q charge/discharge/mA.h', 'I Range', '<Ece>/V', 'Energy charge/W.h', 'Energy discharge/W.h', 'Capacitance charge/µF', 'Capacitance discharge/µF', 'Q discharge/mA.h', 'Capacity (mAh)', 'Capacity/mA.h', 'Efficiency/%', 'cycle number', 'P/W', 'Voltage (V)', '']
    elif step_type == 'CP discharge':
        dataframe.columns = ['mode', 'ox/red', 'error', 'control changes', 'Ns changes', 'counter inc.', 'Ns', 'TestTime (seconds)', 'control/mA', '<Ewe>/V', 'Current (mA)', 'dQ/C', '(Q-Qo)/C', 'half cycle', 'Q charge/discharge/mA.h', 'I Range', '<Ece>/V', 'Energy charge/W.h', 'Energy discharge/W.h', 'Capacitance charge/µF', 'Capacitance discharge/µF', 'Capacity (mAh)', 'Q charge/mA.h', 'Capacity/mA.h', 'Efficiency/%', 'cycle number', 'P/W', 'Voltage (V)', '']
    elif step_type == 'OCV':
        dataframe.columns = ['mode', 'error', 'TestTime (seconds)', 'Ewe/V', 'Ece/V', 'Voltage (V)', '']
    return dataframe


def Reset_Capacity_To_Zero(list_of_dataframes):
    """Sets 'Capacity (mAh)' of every step back to zero at its start (changed in place).
    list_of_dataframes = list of step dataframes. Returns the list."""
    ########## Set the capacity back to zero for every cycle ##########
    for i in range(0, len(list_of_dataframes)):
        list_of_dataframes[i]['Capacity (mAh)'] = list_of_dataframes[i]['Capacity (mAh)'] - list_of_dataframes[i].iloc[0]['Capacity (mAh)']
    return list_of_dataframes


def Synchronize_OCV_With_Cycling_Data(cycling_dataframe, ocv_dataframe):
    """Synchronises two Maccor channels that were started at different times (cycling WE-RE and OCV CE-RE).
    The start of the cycling (jump of the potential) is found in both and the OCV data is shifted and cut to the same length.
    cycling_dataframe, ocv_dataframe = dataframes with 'Voltage (V)' and 'TestTime (seconds)' (time in s).
    Returns (cycling dataframe, OCV dataframe), both with the test time starting at 0 s."""
    ########## Synchronise two Maccor channels (cycling WE-RE and OCV CE-RE) which were started at different times ##########
    # the change of the potential shows when the cycling starts (overpotential) -> the index of this change is extracted in both dataframes

    # OCV
    cycling_data_OCV = Split_Dataframe_At_Jumps(ocv_dataframe, 'Voltage (V)', -0.01)
    OCV_index = cycling_data_OCV[1].index

    # Cycling
    cycling_data = Split_Dataframe_At_Jumps(cycling_dataframe, 'Voltage (V)', 0.1)
    Cycling_index = cycling_data[1].index

    # Difference in indexes
    index_difference = (OCV_index[0] - Cycling_index[0]) + 1

    # Synchronise both dataframes with the extracted index difference
    ocv_dataframe = ocv_dataframe.iloc[index_difference:] # Creates a new dataframe without the first rows of the previous dataframe
    ocv_dataframe = ocv_dataframe.reset_index() # reset the indexes
    ocv_dataframe['TestTime (seconds)'] = ocv_dataframe['TestTime (seconds)'] - ocv_dataframe.iloc[0]['TestTime (seconds)'] # Correct the time offset

    length_cycling_data = len(cycling_dataframe['Voltage (V)'])
    ocv_dataframe = ocv_dataframe.iloc[:length_cycling_data] # The OCV dataframe is cut to the length of the cycling dataframe

    cycling_dataframe['TestTime (seconds)'] = cycling_dataframe['TestTime (seconds)'] - cycling_dataframe.iloc[0]['TestTime (seconds)'] # Correct the time offset

    return cycling_dataframe, ocv_dataframe


def Read_Maccor_Txt_Files_And_Filenames(a, b, c, d, e, f):
    """Reads all files of a folder whose name contains one of the filter strings and ends with the file format.
    a = folder, b = list of filter strings, c = file format, d = start string of the table row, e = column separator, f = decimal sign.
    Number columns are converted to float. Returns (list of dataframes, list of file names)."""
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
        #file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='UTF-8', skiprows=row_count, decimal=decimal_sign, dtype=np.float64)
        file = pd.read_csv(os.path.join(path, list_of_Measurements[i]), sep=seperation_of_the_values, encoding='unicode_escape', skiprows=row_count, decimal=decimal_sign, dtype=object)
        
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
