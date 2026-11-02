"""Depth profiles, box plots and mass spectra."""

from colour import Color
from plotly_resampler import FigureResampler
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker

from scientific_utils.general.plotting import Convert_cm_To_inch
from scientific_utils.general.plotting import my_colormap
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.general.plotting import pgf_with_latex
from scientific_utils.general.plotting import Matplotlib_Legend_Above_And_Save, Matplotlib_New_Figure_With_Frame, Set_Scientific_Tick_Labels, Has_Offset_Text
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style
from scientific_utils.publication_plotly import cm, pt, MARGIN, FONT_PT, TICK_FONT_PT, ANNOT_FONT_PT, LEGEND_FONT_PT


def Matplotlib_SputterProfile_Overview_With_Colormap(dataframe, x_values_column_name, y_values_column_name, lis_of_ticks_label_colormap , y_ax_label, x_ax_label, save, name_figure, legend_title, y_values_column_names):
    """All ion columns of a sputter profile (x relative to its first value) in one plot, coloured with my_colormap, with colour bar.
    dataframe ('Unnamed' columns are dropped), x_values_column_name, y_values_column_names = column names (the first one is skipped),
    lis_of_ticks_label_colormap = tick labels of the colour bar, save = 1 -> ./images/Overview_<name_figure>.png. (y_values_column_name is not used.)"""
    # Solution according to: https://stackoverflow.com/questions/43805821/matplotlib-add-colorbar-to-non-mappable-object
    fig, frame = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig.set_size_inches(cm2inch(8, 4))

    
    # clean the dataframe from columns which have no name
    dataframe_cleaned = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
    
    number_of_points = len(dataframe_cleaned.columns) - 1

    cmap = my_colormap.resampled(number_of_points) # defining which colormap is used and how many colorpoints are collected

    for n,i in enumerate(range(1, len(dataframe_cleaned.columns))):
        x = (dataframe_cleaned[x_values_column_name] - dataframe_cleaned.iloc[0][x_values_column_name])
        y = dataframe_cleaned[y_values_column_names[i]]

        # no legend entry per curve: the colour bar shows the ions
        plt.plot(x, y, c=cmap(n), linestyle='None', alpha=0.5, marker='.', linewidth=1.5)

    # Defining that a colorbar is plotted according to the defined colormap
    sm = plt.cm.ScalarMappable(cmap=cmap) # defining that the colomap is used for mappable
    sm.set_array([])
    
    list_of_ticks_colormap = []
    for i in range(1, number_of_points + 1):
        if i == 1:
            tick = ((1/number_of_points)/2) * i
            list_of_ticks_colormap.append(tick)
        elif i == number_of_points:
            tick = 1-((1/number_of_points)/2)
            list_of_ticks_colormap.append(tick)
        else:
            tick = ((1/number_of_points)/2) * (i+(i-1))
            list_of_ticks_colormap.append(tick)
    
    cbar = plt.colorbar(sm, ax=plt.gca(), ticks=list_of_ticks_colormap, label=r'$detected$ $ions$') # defining which mappable is plottet as colorbar and which ticks and label
    cbar.ax.set_yticklabels(lis_of_ticks_label_colormap ) # changes the label of the ticks
    

    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame, (-2,2))

    # Defining the axis
    frame.set_ylabel(y_ax_label)                 # Label of the y axis
    #frame.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    
    frame.set_xlabel(x_ax_label)                                              # Label of the x axis
    #frame.set_xscale('log')
    #frame.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame.set_xticks([])                               # which values are shown on the x axis
    
    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame, legend_title, save, './images/Overview_%s.png' %(name_figure))
    
    plot = plt.show(block=False)
    
    return plot


