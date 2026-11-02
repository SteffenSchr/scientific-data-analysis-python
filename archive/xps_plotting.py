"""Unused functions moved here from `scientific_utils/xps/plotting.py` (nothing in the repository called them)."""

from colour import Color
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from scientific_utils.general.plotting import Convert_cm_To_inch
from scientific_utils.general.plotting import my_colormap
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style
from scientific_utils.general.plotting import pgf_with_latex


def Matplotlib_Interactive_XPS_Plot(raw_data, input_parameters_Plot):
    """Several configurable XPS plots in one call; everything is set in the dictionary input_parameters_Plot
    (number_of_plots, x/y column names, axis labels, curve labels and styles, vertical lines with text, list_of_plot_names;
    saving = 'Yes' or '' -> ./<plot name>.png). Every list needs one entry per plot.
    raw_data = data, one dataframe per plot."""
    #############################################
    ########## Define What Data to use ##########
    #############################################
    
    ##### Define which list of dataframe is used #####
    data = raw_data
    print('The Dataframe with the variable name %s is used.' %'raw_data')
    print('The option to change the name of the variable dynamically is missing here!')
    print('---------------------------')
    
    ##### Look how many dataframes / measurements files are in the list #####
    print('There are %s different dataframes in the loaded data list' %(len(data)))
    
    ##### The Column names of the Dataframes are #####
    list_of_column_names = []
    for i in range(len(data)):
        list_of_column_names.append(data[i].columns)
        print(list_of_column_names[i])
    
    ################################################
    ########## Define the number of Plots ##########
    ################################################
    
    ##### Define the number of figures which should be created #####
    ##### Use the Input saved in the dictonary befor
    number_of_plots = int(input_parameters_Plot.get('number_of_plots', 1))
    print('-------------------')
    print('Creating %s plots' %(number_of_plots))
    print('-------------------')
    
    ###############################################
    ########## Define which X-Axis used  ##########
    ###############################################
    
    ##### Select the Name of the X-Axis for the different plots #####
    list_of_x_axis_names = []
    
    ##### Define the X-Axis used from the Data 
    ##### Use the Dictonary Entry
    list_of_x_axis_names = input_parameters_Plot.get('list_of_x_axis_names', [])
    
    if len(list_of_x_axis_names) == number_of_plots:
        print('-------------------')
        print('The following X-Axis for the %s differnt plots are selected: %s' %(number_of_plots, list_of_x_axis_names))
        print('-------------------')
    elif len(list_of_x_axis_names) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('A proper error message is still missing here, so that the script also stops!')
        print('-------------------')
    
    ##############################################
    ########## Define which Y-Axis used ##########
    ##############################################
        
    ##### Defining an empty List for list of Y-Axis names
    list_of_list_with_y_axis_names = []
    
    ##### Select the Y-Axis for plotting; List of List is used because every Plot can have multiply Y Columns plotted
    ##### Use the Dictonary Entry
    list_of_list_with_y_axis_names = input_parameters_Plot.get('list_of_list_with_y_axis_names', [])
    
    if len(list_of_list_with_y_axis_names) == number_of_plots:
        print('-------------------')
        for i in range(number_of_plots):
            print('Y-Axis for the %s plot are: %s' %((i+1), list_of_list_with_y_axis_names[i]))
        print('-------------------')
    elif len(list_of_list_with_y_axis_names) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('A proper error message is still missing here, so that the script also stops!')
        print('-------------------')  

    ###########################################################
    ########## Define the Options for Saving Figures ##########
    ###########################################################
    
    ##### Saving Options 
    ##### User Input which defines what option is used
    saving = input_parameters_Plot.get('saving', '')
    ##### Defines a list for the names of the figures
    list_of_plot_names = []
    if saving == 'Yes':
        for i in range(number_of_plots):
            ##### User Inputs defines the name of the saved figures
            plot_name = input_parameters_Plot.get('plot_name', [])
            list_of_plot_names.append(plot_name)
            if plot_name == '':
                ##### When the user inputs nothin (just pressing "Enter") the value from the predefined dictonary is used
                list_of_plot_names = input_parameters_Plot.get('list_of_plot_names')
                break
    elif saving == '':
        ##### When the user inputs nothin (just pressing "Enter") the value from the predefined dictonary is used
        list_of_plot_names = input_parameters_Plot.get('list_of_plot_names')
    elif saving == 'No':
        print('saving option turned off')
    
    ########################################################################################
    ################################### Plotting Options ###################################
    ########################################################################################
    
    
    ########################### Options for every plot #####################################
    
    ############################################
    ########## Define X-Axis Labeling ##########
    ############################################
    ##### Define an empty list for the X-Axis labels shown in the final plot
    list_of_x_axis_labels = []
    
    ##### Use the Dictonary Entry
    list_of_x_axis_labels = input_parameters_Plot.get('list_of_x_axis_labels', [])
    
    if len(list_of_x_axis_labels) == number_of_plots:
        print('-------------------')
        print('The following X-Axis for the %s differnt plots are selected: %s' %(number_of_plots, list_of_x_axis_labels))
        print('-------------------')
    elif len(list_of_x_axis_labels) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('A proper error message is still missing here, so that the script also stops!')
        print('-------------------')
    
    ############################################
    ########## Define Y-Axis Labeling ##########
    ############################################
    
    ##### Defining an empty List for the Y-Axis label
    list_of_y_axis_labels = []
    
    ##### Select the Y-Axis for plotting; List of List is used because every Plot can have multiply Y Columns plotted
    ##### Use the Dictonary Entry
    list_of_y_axis_labels = input_parameters_Plot.get('list_of_y_axis_labels', [])
    
    if len(list_of_y_axis_labels) == number_of_plots:
        print('-------------------')
        print('The following Y-Axis for the %s differnt plots are selected: %s' %(number_of_plots, list_of_y_axis_labels))
        print('-------------------')
    elif len(list_of_y_axis_labels) != number_of_plots:
        print('-------------------')
        print('The number of selected Y-Axis do not match with the number of created plots!!!!')
        print('A proper error message is still missing here, so that the script also stops!')
        print('-------------------')
    
    ########################### Options for every curve ####################################
    
    #########################################################
    ########## Define Y-Graph/Plotted Data Labeles ##########
    #########################################################
    
    ##### Defining an empty List for Lists of the Graphs/Data Labeling
    list_of_list_with_y_curve_labels = []
    
    ##### Use the Dictonary Entry
    list_of_list_with_y_curve_labels = input_parameters_Plot.get('list_of_list_with_y_curve_labels', [])
    
    if len(list_of_list_with_y_curve_labels) == number_of_plots:
        print('-------------------')
        for i in range(number_of_plots):
            print('Y-curve labels for the %s plot are: %s' %((i+1), list_of_list_with_y_curve_labels[i]))
        print('-------------------')
    elif len(list_of_list_with_y_curve_labels) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('A proper error message is still missing here, so that the script also stops!')
        print('-------------------')
    
    ############################################################################
    ########## Define Options for Y-Graph/Plotted Data Plotting Style ##########
    ############################################################################
    
    ##### Create a List for List of Parameters which define the Style of the Plottet curve for every Y-Graph
    list_of_list_of_list_with_y_curve_style = []
    
    ##### Input what option to choose
    y_curve_style_options = input_parameters_Plot.get('y_curve_style_options', '')
    
    if y_curve_style_options == 'Standard':
        ##### Standard options are selected
        list_of_standard_style = ['cmap', 0.75, '.', 0.75,'-', 0.5] # [color, alpha, marker, markersize, linestyle, linewidth]
        for i in range(number_of_plots):
            ##### Standard Options are selected for every plot
            list_of_list_with_y_cruve_style_one_plot = []
            for n in range(0, len(list_of_list_with_y_axis_names[i])):
                 ##### Standard Options are selected for ever Y-Curve
                list_of_y_curve_style = list_of_standard_style
                list_of_list_with_y_cruve_style_one_plot.append(list_of_y_curve_style)
            list_of_list_of_list_with_y_curve_style.append(list_of_list_with_y_cruve_style_one_plot)
        
    elif y_curve_style_options == '':
        ##### Use the List our of the dictonary for the Plotting Style of the graphs
        list_of_list_of_list_with_y_curve_style = input_parameters_Plot.get('list_of_list_of_list_with_y_curve_style', [])
    
    
    if len(list_of_list_of_list_with_y_curve_style) == number_of_plots:
        print('-------------------')
        for i in range(number_of_plots):
            print('Y-curve labels for the %s plot are: %s' %((i+1), list_of_list_of_list_with_y_curve_style[i]))
        print('-------------------')
    elif len(list_of_list_of_list_with_y_curve_style) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('A proper error message is still missing here, so that the script also stops!')
        print('-------------------')
    
    ###########################################################################
    ########## Options for additional Lines and Text in the Figures  ##########
    ###########################################################################
    
    ##### Create a List for Parameters for Lines and Text in the Figures
    list_of_list_for_vlines_and_text = []  #Format of one List Entry: [x=284.8, color = 'grey', linewidth=1, linestyle='--', label='Carbon C-C sp3']
    
    text_and_lines = input_parameters_Plot.get('text_and_lines', '')
    if text_and_lines == 'Yes':
        ##### Uses pre defined Paramters from the Dictonary
        list_of_list_for_vlines_and_text = input_parameters_Plot.get('list_of_list_for_vlines_and_text')
    elif text_and_lines == '':
        print('No additional Lines or Text is plotted in the Plots')
        
    #############################################################################################
    ##################################### Plotting ##############################################
    #############################################################################################
    
    for i in range(number_of_plots):
        ####################################
        ########## Creat a Figure ##########
        ####################################
        
        # Solution according to: https://stackoverflow.com/questions/43805821/matplotlib-add-colorbar-to-non-mappable-object
        ##### Creating a Figure
        fig = plt.figure()
        ##### Set the Size of the Figure by using Centimeters which are tranformed to inches with a function
        fig.set_size_inches(Convert_cm_To_inch(OVERVIEW_W_CM, OVERVIEW_H_CM/0.6)) # was: Convert_cm_To_inch(24, 12); axes below are 1.0 x 0.6 of the figure
        ##### Use of the Defined Paramterts for Font, Font Size, .....
        plt.rcParams.update(pgf_with_latex)
        ##### Create one axis at a certain position
        frame = fig.add_axes((.1,.3,1.0,0.6))
           
        #############################################
        ########## Define the X and Y Data ##########
        #############################################
        
        ##### Define the X-Data
        x = data[i][list_of_x_axis_names[i]]
        
        ##### Create a List for multiple Y-Data
        list_of_y_data = []
        ##### Fill the List with multiple Y-Data
        for n in range(0, len(list_of_list_with_y_axis_names[i])):
            y = data[i][list_of_list_with_y_axis_names[i][n]]
            list_of_y_data.append(y)
        
        ###################################################################
        ########## Define which colormap form Matplotlib is used ##########
        ###################################################################
        ##### defines the name of the colormap used and how many colors are selcted
        colormap = my_colormap # was 'coolwarm'
        number_of_points_for_cmap = len(list_of_y_data)
        cmap = colormap.resampled(number_of_points_for_cmap) # defining which colormap is used and how many colorpoints are collected
        
        ##########################################################
        ########## Creating Y-Graph/Plotted Data Labels ##########
        ##########################################################
        ##### creating labels 
        list_of_labels = []
        list_of_ticks_label_colormap = []
        for j in range(0, len(list_of_y_data)):
            y_name = list_of_list_with_y_axis_names[i][j]
            list_of_ticks_label_colormap.append(y_name)
            datapoints = len(list_of_y_data[j])
            y_min = list_of_y_data[j].min()
            y_max = list_of_y_data[j].max()
            label = 'Curve: %s ; Datapoints: %s ; Y_range: from %s to %s' %(y_name, datapoints, y_min, y_max)
            list_of_labels.append(label)
        
        ###########################################
        ########## Creating the Y-Graphs ##########
        ###########################################
        ##### plotting with a regular colormap from matplotlib
        if list_of_list_of_list_with_y_curve_style[i][0][0] == 'cmap':
            for k in range(0, len(list_of_list_with_y_axis_names[i])):
                alpha_style = list_of_list_of_list_with_y_curve_style[i][k][1]
                marker_style = list_of_list_of_list_with_y_curve_style[i][k][2]
                markersize_style = list_of_list_of_list_with_y_curve_style[i][k][3]
                linestyle_style = list_of_list_of_list_with_y_curve_style[i][k][4] 
                linewidth_style = list_of_list_of_list_with_y_curve_style[i][k][5]
                plt.plot(x, list_of_y_data[k], c=cmap(k),alpha=alpha_style, marker=marker_style, markersize=markersize_style, markeredgecolor='black', markeredgewidth=0.1, label=list_of_labels[k], linestyle=linestyle_style, linewidth=linewidth_style)
                plt.fill(x, list_of_y_data[k], c=cmap(k), alpha=0.3)
        ##### plotting with a user defined colormap from the user input
        else:
            #####################################################
            ########## Define Colormap from User Input ##########
            #####################################################
            
            ##### Create Color Gradient with for loop 
            ##### Selecteable colors: https://www.w3.org/TR/css-color-3/#svg-color
            list_of_colors = []
            for k in range(0, len(list_of_list_with_y_axis_names[i])):
                ##### Select all Selected Colors by the user in one list
                selected_color = list_of_list_of_list_with_y_curve_style[i][k][0]
                list_of_colors.append(selected_color)
            
            color_gradient = []
            if len(list_of_colors) == 1:
                ##### When only one Color is given the Color gradient is created out of this one color
                single_color = Color(list_of_colors[0])
                color_gradient.append(single_color)
            else:
                ##### Creating the Color gradient out of the user input
                for y in range(0, (len(list_of_colors)-1)):
                    ##### Color gradient can only be created out of two color --> Meaning multiple iteration of creation is needed to create a complete custom color gradient
                    start_color = Color(list_of_colors[y])
                    end_color = Color(list_of_colors[y+1])
                    ##### Create a temporary colour gradient
                    color_gradient_temp = list(start_color.range_to(end_color,2))
                    if y == 0:
                        color_gradient = color_gradient + color_gradient_temp
                    else:
                        color_gradient = color_gradient + color_gradient_temp[1:]
        
            print('The selected color gradient is: %s' %(color_gradient))
            
            ###### transfoms the color names into hex code and than to RGBA arrays
            for j in range(0, len(color_gradient)):
                ##### transform the colornames into hex code
                color_temp = color_gradient[j].hex
                ##### transforms the hex coded colors inta RGBA values
                color_as_RGBA = matplotlib.colors.to_rgba(color_temp, alpha=1)
                color_gradient[j] = color_as_RGBA
            
            ##### transfroms the list of RGBA values to a matplotlib colormap
            color_gradient_as_cmap = ListedColormap(color_gradient)
            
            ###########################################
            ########## Creating the Y-Graphs ##########
            ###########################################
            ##### plotting the data with the defiend color gradient:
            for k in range(0, len(list_of_list_with_y_axis_names[i])):
                alpha_style = list_of_list_of_list_with_y_curve_style[i][k][1]
                marker_style = list_of_list_of_list_with_y_curve_style[i][k][2]
                markersize_style = list_of_list_of_list_with_y_curve_style[i][k][3]
                linestyle_style = list_of_list_of_list_with_y_curve_style[i][k][4] 
                linewidth_style = list_of_list_of_list_with_y_curve_style[i][k][5]
                plt.plot(x, list_of_y_data[k], c=color_gradient_as_cmap(k), alpha=alpha_style, marker=marker_style, markersize=markersize_style, markeredgecolor='black', markeredgewidth=0.1, label=list_of_labels[k], linestyle=linestyle_style, linewidth=linewidth_style)
        
        ########################################################################
        ########## Creating additional Lines and Text in the Figures  ##########
        ########################################################################
        ##### plotting lines and text
        if text_and_lines == 'Yes':
            for k in range(0, len(list_of_list_for_vlines_and_text)):
                ##### Use of the defined Paramerters
                #Format used: [x=284.8, color = 'grey', linewidth=1, linestyle='--', label='Carbon C-C sp3']
                x_line = list_of_list_for_vlines_and_text[k][0]
                color_line = list_of_list_for_vlines_and_text[k][1]
                linewidth_line = list_of_list_for_vlines_and_text[k][2]
                linestyle_line = list_of_list_for_vlines_and_text[k][3]
                text = list_of_list_for_vlines_and_text[k][4]
                ##### Plot vertical line which go over the complete plot in the vertical space
                plt.axvline(x=x_line, color = color_line, linewidth=linewidth_line, linestyle=linestyle_line)
                ##### 
                trans = frame.get_xaxis_transform()
                ##### Plot Text in the Figure 
                plt.text((x_line+0.1), .5, text, rotation=90, verticalalignment='center', transform=trans)
        
        #####################################################################
        ########## Creating the Colorbar with the defined colormap ##########
        #####################################################################
        ##### Defining that a colorbar is plotted according to the defined colormap
        if list_of_list_of_list_with_y_curve_style[i][0][0] == 'cmap':
            sm = plt.cm.ScalarMappable(cmap=cmap) ##### defining that the colomap is used for mappable
        else:
            sm = plt.cm.ScalarMappable(cmap=color_gradient_as_cmap)
        
        ###############################################################################
        ########## Plotting the Colorbar and creating the Tick labels #################
        ###############################################################################
        ##### Deleting the Tick labels from the colorbar
        sm.set_array([])
    
        ##### Define the Position of the Tick labels according to the number of colors in the colorbar
        list_of_ticks_colormap = []
        for l in range(1, number_of_points_for_cmap + 1):
            if l == 1:
                tick = ((1/number_of_points_for_cmap)/2) * l
                list_of_ticks_colormap.append(tick)
            elif l == number_of_points_for_cmap:
                tick = 1-((1/number_of_points_for_cmap)/2)
                list_of_ticks_colormap.append(tick)
            else:
                tick = ((1/number_of_points_for_cmap)/2) * (l+(l-1))
                list_of_ticks_colormap.append(tick)
        
        ##### Define Colorbar label
        colormap_label = ''
        
        ##### Plot the Colorbar
        cbar = plt.colorbar(sm, ax=plt.gca(), ticks=list_of_ticks_colormap, label=colormap_label) # defining which mappable is plottet as colorbar and which ticks and label
        
        ##### Create the new Tick labels for the Colorbar
        if len(list_of_list_with_y_curve_labels) != number_of_plots:  
            cbar.ax.set_yticklabels(list_of_ticks_label_colormap) # changes the label of the ticks
        else:
            cbar.ax.set_yticklabels(list_of_list_with_y_curve_labels[i]) # changes the label of the ticks
        
        ######################################################
        ########## Creating the X and Y-Axis Labels ##########
        ######################################################
        ##### Scientific label format changing from 1e1 to 1x10^1 (alternativ method: https://stackoverflow.com/questions/31517156/adjust-exponent-text-after-setting-scientific-limits-on-matplotlib-axis)
        mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
        mf.set_powerlimits((-4,4))
        frame.yaxis.set_major_formatter(mf)
        frame.xaxis.set_major_formatter(mf)

        ##### Defining the Y-axis
        y_ax_label = list_of_y_axis_labels[i]
        frame.set_ylabel(y_ax_label)                 # Label of the y axis
        #frame.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
        #frame.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
        
        ##### Define the X-Axis
        x_ax_label = list_of_x_axis_labels[i]
        frame.set_xlabel(x_ax_label)                                              # Label of the x axis
        #frame.set_xscale('log')
        #frame.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        #frame.set_xticks([])                               # which values are shown on the x axis
    
        ###############################################
        ########## Saving the created Figure ##########
        ###############################################
        ##### Saving otpions
        if saving == 'Yes' or saving == '':
            print('----------------- \nstarting plotting number %s' %(i+1))
            plt.savefig('./%s.png' %(list_of_plot_names[i]))
            print('finished plotting number %s\n------------------' %(i+1))
        
        #######################################################
        ########## Creating the Legend of the Figure ##########
        #######################################################
        
        legend_title = 'XPS Spectra + Components'
        legend = frame.legend(title= legend_title                                     # show the legend of the labelled plots
            ,loc='lower left' 
            ,bbox_to_anchor=(0., 1.02, 1., .102)                           # Position of the legend
            #,ncol=1
            #,mode="expand"
            #,borderaxespad=0.
            )
    
    return plt.show(block=True)


