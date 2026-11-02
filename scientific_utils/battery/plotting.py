"""Plots for cycling and rate test data."""

import plotly.graph_objects as go
import math
import matplotlib
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker

from scientific_utils.general.plotting import Convert_cm_To_inch
from scientific_utils.general.plotting import list_of_Hexcolors
from scientific_utils.general.plotting import my_colormap
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.general.plotting import pgf_with_latex
from scientific_utils.general.plotting import Matplotlib_Legend_Above_And_Save, Matplotlib_New_Figure_With_Frame, Set_Scientific_Tick_Labels
from scientific_utils.general.plotting import yellow
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style
from scientific_utils.publication_plotly import my_color_scale
from scientific_utils.publication_plotly import pt, FONT_PT, TICK_FONT_PT, LEGEND_FONT_PT


def Matplotlib_Overview_With_Colormap(list_of_dataframes, x_values_column_name, y_values_column_name, y_ax_label, x_ax_label, save, name_figure, legend_title, list_of_labels=None, colorbar_ticks=None, colorbar_ticklabels=None):
    """All curves (x relative to its first value) in one plot, coloured by cycle or rate, with colour bar.
    list_of_labels = None -> cycles 1..50, else the rates. save = 1 -> ./images/Overview_<name_figure>.pdf.
    colorbar_ticks/colorbar_ticklabels = positions (0..1) and labels of the colour bar
    (default: cycles 1, 25, 50 or the rates 0.10, 0.33, 1.00 C of this repository)."""
    # Solution according to: https://stackoverflow.com/questions/43805821/matplotlib-add-colorbar-to-non-mappable-object
    fig, frame = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig.set_size_inches(cm2inch(8, 4))

    
    number_of_points = len(list_of_dataframes)

    cmap = my_colormap.resampled(number_of_points) # defining which colormap is used and how many colorpoints are collected

    for n,i in enumerate(range(0, len(list_of_dataframes))):
        x = (list_of_dataframes[i][x_values_column_name] - list_of_dataframes[i].iloc[0][x_values_column_name])
        y = list_of_dataframes[i][y_values_column_name]

        # no legend entry per curve: the colour bar shows the cycle or rate
        plt.plot(x, y, c=cmap(n), linestyle='None', alpha=0.5, marker='.', linewidth=1.5)

    # Defining that a colorbar is plotted according to the defined colormap
    sm = plt.cm.ScalarMappable(cmap=cmap) # defining that the colomap is used for mappable
    sm.set_array([])
    if list_of_labels is None:
        if colorbar_ticks is None: # default: 50 cycles
            colorbar_ticks = [0.01, 0.50, 0.99]
            colorbar_ticklabels = [1, 25, 50]
        cbar = plt.colorbar(sm, ax=plt.gca(), ticks=colorbar_ticks, label=r'$Cycle$') # defining which mappable is plottet as colorbar and which ticks and label
        cbar.ax.set_yticklabels(colorbar_ticklabels) # changes the label of the ticks
    else:
        if colorbar_ticks is None: # default: the three rates of the rate test
            colorbar_ticks = [0.17, 0.50, 0.83]
            colorbar_ticklabels = [0.10, 0.33, 1.00]
        cbar = plt.colorbar(sm, ax=plt.gca(), ticks=colorbar_ticks, label=r'$Rate$ / C')
        cbar.ax.set_yticklabels(colorbar_ticklabels)
    

    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame, (-2,2))

    # Defining the axis
    frame.set_ylabel(y_ax_label)				                # Label of the y axis
    #frame.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    
    frame.set_xlabel(x_ax_label)                                              # Label of the x axis
    #frame.set_xscale('log')
    #frame.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame.set_xticks([])                               # which values are shown on the x axis
    
    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame, legend_title, save, './images/Overview_%s.pdf' %(name_figure), dpi=1000, facecolor='w', edgecolor='w', format='pdf',bbox_inches='tight')
    
    plot = plt.show(block=False)
    
    return plot


