"""Unused functions moved here from `scientific_utils/battery/analysis.py` (nothing in the repository called them)."""

from numpy import diff
from scipy.interpolate import interp1d
import matplotlib as mpl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.signal

from scientific_utils.general.analysis import Round_Down_To_Odd
from scientific_utils.general.plotting import my_colormap
from scientific_utils.general.plotting import pgf_with_latex


def Extract_OCV_And_Charging_Discharging_Steps(a):
    """Splits a cycler dataframe into steps (new step when 'StepTime (seconds)' falls by more than 3 s)
    and sorts them by the current at the start: 0 -> OCV, > 0 -> charging, < 0 -> discharging.
    a = dataframe ('StepTime (seconds)', 'Current (mA)').
    Returns (OCV steps, OCV step names, charging steps, names, discharging steps, names); names are 'Step n'."""
    ##### Define the input data
    data = a
    
    ##### Seperate the Steps into seperate dataframes 
    step_groupcondition = (data['StepTime (seconds)'] < (data['StepTime (seconds)'].shift() - 3)).cumsum() # if the value of the row is smaller than the value of the row before minus 3, one is added, otherwise the value is 0
    grouped_steps = data.groupby(step_groupcondition)              # Groups the dataframe with the results from before: a new dataframe is created for every number in 'group_ids'
    list_of_steps = [g for k,g in grouped_steps] # Put the separated cycles in a list, so that every list entry is one cycle
    
    ##### Define empty List for the different Steps
    list_for_OCV = []
    list_for_OCV_StepName = []
    
    list_for_Charging = []
    list_for_Charging_StepName = []
    list_for_Discharging = []
    list_for_Discharging_StepName = []
        
    ##### Sort the different Steps into their Electrochemical Procedure
    for i in range(len(list_of_steps)):
        if list_of_steps[i].iloc[0]['Current (mA)'] == 0:
            list_for_OCV.append(list_of_steps[i])
            Step_Name = str('Step %s' %(i+1))
            list_for_OCV_StepName.append(Step_Name)
        
        elif list_of_steps[i].iloc[0]['Current (mA)'] != 0:
            ######### Trennung in charing and discharging ##########
            if list_of_steps[i].iloc[0]['Current (mA)'] > 0:
                list_for_Charging.append(list_of_steps[i])
                Step_Name = str('Step %s' %(i+1))
                list_for_Charging_StepName.append(Step_Name)
            
            elif list_of_steps[i].iloc[0]['Current (mA)'] < 0:
                list_for_Discharging.append(list_of_steps[i]) 
                Step_Name = str('Step %s' %(i+1))
                list_for_Discharging_StepName.append(Step_Name)
    
    return  list_for_OCV, list_for_OCV_StepName, list_for_Charging, list_for_Charging_StepName, list_for_Discharging, list_for_Discharging_StepName


def Extract_ConstantCurrent_And_ConstantPotential_Steps(a, b):
    """Separates constant current steps from potential hold steps by comparing the mean |current| and |voltage| of a step
    with the mean of its rows 1-3 (threshold 0.04 mA resp. 0.04 V).
    a = list of step dataframes ('Current (mA)', 'Voltage (V)'), b = list of step names.
    Returns 8 lists: CC charge steps + names, CC discharge + names, potential hold charge + names, potential hold discharge + names."""
    ##### Define the input data
    data = list_of_dataframes = a
    names = list_of_StepNames = b
    
    
    ##### Define empty List for the different Steps
    list_for_ConstantCurrentCharge = []
    list_for_ConstantCurrentCharge_StepName = [] 
    list_for_ConstantCurrentDischarge = []
    list_for_ConstantCurrentDischarge_StepName = [] 
    
    list_for_PotentialHoldCharge = []
    list_for_PotentialHoldCharge_StepName = []
    list_for_PotentialHoldDischarge = []
    list_for_PotentialHoldDischarge_StepName = []
    
    ##### Seperate into constant Pot or Constant Current steps
    #calculate the mean over 10 rows and check how this mean changes compared to a given threshold
    for i in range(len(data)):
        ##### selecting the first 10 rows of the dataframe
        #length_data = len(data[i])
        select_data = data[i] # .iloc[:10]
        
        ##### Calculating the current mean and current threshold
        mean_current = sum(abs(select_data['Current (mA)'])) / len(select_data)
        threshold_current = 2*0.02 # 0.0002
        threshold_current_value = sum(abs(data[i].iloc[1:4]['Current (mA)']))/3 - threshold_current
        #print('mean current %s ; threshold %s' %(mean_current, threshold_current_value))
        
        ##### Calculating the voltage mean and voltage threshold
        mean_voltage = sum(abs(select_data['Voltage (V)'])) / len(select_data)
        threshold_voltage = 2*0.02 # 0.0002
        threshold_voltage_value = sum(abs(data[i].iloc[1:4]['Voltage (V)']))/3 - threshold_voltage
        #print('mean voltage %s ; threshold %s' %(mean_voltage, threshold_voltage_value))
        
        ##### Check if the step is charging or discharging, because this changes the threshold condition
        ##### Comparing the mean value to the first value + trheshold to identify if the step is a constant potetial or constant current step
        if data[i].iloc[0]['Current (mA)'] > 0:
            if (mean_current <= threshold_current_value) == True and (mean_voltage >= threshold_voltage_value) == True:
                list_for_PotentialHoldCharge.append(data[i])
                list_for_PotentialHoldCharge_StepName.append(names[i])
            elif (mean_current >= threshold_current_value) == True and (mean_voltage >= threshold_voltage_value) == True:
                list_for_ConstantCurrentCharge.append(data[i])
                list_for_ConstantCurrentCharge_StepName.append(names[i])
        
        elif data[i].iloc[0]['Current (mA)'] < 0:
            if (mean_current <= threshold_current_value) == True and (mean_voltage >= threshold_voltage_value) == True:
                list_for_PotentialHoldDischarge.append(data[i])
                list_for_PotentialHoldDischarge_StepName.append(names[i])
            elif (mean_current >= threshold_current_value) == True and (mean_voltage <= threshold_voltage_value) == True:
                list_for_ConstantCurrentDischarge.append(data[i])
                list_for_ConstantCurrentDischarge_StepName.append(names[i])
            
    return list_for_ConstantCurrentCharge, list_for_ConstantCurrentCharge_StepName, list_for_ConstantCurrentDischarge, list_for_ConstantCurrentDischarge_StepName, list_for_PotentialHoldCharge, list_for_PotentialHoldCharge_StepName, list_for_PotentialHoldDischarge, list_for_PotentialHoldDischarge_StepName