def Matplotlib_XPS_Spectra_Plot(a, b, c, d, e, f, g, h, i, j):
    """XPS spectra: several y columns of one dataframe against binding energy, saved and shown.
    a = dataframe, b = x column, c = list of y columns, d = colours, e/f = x/y limits, g = y scale, h/i = x/y axis label, j = file path."""
    ### Functions needed from other Package
    
    ### Define Parameters
    Dataframe = a
    x_column_name = b
    list_of_y_column_names = c
    list_of_colors = d
    XLims = e
    YLims = f
    YScale = g
    XAxis_Label = h
    YAxis_Label = i
    Filepath_for_saving = j
    
    ### Define different Plotparameters
    PlotParameters = {                      # setup matplotlib to use latex for output
    "text.usetex": False,                # use LaTeX to write all text
    #"mathtext.fontset": "stixsans",
    "legend.title_fontsize" : 14,
    "legend.fontsize": 10,              # Make the legend/label fonts a little smaller
    "axes.labelsize": 12,               # LaTeX default == 10pt font.
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.figsize" : Convert_cm_To_inch(3*6, 3*4),
    'savefig.dpi'         : 300,   ## figure dots per inch or 'figure'
    'savefig.facecolor'   : 'white',    ## figure facecolor when saving
    'savefig.edgecolor'   : 'white',    ## figure edgecolor when saving
    'savefig.format'      : 'png',      ## png, ps, pdf, svg
    'savefig.bbox'        : 'tight' 
    }
    ##### Creating a Figure
    fig = plt.figure()
    
    ##### Use of the Defined Paramterts for Font, Font Size, .....
    plt.rcParams.update(PlotParameters)
    plt.rcParams.update(pgf_with_latex) # publication style (one style for all plots) overrides the old font sizes and figure size
    
    ##### Create one axis at a certain position
    frame = fig.add_axes((.1,.3,1.0,0.6))
    
    ### Plot Options
    for i in range(len(list_of_y_column_names)):
        plt.plot(Dataframe[x_column_name], Dataframe[list_of_y_column_names[i]], label=list_of_y_column_names[i], color=list_of_colors[i], alpha=0.75, marker='.', markersize=2.0, markeredgecolor='black', markeredgewidth=0.1, linestyle='-', linewidth=1.5)
    
    ### Scientific label format changing from 1e1 to 1x10^1 (alternativ method: https://stackoverflow.com/questions/31517156/adjust-exponent-text-after-setting-scientific-limits-on-matplotlib-axis)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-4,4))
    frame.yaxis.set_major_formatter(mf)
    frame.xaxis.set_major_formatter(mf)
    
    ### X Axis Options
    frame.invert_xaxis()
    frame.set_xlim(XLims) 
    frame.set_xticks([])
    frame.set_xticklabels([])
    frame.set_xlabel(XAxis_Label) # Label of the x axis
    
    ### Y Axis Options
    frame.set_yscale(YScale)
    frame.set_ylim(YLims)
    frame.set_yticks([])
    frame.set_yticklabels([])
    frame.set_ylabel(YAxis_Label) 
      
    
    ### Save Figure
    plt.savefig(Filepath_for_saving)
    
    ### Create a Legend
    legend = frame.legend(title=None # show the legend of the labelled plots
    ,loc='lower left' 
    ,bbox_to_anchor=(0., 1.02, 1., .102)                           # Position of the legend
    #,ncol=1
    #,mode="expand"
    #,borderaxespad=0.
    )
    
    ### Show Figure
    plt.show()
    
    return