def Matplotlib_Overview_Single_Dataframe(list_of_dataframes, x_values_column_name, y_values_column_name, y_ax_label, x_ax_label, save, name_figure, legend_title):
    """One dataframe (CP and OCV steps) with fixed axis ranges (x 9.25-10.25, y 3.55-3.75).
    save = 1 -> ./images/CP_and_OCV_vs_time_<name_figure>.png."""
    # Solution according to: https://stackoverflow.com/questions/43805821/matplotlib-add-colorbar-to-non-mappable-object
    fig, frame = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig.set_size_inches(cm2inch(8, 4))


    x = list_of_dataframes[x_values_column_name]
    y = list_of_dataframes[y_values_column_name]   
        
    plt.plot(x, y, list_of_Hexcolors[0], linestyle='None', alpha=0.5, marker='.', label='CP and OCV', linewidth=1.5)  

    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame, (-3,3))

    # Defining the axis
    frame.set_ylabel(y_ax_label)				                # Label of the y axis
    frame.set_ylim(3.55, 3.75)                                                             # minimum and maximum value shown on the y axis
    #frame.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    
    frame.set_xlabel(x_ax_label)                                              # Label of the x axis
    #frame.set_xscale('log')
    frame.set_xlim(9.25, 10.25)                                                         # minimum and maximum value shown on the x axis
    #frame.set_xticks([])                               # which values are shown on the x axis
    
    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame, legend_title, save, './images/CP_and_OCV_vs_time_%s.png' %(name_figure))
    
    plot = plt.show(block=False)
    
    return plot


def Matplotlib_Compare_Raw_And_Equidistant_Data(dataframe, x_values_column_name, y_values_column_name, cycle, dataframe_equidistant, x_values_column_name_equidistant, y_values_column_name_equidistant ,y_ax_label, y_ax_lim, x_ax_label, x_ax_lim, save, name_figure, legend_title):
    """One raw curve and its equidistant (resampled) version in one plot.
    save = 1 -> ./images/Overview_<name_figure>.pdf."""
    # data for raw values
    x = dataframe[x_values_column_name]
    y = dataframe[y_values_column_name]

    #data for equidistant data
    x_equidistant = dataframe_equidistant[x_values_column_name_equidistant]
    y_equidistant = dataframe_equidistant[y_values_column_name_equidistant]

    fig, ax = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area (was: plt.figure() with fig.set_size_inches((2.5*3.4),(3.4)))

    plt.plot(x, y, list_of_Hexcolors[0], linestyle='None', alpha=0.5, marker='.', label='raw data (%s points)' %(len(dataframe)), linewidth=1.5)
    plt.plot(x_equidistant, y_equidistant, list_of_Hexcolors[-1], linestyle='None', alpha=0.5, marker='.', label='equidistant data (%s points)' %(len(dataframe_equidistant)), linewidth=1.5)

    ax.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))

    ax.set_ylabel(y_ax_label)				                # Label of the y axis
    plt.ylim(y_ax_lim)                                                             # minimum and maximum value shown on the y axis
    #plt.yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    ##### Plot the OCV before every charging step of the rate test
    ax.set_xlabel(x_ax_label)                                              # Label of the x axis
    #ax.set_xscale('log')
    plt.xlim(x_ax_lim)                                                          # minimum and maximum value shown on the x axis
    #plt.xticks(np.arange(-1.2e-1, 1.2e-1, 4e-2))                               # which values are shown on the x axis

    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(ax, legend_title, save, './images/Overview_%s.pdf' %(name_figure), dpi=1000, facecolor='w', edgecolor='w', format='pdf',bbox_inches='tight')
    #plt.axis('equal')
    #ax.grid()                                                                  # adds a grid
    
    plot = plt.show(block=False)                                                       # Shows the plot, but the following code keeps running

    return plot