def Matplotlib_BoxPlot(a, b, c, d, e, show_plot=True):
    """Box plot of several data series, saved and shown.
    a = list of series, b = y axis label, c = x axis label, d = sample names (x tick labels), e = file path. show_plot = False -> only saved, not shown."""
    ### Functions needed from other Package
    
    ### Define Parameters
    List_of_DataSeries = a
    YAxis_Label = b
    XAxis_Label = c
    List_of_Sample_Names = d
    Filepath_for_saving = e
    
    ### Define different Plotparameters
    PlotParameters = {                      # setup matplotlib to use latex for output
    "text.usetex": False,                # use LaTeX to write all text
    #"mathtext.fontset": "stixsans",
    "legend.title_fontsize" : 14,
    "legend.fontsize": 10,              # Make the legend/label fonts a little smaller
    "axes.labelsize": 12,               # LaTeX default == 10pt font.
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.figsize" : Convert_cm_To_inch(1*10, 1*8),
    'savefig.dpi'         : 300,   ## figure dots per inch or 'figure'
    'savefig.facecolor'   : 'white',    ## figure facecolor when saving
    'savefig.edgecolor'   : 'white',    ## figure edgecolor when saving
    'savefig.format'      : 'png',      ## png, ps, pdf, svg
    'savefig.bbox'        : 'tight' 
    }
    
    fig, ax = plt.subplots()
    
    plt.rcParams.update(PlotParameters)
    plt.rcParams.update(pgf_with_latex) # publication style (one style for all plots) overrides the old font sizes and figure size
    ##### Set the Size of the Figure by using Centimeters which are tranformed to inches with a function
    Set_Figure_Size_For_Plot_Area(fig) # was: fig.set_size_inches(Convert_cm_To_inch(10, 8))
    
    ### Plot Options
    ax.boxplot(List_of_DataSeries)
    
    ### Axis Options
    ax.set_ylabel(YAxis_Label)  # Label of the y axis
    
    number_of_samples_as_list = list(np.arange(1, (len(List_of_DataSeries)+1), 1))
    ax.set_xticks(number_of_samples_as_list, List_of_Sample_Names, rotation = 45, ha='right')
    ax.set_xlabel(XAxis_Label) # Label of the x axis
    
    ### Save Figure
    plt.savefig(Filepath_for_saving)
    
    ### Show Figure (or only close it, when the saved file is enough)
    if show_plot == True:
        plt.show()
    else:
        plt.close(fig)
    
    return


def Matplotlib_DepthProfil(a, b, c, d, e, f, g, h, i, j):
    """Depth profile: several ion columns against sputter time / fluence, saved and shown.
    a = dataframe, b = x column, c = list of y columns, d = colours, e/f = x/y limits, g = y scale ('linear'/'log'), h/i = x/y axis label, j = file path."""
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
    "figure.figsize" : Convert_cm_To_inch(1*6, 1*4),
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
    
    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame, (-4,4))
    
    ### X Axis Options
    frame.set_xlim(XLims) 
    frame.set_xlabel(XAxis_Label) # Label of the x axis
    
    ### Y Axis Options
    frame.set_ylim(YLims) 
    frame.set_ylabel(YAxis_Label) 
    frame.set_yscale(YScale)  
    
    ### Create a Legend
    legend = frame.legend(title=None # show the legend of the labelled plots
    ,loc='lower left'
    ,bbox_to_anchor=(0., 1.02, 1., .102)                           # Position of the legend
    #,ncol=1
    #,mode="expand"
    #,borderaxespad=0.
    )

    ### Save Figure (after the legend, so it is in the saved file)
    plt.savefig(Filepath_for_saving)

    ### Show Figure
    plt.show()
    
    return