def Plotly_XPS_Surface_Spectra_Plot(a, b, c, d, e, f, g, h, i, j):
    """Interactive XPS spectrum with fitted components (filled), background and raw data; binding energy axis reversed; saved as html.
    a = dataframe, b = x column, c = raw data column, d = list of component columns, e = background column, f = curve label,
    g = colours, h/i = x/y axis label, j = html file path."""
    #### Define Parameters
    dataframe = a
    x_column_name = b
    y_column_name_raw_data = c
    list_of_y_column_names_components = d
    y_column_name_background = e
    curve_label = f
    list_of_colors = g
    XAxis_Label = h
    YAxis_Label = i
    Filepath_for_saving = j

    ##### Define Figure
    # 1. Wrap the Plotly-Figure with the FigureResampler
    fig = go.Figure()
    
    #Plotting Components
    for i in range(len(list_of_y_column_names_components)):
        fig.add_scatter(
            x=dataframe[x_column_name], 
            y=dataframe[y_column_name_background], 
            name='Background', 
            mode='lines',  # set the mode to 'markers+lines'
            showlegend=False,
            #visible='legendonly',
            line=dict(
                color='grey',  # set the line colour to red
                width=0.1,  # set the line width to 2
                dash='solid'  
            )
            )
        
        fig.add_scatter(
            x=dataframe[x_column_name], 
            y=dataframe[list_of_y_column_names_components[i]], 
            name=list_of_y_column_names_components[i], 
            mode='lines',  # set the mode to 'markers+lines'
            fill="tonextx",
            line=dict(
                color=list_of_colors[i+1],  # set the line colour to red
                width=2,  # set the line width to 2
                dash='solid'  
            )
            )
    
    #Plotting Background
    fig.add_scatter(
        x=dataframe[x_column_name], 
        y=dataframe[y_column_name_background], 
        name='Background', 
        mode='lines',  # set the mode to 'markers+lines'
        line=dict(
            color='grey',  # set the line colour to red
            width=2,  # set the line width to 2
            dash='solid'  
        )
        )
    
    #Plotting Raw Data
    fig.add_scatter(
        x=dataframe[x_column_name], 
        y=dataframe[y_column_name_raw_data], 
        name='Raw Data', 
        mode='lines',  # set the mode to 'markers+lines'
        line=dict(
            color=list_of_colors[0],  # set the line colour to red
            width=2,  # set the line width to 2
            dash='solid'  
        )
        )

    fig.update_xaxes(autorange='reversed')
    
    ##### Change Visual Layout of the Plot: publication style, size and legend are set in publication_plotly.py
    apply_style(fig, XAxis_Label, YAxis_Label, plot_w_cm=OVERVIEW_W_CM, plot_h_cm=OVERVIEW_H_CM,
                x_tickformat='uniform', y_tickformat='uniform', showlegend=SHOW_LEGEND)

    # Save Plot as interactive html Plot
    fig.write_html(Filepath_for_saving) # images_outdir + "Comparing_specCapacites" + ".html"

    fig.show()