def Matplotlib_Data_Smoothed_Residuals(list_of_dataframes, x_values_column_name, y_values_column_name, y_values_smoothed_column_name, list_of_dataframes_peaks, x_peak_values_column_name, y_peak_values_column_name, cycle_to_save, additional_name,legend_title, list_of_labels=None, set_axis_limits=True, cycles_to_show=None):
    """For every curve: dQ/dV, smoothed curve, peaks (red crosses) and the residuals below.
    The curve number cycle_to_save is saved as ./images/Plotting_data_smootheddata_residuals_<Cycle|Rate><n>_<additional_name>.png.
    set_axis_limits = False -> automatic axis limits. cycles_to_show = list of curve numbers that are plotted (None -> all)."""
    for i in range(0, len(list_of_dataframes)):
        if cycles_to_show is not None and (i+1) not in cycles_to_show and i != cycle_to_save - 1: # only the chosen curves (and the saved one) are plotted
            continue
        # cycles are counted, rates are taken from the list of labels
        if list_of_labels is None:
            label_name = 'Cycle'
            label_value = (i+1)
        else:
            label_name = 'Rate'
            label_value = list_of_labels[i]
        #### Settings for the whole figure 1
        fig1 = plt.figure()
        #fig1.set_size_inches((2.5*3.4),(3.4))
        #plt.rcParams.update(pgf_with_latex) # important when worked with latex and pgfplot
        
    
        #print(list_of_dataframes_peaks[i])
        #print(list_of_dataframes_peaks[i][0])
        #print(list_of_dataframes_peaks[i][0][y_peak_values_column_name])
        
    
        #### Important plot parameters based on the length of the dataframes
        # x values
        X = list_of_dataframes[i][x_values_column_name]
        X2_list = []
        for j in range(0, len(list_of_dataframes_peaks[i])):
            X2 = pd.DataFrame(list_of_dataframes_peaks[i][j][x_peak_values_column_name]).to_numpy()
            X2_list.append(X2)
            
        # y values
        Y = list_of_dataframes[i][y_values_column_name]
        Y2 = list_of_dataframes[i][y_values_smoothed_column_name]
        Y3_list = []
        for j in range(0, len(list_of_dataframes_peaks[i])):
            Y3 = pd.DataFrame(list_of_dataframes_peaks[i][j][y_peak_values_column_name]).to_numpy()
            Y3_list.append(Y3)
            
        # Values for plotting
        residuals = Y - Y2
        residuals_min = min(residuals)
        residuals_max = max(residuals)
        residuals_range = residuals_max - residuals_min
        residuals_min_extended = residuals_min - residuals_range*0.02
        residuals_max_extended = residuals_max + residuals_range*0.02
    
        # For the length of the x axis
        X_range = max(X) - min(X)
        Xmin = min(X) 
        Xmax = max(X) 
        Xmin_extended = Xmin - X_range*0.02
        Xmax_extended = Xmax + X_range*0.02
    
        # For the length of the y axis
        Ymin = min(Y2)
        Ymax = max(Y2)
        Y_range = Ymax - Ymin
        Ymin_extended = Ymin - Y_range*0.2
        Ymax_extended = Ymax + Y_range*0.2
    
        # For the legend
        number_of_datapoints = len(X)
    
        ### Settings for the first axis (here the dQ/dV plot)
        frame1 = fig1.add_axes((.1,.3,1.0,0.6))
        plt.plot(X, Y, list_of_Hexcolors[i], linestyle='None', alpha=0.5, marker='.', label=r'equidistant data', linewidth=1.5)
        plt.plot(X, Y2, my_color_scale[1], linestyle='None', alpha=0.5, marker='.', label=r'Savitzky-Golay smoothed', linewidth=1.5) # colour was yellow (#ffa200)
        for j in range(0, len(X2_list)):
            plt.plot(X2_list[j], Y3_list[j], color='red', linestyle='None', alpha=1.0, marker='x', label=r'peaks', linewidth=5.0)

        #frame1.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
        
        # Scientific label format changing from 1e1 to 1x10^1
        Set_Scientific_Tick_Labels(frame1, (-2,2))

        frame1.set_ylabel(r'$ \frac{dQ}{dV}$ / $\frac{\mathsf{mAh}}{\mathsf{V}}$', labelpad=15)				                # Label of the y axis
        if set_axis_limits == True:
            frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
        #frame1.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    
        frame1.set_xlabel(r'')                                              # Label of the x axis
        #ax.set_xscale('log')
        if set_axis_limits == True:
            frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        frame1.set_xticks([])                               # which values are shown on the x axis

        ### Settings for the second axis (here the residuals)
        frame2 = fig1.add_axes((0.1,.1,1.0,0.185))        
        plt.plot(X, residuals, alpha=0.8, marker='None', linestyle='-', linewidth=1.5)
        plt.hlines(y=0,xmin=Xmin_extended,xmax=Xmax_extended,color='red',linestyle='--',lw=1, alpha=0.5)
    
        frame2.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))

        frame2.set_ylabel(r' $residuals$ ')				                # Label of the y axis
        if set_axis_limits == True:
            frame2.set_ylim(residuals_min_extended, residuals_max_extended)                                                             # minimum and maximum value shown on the y axis
        #frame2.set_yticks(np.arange(-0.3, 0.31, 0.15))                                        # which values are shown on the y axis

        frame2.set_xlabel(r' $Potential$ / V  ')                                              # Label of the x axis
        #ax.set_xscale('log')
        if set_axis_limits == True:
            plt.xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        #plt.xticks(np.arange(-1.2e-1, 1.2e-1, 4e-2))                               # which values are shown on the x axis

        #Saving One Figure from one Rate
        index_to_save = cycle_to_save - 1
        
        # Legend above the plot and saving (legend first, so it is in the saved file)
        Matplotlib_Legend_Above_And_Save(frame1, legend_title + ' (%s: %s)' %(label_name, label_value), i == index_to_save, './images/Plotting_data_smootheddata_residuals_%s%s_%s.png' %(label_name, label_value, additional_name))
        
        plot = plt.show(block=False)
        
    return plot