def Plotly_DepthProfil(a, b, c , d, e, f, g, h):
    """Interactive depth profile (publication style), saved as <h>.html without legend, shown with legend.
    a = dataframe, b = x column, c = list of y columns, d = curve labels, e = colours, f/g = x/y axis label, h = file path without ending."""
    
    # Define Variables
    Dataframe = a
    x_column_name = b
    list_of_y_column_names = c
    list_of_curve_label = d
    list_of_colors = e
    XAxis_Label = f
    YAxis_Label = g
    Filepath_for_saving = h
    
    ##### Define Figure
    fig = go.Figure()
     
    for i in range(len(list_of_y_column_names)):
        ##### Add Scatter plots and change style
        fig.add_scatter(
        x=Dataframe[x_column_name], 
        y=Dataframe[list_of_y_column_names[i]], 
        name=list_of_curve_label[i], 
        mode='markers+lines',  # set the mode to 'markers+lines'
        marker=dict(
            color=list_of_colors[i],  # set the marker colour
            size=4.5,  # set the marker size to 8
            symbol='circle',  # set the marker symbol to circles
            opacity=1.0,  # set the marker opacity to 0.8
            line=dict(width=0.8)  # set the width of the line around the markers
        ),
        line=dict(
            color=list_of_colors[i],  # set the line colour to red
            width=2,  # set the line width to 2
            dash='solid'  
        )
        )
    
    ##### Change Visual Layout of the Plot: publication style, size and legend are set in publication_plotly.py
    apply_style(fig, XAxis_Label, YAxis_Label, plot_w_cm=OVERVIEW_W_CM, plot_h_cm=OVERVIEW_H_CM,
                x_tickformat='uniform', y_tickformat='uniform', showlegend=SHOW_LEGEND)

    # Save Plot as interactive html Plot
    fig.update_layout(showlegend=False)
    fig.write_html(Filepath_for_saving + ".html") # images_outdir + "Comparing_specCapacites" + ".html"

    #fig.update_layout(showlegend=False)
    #fig.write_image(Filepath_for_saving + ".svg")

    fig.update_layout(showlegend=True)

    fig.show()


def Plotly_DepthProfil_Multiple_YAxis(a, b, c, d, e, f, g, h):
    """Depth profile with one coloured y axis per ion (axes next to each other on the left), saved as <h>.html.
    a = dataframe, b = x column, c = list of y columns (up to 4), d = curve labels (also the y axis titles), e = colours, f = x axis label, g = not used, h = file path without ending."""
    # Variables
    Dataframe = a
    x_column_name = b
    list_of_y_column_names = c
    list_of_curve_label = d
    list_of_colors = e
    XAxis_Label = f
    Filepath_for_saving = h

    # Dimensions (XPS style) -> publication style: the plot area inside the x domain [0.4, 0.95] is OVERVIEW_W_CM x OVERVIEW_H_CM
    # (was width_cm = 15, height_cm = 6, DPI_screen = 119)
    width_px = round(cm(OVERVIEW_W_CM) / 0.55) + 20      # 0.55 = width of the x domain, 20 = left + right margin
    height_px = round(cm(OVERVIEW_H_CM)) + MARGIN['t'] + MARGIN['b']

    fig = go.Figure()

    # 1. Add the data traces
    for i in range(len(list_of_y_column_names)):
        fig.add_trace(go.Scatter(
            x=Dataframe[x_column_name],
            y=Dataframe[list_of_y_column_names[i]],
            name=list_of_curve_label[i],
            yaxis=f"y{i+1}",
            mode='markers+lines',
            marker=dict(color=list_of_colors[i], size=4),
            line=dict(width=1.5)
        ))

    # 2. THE TRICK: an empty trace for the right axis to force the line
    mirror_axis_id = len(list_of_y_column_names) + 1
    fig.add_trace(go.Scatter(
        x=[None], y=[None], 
        yaxis=f"y{mirror_axis_id}", 
        showlegend=False
    ))

    # 3. Configure the layout
    layout_dict = {
        'width': width_px,
        'height': height_px,
        'autosize': False,
        'margin': dict(l=10, r=10, t=MARGIN['t'], b=MARGIN['b']),   # was t=10, b=10 (room for the x axis title)
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'showlegend': False,
        'font': dict(family='Arial', size=pt(FONT_PT), color='black'),   # was size=11 (px)
        'xaxis': dict(
            title=XAxis_Label,
            domain=[0.4, 0.95], # Space on the left for the y axes (was [0.3, 0.9]; more room for the larger publication fonts)
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True, # Draws the top line
            ticks='inside',
            ticklen=5,
            tickwidth=2,
            minor=dict(ticks='inside', ticklen=3, tickwidth=1),
            title_font=dict(size=pt(FONT_PT)),
            tickfont=dict(size=pt(TICK_FONT_PT)),
            automargin=False,      # fixed margins -> fixed plot area
            exponentformat='power'
        )
    }

    # 4. Define all y axes (left) and the mirror axis (right)
    for i in range(len(list_of_y_column_names)):
        axis_key = f'yaxis{i+1}' if i > 0 else 'yaxis'
        layout_dict[axis_key] = dict(
            title=dict(text=list_of_curve_label[i], font=dict(color=list_of_colors[i], size=pt(ANNOT_FONT_PT)), standoff=2),   # was size=10 (px)
            tickfont=dict(color=list_of_colors[i], size=pt(LEGEND_FONT_PT)),   # was size=9 (px); small, the y axes stand close together
            ticks='inside',
            ticklen=5,
            tickwidth=2,   # was 1.5
            showline=True,
            linewidth=2,
            linecolor=list_of_colors[i],
            anchor="free" if i > 0 else "x",
            overlaying="y" if i > 0 else None,
            side="left",
            position=0.4 - (i * 0.12) if i > 0 else None,   # was 0.3 - (i * 0.08)
            exponentformat='power'
        )

    # Finish the right mirror axis
    layout_dict[f'yaxis{mirror_axis_id}'] = dict(
        side="right",
        overlaying="y",
        anchor="x",
        showline=True,
        linewidth=2,
        linecolor='black', # right box line black
        ticks='inside',
        ticklen=5,
        tickwidth=2,
        showticklabels=False
    )

    fig.update_layout(**layout_dict)

    # Save and show
    fig.write_html(Filepath_for_saving + ".html")
    fig.show()