def Calculate_CRate_From_Measured_Current(a, b, c):
    """C-rate of a measured current.
    a = active material mass in mg, b = theoretical specific capacity in mAh/g, c = measured current in A.
    The current for 1C is a*b/1e6 A. Returns the C-rate."""
    # define Parameters
    active_material_mass = a
    theoretical_specific_capacity = b
    measured_current = c
    
    # Calculating the Current needed to reach 1 C
    current_1C = (active_material_mass*theoretical_specific_capacity)/(1e6)
    print('Current needed for 1C with a theoretical capacity of %s mAh/g: %s A' %(theoretical_specific_capacity, current_1C))
    print('The measured Current is: %s A' %(measured_current))
    # Calculating the C Rate of the measured Current
    C_Rate = measured_current / current_1C
    print('C-Rate of measured current equals: %s C' %(C_Rate))
    
    return C_Rate


def Calculate_Mean_Ratio_And_Save(dataframe_name_for_calculation, list_of_column_names_numerator, list_of_column_names_denominator, dataframe_name_for_saving, new_column_name):
    """Mean of the ratios numerator column i / denominator column i, saved as a new column in another dataframe.
    dataframe_name_for_calculation = dataframe with the columns, list_of_column_names_numerator/denominator = column names,
    dataframe_name_for_saving = dataframe that gets the new column new_column_name. Returns None."""
    numerators_list = []
    denominators_list = []
    ratio_list = []
    
    for i in range(0, len(list_of_column_names_numerator)):
        numerator = dataframe_name_for_calculation[list_of_column_names_numerator[i]]
        numerators_list.append(numerator)

    for i in range(0, len(list_of_column_names_denominator)):
        denominator = dataframe_name_for_calculation[list_of_column_names_denominator[i]]
        denominators_list.append(denominator)

    #print('numerators_list: ', numerators_list) 
    #print('denominators_list: ', denominators_list)
            
    for j in range(0, len(numerators_list)):
        ratio = numerators_list[j]/denominators_list[j]
        ratio_list.append(ratio)
        
    #print('ratio_list: ' , ratio_list)
    
    mean_ratio = sum(ratio_list)/len(ratio_list)
    #print('mean_ratio: ' , mean_ratio)

    dataframe_name_for_saving[new_column_name] = mean_ratio
      
    return


def Calculate_Ratio_Over_Multiple_Columns(list_of_columnnames_which_relativised, list_for_values_that_get_substracted, start_string_part_for_new_column_name, end_string_part_for_new_column_name, dataframe_for_ratio_calculation, dataframe_for_saving_new_value, name_of_new_column):
    """Ratio of every column in list_of_columnnames_which_relativised to the first column in list_for_values_that_get_substracted
    (with Calculate_Mean_Ratio_And_Save). The new column is called '<name_of_new_column> at <column name up to end_string_part_for_new_column_name>'.
    start_string_part_for_new_column_name is not used. Returns None."""
    for i in range(0, len(list_of_columnnames_which_relativised)):
        # column names
        text1 = list_for_values_that_get_substracted[0]
        text2 = list_of_columnnames_which_relativised[i]
        #define the boundaries of the string part which shall be extracted 
        start_string = start_string_part_for_new_column_name
        end_string = end_string_part_for_new_column_name
        # extract the string part set by the boundaries (this string part is used for the name of the new column)
        string_part_text2 = text2[0:text2.find(end_string) + len(end_string)]
        # Calculate the ratio between the columns with name 'text1' and 'text2' and generate a new columnname with 'string_part_text1'
        Calculate_Mean_Ratio_And_Save(dataframe_for_ratio_calculation, [text2], [text1], dataframe_for_saving_new_value, name_of_new_column + ' at %s' %(string_part_text2))