def Plotly_XPS_Multiple_Dataframes(a, b, c, d, e, f, g, h):
    """Interactive plot of several XPS spectra (e.g. a depth profile; offsets for stacking are added before, e.g. with Offset_Dataframes), binding energy axis reversed, no y tick labels;
    saved as <h>.html without legend, shown with legend.
    a = list of dataframes, b = x column per dataframe, c = raw data column per dataframe, d = curve labels, e = colours, f/g = axis labels, h = file path without ending."""
    #### Define Parameters
    list_of_dataframes = a
    list_of_x_column_names = b
    list_of_y_column_name_raw_data = c
    list_of_curve_label = d
    list_of_colors = e
    XAxis_Label = f
    YAxis_Label = g
    Filepath_for_saving = h

    ##### Define Figure
    # 1. Wrap the Plotly-Figure with the FigureResampler
    fig = go.Figure()
    
    for j in range((len(list_of_dataframes))):
        #print(j)
        #Plotting Raw Data
        fig.add_scatter(
            x=list_of_dataframes[j][list_of_x_column_names[j]], 
            y=list_of_dataframes[j][list_of_y_column_name_raw_data[j]], 
            name=list_of_curve_label[j], 
            mode='lines',  # set the mode to 'markers+lines'
            line=dict(
                color=list_of_colors[j],  # set the line colour to red
                width=2,  # set the line width to 2
                dash='solid'  
            )
            )

    fig.update_xaxes(autorange='reversed')
    
    ##### Change Visual Layout of the Plot: publication style, size and legend are set in publication_plotly.py
    apply_style(fig, XAxis_Label, YAxis_Label, plot_w_cm=OVERVIEW_W_CM, plot_h_cm=OVERVIEW_H_CM,
                x_tickformat='uniform', y_tickformat=None, y_ticklabels=False, showlegend=SHOW_LEGEND)

    # Save Plot as interactive html Plot
    fig.update_layout(showlegend=False)
    fig.write_html(Filepath_for_saving + ".html") # images_outdir + "Comparing_specCapacites" + ".html"

    #fig.update_layout(showlegend=False)
    #fig.write_image(Filepath_for_saving + ".svg")

    fig.update_layout(showlegend=True)
    fig.show()


