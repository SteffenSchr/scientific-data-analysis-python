"""Reading and splitting battery cycler exports (Maccor and Biologic)."""

import os
import numpy as np
import pandas as pd

from scientific_utils.general.io import Select_Files_By_Name_And_Format
from scientific_utils.general.io import Find_Start_Row_Of_Data
from scientific_utils.general.analysis import Convert_DataframeColumns_To_Float32


def Read_Biologic_Mpt_Files(path, list_of_files, decimal_sign):
    """Reads Biologic .mpt exports into dataframes (float64); the table starts at the row beginning with 'mode'.
    path = folder, list_of_files = file names, decimal_sign = '.' or ','. Returns the list of dataframes."""
    ########## Read the Biologic .mpt files into dataframes ##########
    # the header of a .mpt file has a different length for every technique -> the table starts at the row with "mode"
    list_of_dataframes = []
    for i in range(len(list_of_files)):
        # one row less than the row with "mode" (count started at -2 in the old loop)
        count = Find_Start_Row_Of_Data(os.path.join(path, list_of_files[i]), "mode") - 1
        file = pd.read_csv(os.path.join(path, list_of_files[i]), sep='\t', encoding='unicode_escape', skiprows=count, decimal=decimal_sign, dtype=np.float64)
        list_of_dataframes.append(file)
    print(len(list_of_dataframes))
    return list_of_dataframes


def Read_Maccor_Txt_Files(path, list_of_files):
    """Reads Maccor .txt exports into dataframes (float64); the table starts at the row beginning with 'Rec#'.
    path = folder, list_of_files = file names. Returns the list of dataframes."""
    ########## Read the Maccor .txt files into dataframes ##########
    # the table starts at the row with "Rec#"
    list_of_dataframes = []
    for i in range(len(list_of_files)):
        count = Find_Start_Row_Of_Data(os.path.join(path, list_of_files[i]), "Rec#")
        file = pd.read_csv(os.path.join(path, list_of_files[i]), sep='\t', encoding='unicode_escape', skiprows=count, decimal='.', dtype=np.float64)
        list_of_dataframes.append(file)
    return list_of_dataframes


def Split_Dataframe_At_Jumps(dataframe, column, jump):
    """Splits a dataframe into steps where the values of one column jump.
    dataframe, column = column name, jump = size of the jump in the unit of the column
    (> 0: new step when the value rises by more than jump, e.g. a time gap; < 0: when it falls, e.g. step time back to zero).
    Returns the list of dataframes."""
    ########## Split a dataframe into separate dataframes where the values in the column jump #########
    # jump > 0: a new dataframe starts when the value is bigger than the value of the row before plus jump (e.g. a time gap between two cycles)
    # jump < 0: a new dataframe starts when the value is smaller than the value of the row before plus jump (e.g. the step time starts again at zero)
    if jump > 0:
        step_groupcondition = (dataframe[column] > (dataframe[column].shift() + jump)).cumsum() # one is added at every jump, so every step gets its own number
    else:
        step_groupcondition = (dataframe[column] < (dataframe[column].shift() + jump)).cumsum()
    grouped_steps = dataframe.groupby(step_groupcondition)              # Groups the dataframe with the results from before: a new dataframe is created for every number in 'step_groupcondition'
    list_of_dataframes = [g for k,g in grouped_steps] # Put the separated steps in a list, so that every list entry is one step
    return list_of_dataframes


def Sort_Maccor_Steps_Into_CP_And_OCV(list_of_steps, voltage_threshold):
    """Sorts Maccor steps into constant current (CP) charge / discharge and OCV after charge / discharge.
    list_of_steps = list of step dataframes ('Current (mA)', 'Voltage (V)'),
    voltage_threshold = voltage in V that separates OCV after charging (above) from OCV after discharging (below).
    Returns (CP charge, CP discharge, OCV after charge, OCV after discharge) as lists of dataframes."""
    ########## Sort the steps of a Maccor file into CP charge, CP discharge, OCV after charge and OCV after discharge ##########
    list_of_CP = []
    list_of_OCV_after_CP_step = []
    list_of_dataframes_CP_charge = []
    list_of_dataframes_CP_discharge = []
    list_of_dataframes_OCV_after_CP_step_charge = []
    list_of_dataframes_OCV_after_CP_step_discharge = []

    ########## Split the dataframes of all steps into OCV steps and CP steps ##########
    for i in range(0, len(list_of_steps)):
        if list_of_steps[i].iloc[0]['Current (mA)'] != 0:
            list_of_CP.append(list_of_steps[i])
        elif list_of_steps[i].iloc[0]['Current (mA)'] == 0:
            list_of_OCV_after_CP_step.append(list_of_steps[i])

    print(len(list_of_CP))
    print(len(list_of_OCV_after_CP_step))

    ######### Split the OCV dataframes into OCV after charging and OCV after discharging #########
    # after charging the cell has a high voltage, after discharging a low voltage
    for i in range(0, len(list_of_OCV_after_CP_step)):
        if list_of_OCV_after_CP_step[i].iloc[0]['Voltage (V)'] > voltage_threshold:
            list_of_dataframes_OCV_after_CP_step_charge.append(list_of_OCV_after_CP_step[i])
        elif list_of_OCV_after_CP_step[i].iloc[0]['Voltage (V)'] < voltage_threshold:
            list_of_dataframes_OCV_after_CP_step_discharge.append(list_of_OCV_after_CP_step[i])

    ######### Split the CP steps into charging and discharging ##########
    for i in range(0, len(list_of_CP)):
        if list_of_CP[i].iloc[0]['Current (mA)'] > 0:
            list_of_dataframes_CP_charge.append(list_of_CP[i])
        elif list_of_CP[i].iloc[0]['Current (mA)'] < 0:
            list_of_dataframes_CP_discharge.append(list_of_CP[i])

    print(len(list_of_dataframes_CP_charge))
    print(len(list_of_dataframes_CP_discharge))

    return list_of_dataframes_CP_charge, list_of_dataframes_CP_discharge, list_of_dataframes_OCV_after_CP_step_charge, list_of_dataframes_OCV_after_CP_step_discharge

