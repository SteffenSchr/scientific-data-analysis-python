"""Nyquist and Bode plots and the plot of selected frequencies."""

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker

from scientific_utils.general.plotting import list_of_Hexcolors
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.general.plotting import pgf_with_latex
from scientific_utils.general.plotting import Matplotlib_Legend_Above_And_Save, Matplotlib_New_Figure_With_Frame, Set_Scientific_Tick_Labels
from scientific_utils.publication_plotly import my_color_scale
from scientific_utils.impedance.analysis import Calculate_Impedance_RQ_Model


def Matplotlib_Nyquist_Plot(f, ModelValues, label, impedance_model=None):
    """Nyquist plot (-Im vs Re, equal scale on both axes) of an impedance model.
    f = frequencies in Hz, ModelValues = model parameters, label = legend entry, impedance_model = model function (default Calculate_Impedance_RQ_Model). Returns the plot."""
    # the RQ model is used if no other model is given
    if impedance_model is None:
        impedance_model = Calculate_Impedance_RQ_Model
    fig = plt.figure()
    Set_Figure_Size_For_Plot_Area(fig) # was: fig.set_size_inches((2.5*3.4),3.4)
    plt.rcParams.update(pgf_with_latex)

    plot = plt.plot(impedance_model(f, ModelValues, PhaseAngle=False).real, -impedance_model(f, ModelValues, PhaseAngle=False).imag, lw=1, label=label)
    
    ax = plt.gca()
    ax.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
    ax.axis('equal')
    
    plt.legend()
    plt.ylabel('-Z imag / Ohm')
    plt.xlabel('Z real / Ohm')
               
    return plot


def Matplotlib_Compare_Model_And_Fit(f, Z_from_model, Z_from_optimized_parameters):
    """Two plots to compare the simulated model with the fit: real part against frequency (log axis) and the Nyquist plot (equal scale on both axes).
    f = frequencies in Hz, Z_from_model / Z_from_optimized_parameters = complex impedance of the model and of the fitted parameters. Returns both figures."""
    ########## Real part against the frequency
    fig_real = plt.figure()
    plt.plot(f, Z_from_model.real, color=my_color_scale[4], linestyle='None', marker='.', label=r'model', linewidth=1.5)
    plt.plot(f, Z_from_optimized_parameters.real, color=my_color_scale[1], linestyle='None', marker='.', label=r'fitted', linewidth=0.5)
    ax = plt.gca()
    ax.set_xscale('log')
    ax.set_xlabel('Frequency / Hz')
    ax.set_ylabel('Z real / Ohm')
    plt.legend()

    ########## Nyquist plot
    fig_nyquist = plt.figure()
    plt.plot(Z_from_model.real, -Z_from_model.imag, color=my_color_scale[4], linestyle='None', marker='.', label=r'model', linewidth=1.5)
    plt.plot(Z_from_optimized_parameters.real, -Z_from_optimized_parameters.imag, color=my_color_scale[1], linestyle='None', marker='.', label=r'fitted', linewidth=0.5)
    ax = plt.gca()
    ax.axis('equal')
    ax.set_xlabel('Z real / Ohm')
    ax.set_ylabel('-Z imag / Ohm')
    plt.legend()

    return fig_real, fig_nyquist


def Matplotlib_XvsY_And_Data_Extraction(list_of_dataframes, x_values_column_name, y_values_column_name, y_ax_label, x_ax_label, rate_to_save, additional_name, legend_title, list_RateTest_labels):
    """One measured Nyquist plot per rate (equal scale on both axes). The rate number rate_to_save is saved as ./images/Impedance_Rate<r>C_<additional_name>.png. Returns the plot."""
    for i in range(0, len(list_of_dataframes)):
        #### Settings for the whole figure 1
        fig1, frame1 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
        #fig1.set_size_inches((2.5*3.4),(3.4))
    
    
        #### Important plot parameters based on the length of the dataframes
        # x values
        X = list_of_dataframes[i][x_values_column_name]

        # y values
        Y = list_of_dataframes[i][y_values_column_name]
       
        # For the length of the x axis
        X_range = max(X) - min(X)
        Xmin = min(X) 
        Xmax = max(X) 
        Xmin_extended = Xmin - X_range*0.02
        Xmax_extended = Xmax + X_range*0.02
    
        # For the length of the y axis
        Y_range = max(Y) - min(Y)
        Ymin = min(Y)
        Ymax = max(Y)
        Ymin_extended = Ymin - Y_range*0.1
        Ymax_extended = Ymax + Y_range*0.1
    
        # For the legend
        number_of_datapoints = len(X)
        
        ### Settings for the first axis (here the dQ/dV plot)
        plot = plt.plot(X, Y, list_of_Hexcolors[i], linestyle='None', alpha=0.5, marker='.', label=r'impedance', linewidth=1.5)

        #frame1.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))

        # Scientific label format changing from 1e1 to 1x10^1
        Set_Scientific_Tick_Labels(frame1, (-3,3))

        frame1.set_aspect('equal', 'datalim') # equal scale on both axes; the axis ranges grow instead of the plot area shrinking (was 'box')
        
        frame1.set_ylabel(y_ax_label)				                # Label of the y axis
        #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
        #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
        frame1.set_xlabel(x_ax_label)                                              # Label of the x axis
        #ax.set_xscale('log')
        #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        #frame1.set_xticks([])                               # which values are shown on the x axis
    
        # Saving setups
        index_to_save = rate_to_save - 1
        
        # Legend above the plot and saving (legend first, so it is in the saved file)
        Matplotlib_Legend_Above_And_Save(frame1, legend_title  + ' Rate: %s ' %(list_RateTest_labels[i]), i == index_to_save, './images/Impedance_Rate%sC_%s.png' %(list_RateTest_labels[i], additional_name))
        
        plot = plt.show(block=False)
        
    return plot


