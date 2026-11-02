"""Unused functions moved here from `scientific_utils/battery/plotting.py` (nothing in the repository called them)."""

import plotly.graph_objects as go
import math
import matplotlib
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker

from scientific_utils.battery.analysis import Calculate_Ratio_Over_Multiple_Columns
from scientific_utils.general.analysis import Extract_Range_Of_Column_Names
from scientific_utils.general.plotting import Convert_cm_To_inch
from scientific_utils.general.plotting import list_of_Hexcolors
from scientific_utils.general.plotting import my_colormap
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.general.plotting import pgf_with_latex
from scientific_utils.general.plotting import yellow
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style
from scientific_utils.publication_plotly import my_color_scale
from scientific_utils.publication_plotly import pt, FONT_PT, TICK_FONT_PT, LEGEND_FONT_PT


def Matplotlib_EC_Plot(a, b, c, d, e, f, g, h, i, j):
    """Line plot of several y columns of one dataframe, saved and shown.
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
    "figure.figsize" : Convert_cm_To_inch(6*6, 6*4),
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
    frame.set_xlim(XLims) 
    frame.set_xlabel(XAxis_Label) # Label of the x axis
    
    ### Y Axis Options
    frame.set_ylim(YLims) 
    frame.set_ylabel(YAxis_Label) 
    frame.set_yscale(YScale)  
    
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


def Matplotlib_EC_Plot_Multiple_Dataframes(a, b, c, d, e, f, g, h, i, j, k):
    """Like Matplotlib_EC_Plot, but one curve per dataframe and y column.
    a = list of dataframes, b = x column, c = list of y columns, d = curve labels, e = colours, f/g = x/y limits, h = y scale, i/j = labels, k = file path."""
    ### Functions needed from other Package
    
    ### Define Parameters
    list_of_Dataframes = a
    x_column_name = b
    list_of_y_column_names = c
    list_of_curve_label = d
    list_of_colors = e
    XLims = f
    YLims = g
    YScale = h
    XAxis_Label = i
    YAxis_Label = j
    Filepath_for_saving = k
    
    ### Define different Plotparameters
    PlotParameters = {                      # setup matplotlib to use latex for output
    "text.usetex": False,                # use LaTeX to write all text
    #"mathtext.fontset": "stixsans",
    "legend.title_fontsize" : 14,
    "legend.fontsize": 10,              # Make the legend/label fonts a little smaller
    "axes.labelsize": 12,               # LaTeX default == 10pt font.
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.figsize" : Convert_cm_To_inch(6*6, 6*4),
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
    for j in range(len(list_of_Dataframes)):
        for i in range(len(list_of_y_column_names)):
            if len(list_of_Dataframes) <= len(list_of_colors):
                plt.plot(list_of_Dataframes[j][x_column_name], list_of_Dataframes[j][list_of_y_column_names[i]], label=list_of_curve_label[j], color=list_of_colors[j], alpha=0.75, marker='.', markersize=2.0, markeredgecolor='black', markeredgewidth=0.1, linestyle='-', linewidth=1.5)
            elif len(list_of_Dataframes) >= len(list_of_colors):
                plt.plot(list_of_Dataframes[j][x_column_name], list_of_Dataframes[j][list_of_y_column_names[i]], color=list_of_colors[i], alpha=0.75, marker='.', markersize=2.0, markeredgecolor='black', markeredgewidth=0.1, linestyle='-', linewidth=1.5)


    
    ### Scientific label format changing from 1e1 to 1x10^1 (alternativ method: https://stackoverflow.com/questions/31517156/adjust-exponent-text-after-setting-scientific-limits-on-matplotlib-axis)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-4,4))
    frame.yaxis.set_major_formatter(mf)
    frame.xaxis.set_major_formatter(mf)
    
    ### X Axis Options
    frame.set_xlim(XLims) 
    frame.set_xlabel(XAxis_Label) # Label of the x axis
    
    ### Y Axis Options
    frame.set_ylim(YLims) 
    frame.set_ylabel(YAxis_Label) 
    frame.set_yscale(YScale)  
    
    ### Save Figure
    plt.savefig(Filepath_for_saving)
    
    ### Create a Legend 
    if len(list_of_Dataframes) == len(list_of_colors):
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


def Plotly_EC_Plot_Multiple_Dataframes(a, b, c, d, e, f, g, h):
    """Interactive Plotly plot, one curve per dataframe (curves with more than 330 points are thinned out to about 300), saved as html.
    a = list of dataframes, b = x column, c = y column per dataframe, d = labels, e = colours, f/g = axis labels, h = html file path."""
    #### Define Parameters
    list_of_Dataframes = a
    x_column_name = b
    list_of_y_column_names = c
    list_of_curve_label = d
    list_of_colors = e
    XAxis_Label = f
    YAxis_Label = g
    Filepath_for_saving = h

    ##### Define Figure
    fig = go.Figure()

    list_of_downsampled_dataframes = []
    for i in range(len(list_of_Dataframes)):
        ##### Downsample Dataframe Size
        max_datapoints = 300
        if len(list_of_Dataframes[i]) > max_datapoints and len(list_of_Dataframes[i]) > 330:
            print('initial amount of datapoints: %s' %(len(list_of_Dataframes[i])))
            sample_rate_float = len(list_of_Dataframes[i])/max_datapoints
            sample_rate_integer = math.ceil(sample_rate_float ) #rounded upwards
            
            downsampled_dataframe = list_of_Dataframes[i].iloc[::sample_rate_integer, :]
            
            list_of_downsampled_dataframes.append(downsampled_dataframe)
            
            print('downsampled amount of datapoints: %s' %(len(downsampled_dataframe)))
        else:
            list_of_downsampled_dataframes.append(list_of_Dataframes[i])
            
    ##### Add Scatter plots and change style
    for i in range(len(list_of_downsampled_dataframes)):
        #print(i)
        fig.add_scatter(
        x=list_of_downsampled_dataframes[i][x_column_name], 
        y=list_of_downsampled_dataframes[i][list_of_y_column_names[i]], 
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
    fig.write_html(Filepath_for_saving) # images_outdir + "Comparing_specCapacites" + ".html"

    fig.show()


def Plotly_EC_Plot_Multiple_Columns(a, b, c, d, e, f, g, h):
    """Interactive Plotly plot of several y columns of one dataframe, saved as html.
    a = dataframe, b = x column, c = list of y columns, d = labels, e = colours, f/g = axis labels, h = html file path."""
    #### Define Parameters
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
    fig.write_html(Filepath_for_saving) # images_outdir + "Comparing_specCapacites" + ".html"

    fig.show()


def Plotly_EC_Plot_List_Of_Lists(a, b, c, d, e, f, g, h, i, j):
    """Interactive 3D Plotly plot of a list of lists of dataframes (one colour per inner list), saved as html.
    a = list of lists of dataframes, b = column on the x axis, c = column on the z axis, d = column on the y axis,
    e = labels (not used), f = colours, g/h/i = x/y/z axis labels, j = html file path."""
    ##### Define Parameters
    list_of_list_with_Dataframes = a
    x_column_name = b
    y_column_name = c
    z_column_name = d
    list_of_list_with_curve_labels = e
    list_of_colors = f
    XAxis_Label = g
    YAxis_Label = h
    ZAxis_Label = i
    Filepath_for_saving = j

    fig = go.Figure()

    for i in range(0, len(list_of_list_with_Dataframes)):
        # Define x, y, and z data
        x_data = []
        for j in range(len(list_of_list_with_Dataframes[i])):
            x_data.append(list_of_list_with_Dataframes[i][j][x_column_name])

        z_data = []
        for j in range(len(list_of_list_with_Dataframes[i])):
            z_data.append(list_of_list_with_Dataframes[i][j][y_column_name])

        y_data = []
        for j in range(len(list_of_list_with_Dataframes[i])):
            y_data.append(list_of_list_with_Dataframes[i][j][z_column_name])
    
        #print(y_data[0])
    
        for j in range(len(y_data)):
            trace = go.Scatter3d(
                x=x_data[j],
                y=y_data[j],
                z=z_data[j],  # add the z array
                name= 'Index %s' %j, #list_of_list_with_curve_labels[i][j],
                mode='lines',
                line=dict(
                    color=list_of_colors[i],
                    width=3,
                    dash='solid'
                )
                )
        
            fig.add_trace(trace)

        
    # Calculate Pixel sized to Centimeter based on the Screens DPI
    # (the 3D plot keeps its own size: at OVERVIEW_W_CM x OVERVIEW_H_CM the 3D scene is too small to read)
    width_cm = 25  # width in centimetres
    height_cm = 25  # height in centimetres
    DPI_screen = 119 # dots per inch for the screen used 

    width_px = int(width_cm * DPI_screen / 2.54)  # width in pixels
    height_px = int(height_cm * DPI_screen / 2.54)  # height in pixels
    
    # Define layout (publication style as far as it exists for 3D axes)
    fig.update_layout(
        font=dict(
            family='Arial',
            size=pt(FONT_PT),   # was 14
            color='black'
        ),
        #title='Overview',
        scene=dict(
            xaxis=dict(title=XAxis_Label,
                showgrid=True,                 # grid kept in 3D: without it the depth cannot be read
                gridcolor='lightgrey',
                gridwidth=0.5,
                showline=True,
                linewidth=2,                   # was 1, publication style
                linecolor='black',
                mirror=True,
                showbackground=False,          # white like plot_bgcolor of the 2D plots
                ticks='inside', ticklen=5, tickwidth=2,
                tickfont=dict(size=pt(TICK_FONT_PT)),
                title_font=dict(size=pt(FONT_PT))  # was 14 px
                      ),
            yaxis=dict(title=YAxis_Label, range=[max(y_data[0]), min(y_data[0])],
                showgrid=True,                 # grid kept in 3D: without it the depth cannot be read
                gridcolor='lightgrey',
                gridwidth=0.5,
                showline=True,
                linewidth=2,                   # was 1, publication style
                linecolor='black',
                mirror=True,
                showbackground=False,          # white like plot_bgcolor of the 2D plots
                ticks='inside', ticklen=5, tickwidth=2,
                tickfont=dict(size=pt(TICK_FONT_PT)),
                title_font=dict(size=pt(FONT_PT))  # was 14 px
                      ),
            zaxis=dict(title=ZAxis_Label,
                showgrid=True,                 # grid kept in 3D: without it the depth cannot be read
                gridcolor='lightgrey',
                gridwidth=0.5,
                showline=True,
                linewidth=2,                   # was 1, publication style
                linecolor='black',
                mirror=True,
                showbackground=False,          # white like plot_bgcolor of the 2D plots
                ticks='inside', ticklen=5, tickwidth=2,
                tickfont=dict(size=pt(TICK_FONT_PT)),
                title_font=dict(size=pt(FONT_PT))  # was 14 px
                      ),
            camera=dict(
                eye=dict(x=-1.7, y=-1.7, z=0.5),
                center=dict(x=0, y=0, z=-0.1),
                up=dict(x=0, y=0, z=1))),
        width=width_px,  # set the width in pixels
        height=height_px,  # set the height in pixels
        margin=dict(r=10, b=10, l=10, t=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=SHOW_LEGEND,
        legend=dict(orientation='h', tracegroupgap=20, font=dict(size=pt(LEGEND_FONT_PT)))
        )

    # Save Graph
    fig.write_html(Filepath_for_saving) # images_outdir + "Comparing_specCapacites" + ".html"
    
    # Show plot
    fig.show()


def Matplotlib_Ratio_Curves_Sorted_By_Values(dataframe_for_soting_rows, list_of_columnnames_which_relativised, list_for_values_that_get_substracted, start_string_part_for_new_column_name, end_string_part_for_new_column_name, dataframe_for_ratio_calculation, name_of_new_column, column_name_for_sorting_new_dataframe, list_of_x_values, y_ax_label, x_ax_label, save, name_figure, label_legend):
    """Ratios of several columns (Calculate_Ratio_Over_Multiple_Columns), one curve per row, sorted and coloured by another column
    (e.g. coulombic efficiency, shown in the colour bar). save = 1 -> ./<name_figure>.png."""
    # Define new dataframe for getting values for plotting
    dataframe_for_plotting = pd.DataFrame()
    
    # Calculation of the Ratio
    dataframe_for_saving_new_value = dataframe_for_plotting
    
    Calculate_Ratio_Over_Multiple_Columns(list_of_columnnames_which_relativised, list_for_values_that_get_substracted, start_string_part_for_new_column_name, end_string_part_for_new_column_name, dataframe_for_ratio_calculation, dataframe_for_saving_new_value, name_of_new_column)

    # Contact the Datarame with the values for plotting and the datframe with the values for sorting
    dataframe_for_plotting = pd.concat([dataframe_for_plotting, dataframe_for_soting_rows], axis=1)
    
    # Sorting the rows according to a column values form the contacted dataframe
    dataframe_for_plotting = dataframe_for_plotting.sort_values(by=column_name_for_sorting_new_dataframe)

    # drop all columns from the contacted dataframe
    column_names_for_dropping = dataframe_for_soting_rows.columns.tolist()
    dataframe_for_plotting = dataframe_for_plotting.drop(column_names_for_dropping, axis=1)
    
    # Extract list of column names from the new dataframe
    dataframe_for_extraction = dataframe_for_plotting
    column_name_beginning = dataframe_for_plotting.columns[0]
    column_name_end = dataframe_for_plotting.columns[-1]
    string1_as_filter = ''
    string2_as_filter = ''

    list_of_column_names, list_of_column_names = Extract_Range_Of_Column_Names(dataframe_for_extraction, column_name_beginning, column_name_end, string1_as_filter, string2_as_filter)
  
    # Get list of indices of the new dataframe (For label the curves in the plot)
    list_of_indices = dataframe_for_plotting.index.values.tolist()    
    
    # Define List of list with the amount of list according to rows in the dataframe
    list_of_list_with_data = [[] for i in range(0, len(list_of_indices))]
    
    # Fill the list of lists with the values of the dataframe
    for i in range(0, len(list_of_column_names)):  
        for j in range(0, len(list_of_indices)):
            data = dataframe_for_plotting.loc[list_of_indices[j], list_of_column_names[i]] 
            list_of_list_with_data[j].append(data)
        
    ################################ Plotting #################################

    fig = plt.figure()
    #fig.set_size_inches(cm2inch(8, 4))
    plt.rcParams.update(pgf_with_latex)

    frame = fig.add_axes((.1,.3,1.0,0.6))
    
    # calculate the number of points extracted from the colormap
    number_of_points_for_cm = len(list_of_list_with_data)
    
    # define which colormap is used and extract the defined number of points
    cmap = my_colormap.resampled(number_of_points_for_cm) # defining which colormap is used and how many colorpoints are collected

    for n,i in enumerate(range(0, len(list_of_list_with_data))):
        x = list_of_x_values
        y = list_of_list_with_data[i]   
        label = list_of_indices[i]
        
        plt.plot(x, y, c=cmap(n), linestyle='-', alpha=1.0, marker='.', label=label, linewidth=1.5)

    # Defining that a colorbar is plotted according to the defined colormap
    sm = plt.cm.ScalarMappable(cmap=cmap) # defining that the colomap is used for mappable
    sm.set_array([])
    length = len(dataframe_for_soting_rows)
    list_of_ticks = [(i)/length for i in range(1, length+1)]
    list_of_ticks = [x - (0.5/length) for x in list_of_ticks]
    cbar = plt.colorbar(sm, ax=plt.gca(), ticks=list_of_ticks, label=r'$Columbic$ $efficiency$') # defining which mappable is plottet as colorbar and which ticks and label
    list_of_yticks_for_cm = dataframe_for_soting_rows[column_name_for_sorting_new_dataframe].tolist()
    cbar.ax.set_yticklabels(['{:.2f}'.format(x) for x in list_of_yticks_for_cm])

    # Scientific label format changing from 1e1 to 1x10^1 (alternativ method: https://stackoverflow.com/questions/31517156/adjust-exponent-text-after-setting-scientific-limits-on-matplotlib-axis)
    mf = mpl.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-3,2))
    frame.yaxis.set_major_formatter(mf)
    frame.xaxis.set_major_formatter(mf)

    # Defining the axis
    frame.set_ylabel(y_ax_label)				                # Label of the y axis
    #frame.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    
    frame.set_xlabel(x_ax_label)                                              # Label of the x axis
    #frame.set_xscale('log')
    #frame.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame.set_xticks(list_of_x_values)                               # which values are shown on the x axis
    
    # Saving otpions
    if save == 1:
        plt.savefig('./%s.png' %(name_figure))
    
    frame.legend(title=label_legend                                     # show the legend of the labelled plots
        ,loc='lower left' 
        ,bbox_to_anchor=(0., 1.02, 1., .102)                           # Position of the legend
        ,ncol=1
        ,mode="expand"
        ,borderaxespad=0.
        )
    
    plt.show(block=False)
