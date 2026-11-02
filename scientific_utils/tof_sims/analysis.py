"""Aligning mass lists and restructuring ToF-SIMS dataframes."""

import numpy as np
import pandas as pd


def Align_Mass_Lists(a, b, c, d):
    """Aligns the mass lists of several measurements in one dataframe: every mass is put on a grid from b to c with step d,
    empty rows are dropped, NaN -> 0, and rows less than 0.005 u apart are summed up.
    a = list of dataframes (column 1 = mass in u, column 2 = area/intensity), b/c = lowest/highest mass in u, d = mass resolution (grid step) in u.
    Returns one dataframe ('created Mass values' + one intensity column per measurement)."""
    ### Function Explained
    # This function aligns multiple dataframes according to their mass values into one dataframe. The mass values in the column are different for every dataframe. For that reasen a massresolution must be given to group rows together which have very similar mass values
    
    ### Defined Parameters
    list_of_dataframes = a
    min_mass_value = b
    max_mass_value = c
    mass_resolution = d
    
    ### Create an array with all possilbe masses
    step_size = mass_resolution
    all_possible_values = np.arange(min_mass_value, max_mass_value, step_size)
    print('Lowest Value: %s u | Highest Value: %s u' %(min_mass_value, max_mass_value))
    print('Number of created datapoints (masses) is: %s' %len(all_possible_values))
    
    ### Create an empty dataframe with all possible masses via a dictionary
    created_masses_dict = {'created Mass values': all_possible_values }
    created_masses_dataframe = pd.DataFrame(created_masses_dict)
    
    ##### Compare created mass list with Mass in the collected data and transfer the data into the new dataframe
    for i in range(0, len(list_of_dataframes)):
        print('Starting comparing %s von %s Dataframe!' %((i+1), len(list_of_dataframes)))
        for k in range(0, len(list_of_dataframes[i])):
            ##### define the column names of the columns which are compared
            column_name_data = list_of_dataframes[i].columns[1]
            column_name_new_data = created_masses_dataframe.columns[0]
        
            ##### defines the range in whoch the value must be of the newly created dataframe based on the step size/mass resolution
            value = list_of_dataframes[i][column_name_data].iloc[k]
            upper_value = value + (step_size*0.49)
            lower_value = value - (step_size*0.49)
        
            ##### Search for the row which has the value contained in the dataframe of the raw data
            boolean_data = created_masses_dataframe[column_name_new_data].between(lower_value, upper_value) # gives the Rows as 'true' which fullfill the criteria
            index = created_masses_dataframe[boolean_data].index
            #print(dataframe_new[boolean_data].index)
        
            ##### Transfer the raw Data into the new created dataframe by index
            column_name_area = list_of_dataframes[i].columns[2]
            value_area = list_of_dataframes[i][column_name_area].iloc[k]
            created_masses_dataframe.loc[index, column_name_area] = value_area
            
    ### Defines a subset of a datframe with only the intensity values  
    #print(created_masses_dataframe.columns)
    created_masses_dataframe_subset = created_masses_dataframe.iloc[:,1:]
    #print(created_masses_dataframe_subset.columns)
    
    ### Delete the rows in the new dataframe which only contains NaN values the defined subset
    created_masses_dataframe = created_masses_dataframe.dropna(subset=created_masses_dataframe_subset.columns, how='all')
    print('Deleting empty rows ....')
    
    ### Replace all NaN values with 0
    created_masses_dataframe = created_masses_dataframe.fillna(0)
    
    ### Extract Column names from the new Dataframe for summing up the values later
    column_names_for_summing_up = list(created_masses_dataframe_subset.columns)

    ### All rows which have a smaller difference than a certain value between each other are summed up
    # Based on: https://stackoverflow.com/questions/46732760/merge-rows-pandas-dataframe-based-on-condition
    # defines the group condition; Here the difference between the selected row and the next row should be smaller than 0.005
    print('Gouping rows together which have a lower mass difference than 0.005 ....')
    grps = created_masses_dataframe['created Mass values'].sub(created_masses_dataframe ['created Mass values'].shift(1)).gt(0.005).cumsum()
    # Perfomrs grouping
    gpby = created_masses_dataframe.groupby(grps)
    # Adding the values of the 
    created_masses_dataframe  = gpby.agg({'created Mass values':min}).join(gpby[column_names_for_summing_up].sum())
    # remove index column name
    created_masses_dataframe.index.name = None
    
    print('....finished!!!')
    
    return created_masses_dataframe