def Matplotlib_XvsY_And_Frequency_Extraction(list_of_dataframes, x_values_column_name, y_values_column_name, z_values_column_name, y_ax_label, x_ax_label, rate_to_save, additional_name, legend_title, list_RateTest_labels):
    """Like Matplotlib_XvsY_And_Data_Extraction; also marks the frequencies in rows 19, 29, ..., 99 and collects their Re and -Im.
    z_values_column_name = frequency column. Returns (plot, one-row dataframe with the selected values)."""
    # Defining of a Dataframe for the selected Frequencies
    dictionary_of_selected_data = {} # the values are collected first and put in the dataframe at once (adding the columns one by one fragments the dataframe)
    
    for i in range(0, len(list_of_dataframes)):
        #### Settings for the whole figure 1
        fig1 = plt.figure()
        #fig1.set_size_inches((2.5*3.4),(3.4))
        #plt.rcParams.update(pgf_with_latex)
    
    
        #### Important plot parameters based on the length of the dataframes
        # x values
        X = list_of_dataframes[i][x_values_column_name]

        # y values
        Y = list_of_dataframes[i][y_values_column_name]
        
        # Z value
        Z = list_of_dataframes[i][z_values_column_name]
       
        # For the length of the x axis
        X_range = max(X) - min(X)
        Xmin = min(X) 
        Xmax = max(X) 
        Xmin_extended = Xmin - X_range*0.02
        Xmax_extended = Xmax + X_range*0.02
    
        # For the length of the y axis
        Y_range = max(Y) - min(Y)
        Ymin = min(Y)
        Ymax = max(Y)
        Ymin_extended = Ymin - Y_range*0.1
        Ymax_extended = Ymax + Y_range*0.1
    
        # For the legend
        number_of_datapoints = len(X)
        
        # selected frequencies according to index in the data frame
        list_of_selected_frequencies = [19, 29, 39, 49, 59, 69, 79, 89, 99]
        
        ### Settings for the first axis (here the dQ/dV plot)
        frame1 = fig1.add_axes((.1,.3,1.0,0.6))
        plot = plt.plot(X, Y, list_of_Hexcolors[i], linestyle='None', alpha=0.5, marker='.', label=r'impedance', linewidth=1.5)
        for k, m in enumerate(list_of_selected_frequencies):
            plt.plot(X.iloc[m], Y.iloc[m], color='red', linestyle='None', alpha=1.0, marker='x', label=r'selected frequencies', linewidth=5.0)
            # the frequency is written next to every second point (instead of one legend entry per point), so the labels do not overlap
            if k % 2 == 0:
                frequency = Z.iloc[m]
                frequency_text = '%.3g kHz' %(frequency/1000) if frequency >= 1000 else '%.3g Hz' %(frequency)
                frame1.annotate(frequency_text, (X.iloc[m], Y.iloc[m]), xytext=(2, 4), textcoords='offset points', fontsize=6, color='red')

        #frame1.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))

        # Scientific label format changing from 1e1 to 1x10^1
        Set_Scientific_Tick_Labels(frame1, (-3,3))

        frame1.set_aspect('equal', 'datalim') # equal scale on both axes; the axis ranges grow instead of the plot area shrinking (was 'box')
        
        frame1.set_ylabel(y_ax_label)				                # Label of the y axis
        #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
        #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
        frame1.set_xlabel(x_ax_label)                                              # Label of the x axis
        #ax.set_xscale('log')
        #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        #frame1.set_xticks([])                               # which values are shown on the x axis
    
        # Saving setups
        index_to_save = rate_to_save - 1
        
        # Legend above the plot and saving (legend first, so it is in the saved file)
        Matplotlib_Legend_Above_And_Save(frame1, legend_title  + ' Rate: %s ' %(list_RateTest_labels[i]), i == index_to_save, './images/Impedance_Rate%sC_%s.png' %(list_RateTest_labels[i], additional_name))
        
        # Extracting the Selected Freqeuncies
        
        for n in list_of_selected_frequencies:
            frequency = Z.iloc[n]
            frequency = round(frequency, 3)
            resistance_real = X.iloc[n]
            resistance_imag = Y.iloc[n]
            rate = list_RateTest_labels[i]
    
            dictionary_of_selected_data['Real / Ohm at Frequency %s Hz and Rate %s C' %(frequency, rate)] = resistance_real
            dictionary_of_selected_data['-Imag / Ohm at Frequency %s Hz and Rate %s C' %(frequency, rate)] = resistance_imag

        data = pd.DataFrame(dictionary_of_selected_data, index=[0])
        
        plot = plt.show(block=False)
        
    return plot , data