def Matplotlib_Interactive_SputterProfile_Plot(list_of_dataframes, input_parameters_Plot):
    """Several configurable sputter profile plots in one call; everything is set in the dictionary input_parameters_Plot
    (number_of_plots, x/y column names, axis labels and styles, colour bar options, curve labels and styles, area filling, vertical lines with text,
    saving options -> ./images/<name>.png). Every list needs one entry per plot (otherwise only a warning is printed).
    list_of_dataframes = data, one dataframe per plot."""
    #############################################
    ########## Define What Data to use ##########
    #############################################
    
    ##### Define which list of dataframe is used #####
    data = list_of_dataframes
    print('The Dataframe with the variable name %s is used.' %'raw_data')
    print('The option to change the name of the variable dynamically is missing here!')
    
    ##### Look how many dataframes / measurements files are in the list #####
    print('---------------------------')
    print('There are %s different dataframes in the loaded data list' %(len(data)))
    print('---------------------------')
    
    ##### The Column names of the Dataframes are #####
    list_of_column_names = []
    for i in range(len(data)):
        list_of_column_names.append(data[i].columns)
        print(list_of_column_names[i])
    
    ################################################
    ########## Define the number of Plots ##########
    ################################################

    ##### Use the Input saved in the dictonary befor
    number_of_plots = int(input_parameters_Plot.get('number_of_plots'))
    print('-------------------')
    print('Creating %s plots' %(number_of_plots))
    print('-------------------')
    
    
    ###############################################
    ########## Define which X-Axis used  ##########
    ###############################################
    
    ##### Select the Name of the X-Axis for the different plots #####
    list_of_x_axis_names = []
    
    ##### Use the Dictonary Entry
    list_of_x_axis_names = input_parameters_Plot.get('list_of_x_axis_names')
    
    ##### Error Message  
    if len(list_of_x_axis_names) == number_of_plots:
        print('-------------------')
        print('The following X-Axis for the %s differnt plots are selected: %s' %(number_of_plots, list_of_x_axis_names))
        print('-------------------')
    elif len(list_of_x_axis_names) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('-------------------')
    
    ##############################################
    ########## Define which Y-Axis used ##########
    ##############################################
        
    ##### Defining an empty List for list of Y-Axis names
    list_of_list_with_y_axis_names = []
    
    ##### Select the Y-Axis for plotting; List of List is used because every Plot can have multiply Y Columns plotted
    list_of_list_with_y_axis_names = input_parameters_Plot.get('list_of_list_with_y_axis_names')
    
    ##### Error Message  
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
    list_of_list_for_saving_options = []
    
    list_of_list_for_saving_options = input_parameters_Plot.get('list_of_list_for_saving_options')

    ########################################################################################
    ################################### Plotting Options ###################################
    ########################################################################################
    
    ########################### Options for every plot #####################################
    
    ############################################
    ########## Define X-Axis Labeling ##########
    ############################################
    ##### Define an empty list for the X-Axis labels shown in the final plot
    list_of_x_axis_labels = []
    
    ##### Use the List our of the dictonary for the X Axis label
    list_of_x_axis_labels = input_parameters_Plot.get('list_of_x_axis_labels')

    ##### Error Message  
    if len(list_of_x_axis_labels) == number_of_plots:
        print('-------------------')
        print('The following X-Axis for the %s differnt plots are selected: %s' %(number_of_plots, list_of_x_axis_labels))
        print('-------------------')
    elif len(list_of_x_axis_labels) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('-------------------')
    
    ############################################
    ########## Define Y-Axis Labeling ##########
    ############################################
    
    ##### Defining an empty List for the Y-Axis label
    list_of_y_axis_labels = []
    
    ##### Use the List our of the dictonary for the Y Axis Label
    list_of_y_axis_labels = input_parameters_Plot.get('list_of_y_axis_labels')
    
    ##### Error Message  
    if len(list_of_y_axis_labels) == number_of_plots:
        print('-------------------')
        print('The following Y-Axis for the %s differnt plots are selected: %s' %(number_of_plots, list_of_y_axis_labels))
        print('-------------------')
    elif len(list_of_y_axis_labels) != number_of_plots:
        print('-------------------')
        print('The number of selected Y-Axis do not match with the number of created plots!!!!')
        print('-------------------')
        
    ####################################################
    ########## Define X-Axis and Y-Axis style ##########
    ####################################################
    ##### Define an empty list for the X-Axis labels shown in the final plot
    list_of_list_of_axis_style_options = []
    
    ##### Use the List our of the dictonary for the Axis plotting style
    list_of_list_of_axis_style_options = input_parameters_Plot.get('list_of_list_of_axis_style_options')

    ##### Error Message    
    if len(list_of_list_of_axis_style_options) == number_of_plots:
        print('-------------------')
        for i in range(number_of_plots):
            print('Axis Style for the %s plot are: %s' %((i+1), list_of_list_of_axis_style_options[i]))
        print('-------------------')
    elif len(list_of_list_of_axis_style_options) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('-------------------')
        
    ###########################################
    ########## Define Colorbar Style ##########
    ###########################################
    ##### Define an empty list for the X-Axis labels shown in the final plot
    list_of_list_with_colorbar_options = []
    
    ##### Use the List our of the dictonary for the Axis plotting style
    list_of_list_with_colorbar_options = input_parameters_Plot.get('list_of_list_with_colorbar_options')
    
    ##### Error Message    
    if len(list_of_list_with_colorbar_options) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('-------------------')
    
        
    ########################### Options for every curve ####################################
    
    #########################################################
    ########## Define Y-Graph/Plotted Data Labeles ##########
    #########################################################
    
    ##### Defining an empty List for Lists of the Graphs/Data Labeling
    list_of_list_with_y_curve_labels = []
    
    ##### Use the List our of the dictonary for the Y-Graph label
    list_of_list_with_y_curve_labels = input_parameters_Plot.get('list_of_list_with_y_curve_labels')
    
    ##### Error Message
    if len(list_of_list_with_y_curve_labels) == number_of_plots:
        print('-------------------')
        for i in range(number_of_plots):
            print('Y-curve labels for the %s plot are: %s' %((i+1), list_of_list_with_y_curve_labels[i]))
        print('-------------------')
    elif len(list_of_list_with_y_curve_labels) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('-------------------')
    
    ############################################################################
    ########## Define Options for Y-Graph/Plotted Data Plotting Style ##########
    ############################################################################
    
    ##### Create a List for List of Parameters which define the Style of the Plottet curve for every Y-Graph
    list_of_list_of_list_with_y_curve_style = []
    
    ##### Use the List our of the dictonary for the Plotting Style of the graphs
    list_of_list_of_list_with_y_curve_style = input_parameters_Plot.get('list_of_list_of_list_with_y_curve_style')
    
    ##### Error Message  
    if len(list_of_list_of_list_with_y_curve_style) == number_of_plots:
        print('-------------------')
        for i in range(number_of_plots):
            print('Y-curve labels for the %s plot are: %s' %((i+1), list_of_list_of_list_with_y_curve_style[i]))
        print('-------------------')
    elif len(list_of_list_of_list_with_y_curve_style) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('-------------------')
        
    ########################################################################
    ########## Define Options for filling area between two curves ##########
    ######################################################################## 
    list_of_list_of_list_with_y_curve_style_area_filling_options = []
    
    ##### Use the List our of the dictonary for the Plotting Style of the graphs
    list_of_list_of_list_with_y_curve_style_area_filling_options = input_parameters_Plot.get('list_of_list_of_list_with_y_curve_style_area_filling_options')
    
    ##### Error Message  
    if len(list_of_list_of_list_with_y_curve_style_area_filling_options) == number_of_plots:
        print('-------------------')
        for i in range(number_of_plots):
            print('Y-curve labels for the %s plot are: %s' %((i+1), list_of_list_of_list_with_y_curve_style_area_filling_options[i]))
        print('-------------------')
    elif len(list_of_list_of_list_with_y_curve_style_area_filling_options) != number_of_plots:
        print('-------------------')
        print('The number of selected X-Axis do not match with the number of created plots!!!!')
        print('-------------------')
    
    ###########################################################################
    ########## Options for additional Lines and Text in the Figures  ##########
    ###########################################################################
    
    ##### Create a List for Parameters for Lines and Text in the Figures
    list_of_list_for_vlines_and_text = []  #Format of one List Entry: [x=284.8, color = 'grey', linewidth=1, linestyle='--', label='Carbon C-C sp3']
    
    ##### Uses pre defined Paramters from the Dictonary for plooting additional line in the plot
    list_of_list_for_vlines_and_text = input_parameters_Plot.get('list_of_list_for_vlines_and_text')

        
    #############################################################################################
    ##################################### Plotting ##############################################
    #############################################################################################
    
    for i in range(number_of_plots):
        ####################################
        ########## Creat a Figure ##########
        ####################################
        
        # Solution according to: https://stackoverflow.com/questions/43805821/matplotlib-add-colorbar-to-non-mappable-object
        ##### Creating a Figure
        fig, frame = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
        ##### Set the Size of the Figure by using Centimeters which are tranformed to inches with a function
        #fig.set_size_inches(cm2inch(24, 12))
           
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
            list_of_labels.append(y_name)
        
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
                if list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][0] == True:
                    selected_curve_index = list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][1]
                    color_area_style = list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][2]
                    alpha_area_style = list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][3]
                    plt.fill_between(x,list_of_y_data[selected_curve_index], list_of_y_data[k], color=color_area_style, alpha=alpha_area_style)
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
                if list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][0] == True:
                    selected_curve_index = list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][1]
                    color_area_style = list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][2]
                    alpha_area_style = list_of_list_of_list_with_y_curve_style_area_filling_options[i][k][3]
                    plt.fill_between(x,list_of_y_data[selected_curve_index], list_of_y_data[k], color=color_area_style, alpha=alpha_area_style)
        ########################################################################
        ########## Creating additional Lines and Text in the Figures  ##########
        ########################################################################
        ##### plotting lines and text
        for k in range(0, len(list_of_list_for_vlines_and_text)):
            if list_of_list_for_vlines_and_text[k][0] == True:
                ##### Use of the defined Paramerters
                #Format used: [x=284.8, color = 'grey', linewidth=1, linestyle='--', label='Carbon C-C sp3']
                x_line = list_of_list_for_vlines_and_text[k][1]
                color_line = list_of_list_for_vlines_and_text[k][2]
                linewidth_line = list_of_list_for_vlines_and_text[k][3]
                linestyle_line = list_of_list_for_vlines_and_text[k][4]
                text = list_of_list_for_vlines_and_text[k][5]
                ##### Plot vertical line which go over the complete plot in the vertical space
                plt.axvline(x=x_line, color = color_line, linewidth=linewidth_line, linestyle=linestyle_line)
                ##### 
                trans = frame.get_xaxis_transform()
                ##### Plot Text in the Figure 
                plt.text((x_line+0.4), .5, text, rotation=90, verticalalignment='center', transform=trans)
        
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

        if list_of_list_with_colorbar_options[i][0] == True:
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
        power_limits = list_of_list_of_axis_style_options[i][0]
        y_lim = list_of_list_of_axis_style_options[i][1]
        y_ticks_enable = list_of_list_of_axis_style_options[i][2]
        y_ticks = list_of_list_of_axis_style_options[i][3]
        x_lim = list_of_list_of_axis_style_options[i][4]
        x_ticks_enable = list_of_list_of_axis_style_options[i][5]
        x_ticks = list_of_list_of_axis_style_options[i][6]

        # Scientific label format changing from 1e1 to 1x10^1
        Set_Scientific_Tick_Labels(frame, power_limits)

        ##### Defining the Y-axis
        y_ax_label = list_of_y_axis_labels[i]
        frame.set_ylabel(y_ax_label)                 # Label of the y axis
        frame.set_ylim(y_lim)                                                             # minimum and maximum value shown on the y axis
        if y_ticks_enable == 'Yes':
            frame.set_yticks(y_ticks)                                        # which values are shown on the y axis
        
        ##### Define the X-Axis
        x_ax_label = list_of_x_axis_labels[i]
        frame.set_xlabel(x_ax_label)                                              # Label of the x axis
        #frame.invert_xaxis() 
        #frame.set_xscale('log')
        frame.set_xlim(x_lim)                                                         # minimum and maximum value shown on the x axis
        if x_ticks_enable == 'Yes':
            frame.set_xticks(x_ticks)                               # which values are shown on the x axis
    
        #######################################################
        ########## Creating the Legend of the Figure ##########
        #######################################################

        legend = frame.legend(title= None                                     # show the legend of the labelled plots
            ,loc='lower left'
            ,bbox_to_anchor=(0., 1.02, 1., .102)                           # Position of the legend
            #,ncol=1
            #,mode="expand"
            ,borderaxespad=1.5 if Has_Offset_Text(frame.yaxis) else 0.5    # higher, so the x10^n text of the y axis stays visible (0.5 = default)
            )

        ###############################################
        ########## Saving the created Figure ##########
        ###############################################
        ##### Saving otpions (after the legend, so it is in the saved file)
        if list_of_list_for_saving_options[i][0] == True:
            print('----------------- \nstarting plotting number %s' %(i+1))
            plt.savefig('./images/%s.png' %(list_of_list_for_saving_options[i][1]))
            print('finished plotting number %s\n------------------' %(i+1))

    return