def Plotly_XPS_DepthProfil_Spectra_Plot(a, b, c, d, e, f, g, h, i, j):
    """Like Plotly_XPS_Multiple_Dataframes, with the fitted components (filled) and background of every spectrum; saved as <j>.html and <j>.svg.
    a = list of dataframes, b = x columns, c = raw data columns, d = list of lists of component columns, e = background columns,
    f = curve labels, g = colours, h/i = axis labels, j = file path without ending."""
    #### Define Parameters
    list_of_dataframes = a
    list_of_x_column_names = b
    list_of_y_column_name_raw_data = c
    list_of_list_of_y_column_names_components = d
    list_of_y_column_name_background = e
    list_of_curve_label = f
    list_of_colors = g
    XAxis_Label = h
    YAxis_Label = i
    Filepath_for_saving = j

    ##### Define Figure
    # 1. Wrap the Plotly-Figure with the FigureResampler
    fig = go.Figure()
    
    for j in range(len(list_of_dataframes)):
        
        dataframe = list_of_dataframes[j]
        
        #Plotting Components
        for i in range(len(list_of_list_of_y_column_names_components[j])):
            if len(list_of_y_column_name_background) > 1:
                fig.add_scatter(
                    x=dataframe[list_of_x_column_names[j]], 
                    y=dataframe[list_of_y_column_name_background[j]], 
                    name='Background', 
                    mode='lines',  # set the mode to 'markers+lines'
                    showlegend=False,
                    #visible='legendonly',
                    line=dict(
                        color='grey',  # set the line colour to red
                        width=0.1,  # set the line width to 2
                        dash='solid'  
                    )
                    )
        
            fig.add_scatter(
                x=dataframe[list_of_x_column_names[j]], 
                y=dataframe[list_of_list_of_y_column_names_components[j][i]], 
                name=list_of_list_of_y_column_names_components[j][i], 
                mode='lines',  # set the mode to 'markers+lines'
                fill="tonextx",
                line=dict(
                    color=list_of_colors[i+1],  # set the line colour to red
                    width=2,  # set the line width to 2
                    dash='solid'  
                )
                )
    
        #Plotting Background
        if len(list_of_y_column_name_background) > 1:
            fig.add_scatter(
                x=dataframe[list_of_x_column_names[j]], 
                y=dataframe[list_of_y_column_name_background[j]],
                name='Background', 
                mode='lines',  # set the mode to 'markers+lines'
                line=dict(
                    color='grey',  # set the line colour to red
                    width=2,  # set the line width to 2
                    dash='solid'  
                )
                )
    
        #Plotting Raw Data
        fig.add_scatter(
            x=dataframe[list_of_x_column_names[j]], 
            y=dataframe[list_of_y_column_name_raw_data[j]], 
            name='Raw Data', 
            mode='lines',  # set the mode to 'markers+lines'
            line=dict(
                color=list_of_colors[0],  # set the line colour to red
                width=2,  # set the line width to 2
                dash='solid'  
            )
            )

    fig.update_xaxes(autorange='reversed')
    
    ##### Change Visual Layout of the Plot: publication style, size and legend are set in publication_plotly.py
    apply_style(fig, XAxis_Label, YAxis_Label, plot_w_cm=OVERVIEW_W_CM, plot_h_cm=OVERVIEW_H_CM,
                x_tickformat='uniform', y_tickformat=None, y_ticklabels=False, showlegend=SHOW_LEGEND)

    # Save Plot as interactive html Plot
    fig.write_html(Filepath_for_saving + ".html") # images_outdir + "Comparing_specCapacites" + ".html"

    fig.update_layout(showlegend=False)
    fig.write_image(Filepath_for_saving + ".svg")

    fig.update_layout(showlegend=True)
    fig.show()
