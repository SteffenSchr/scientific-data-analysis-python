"""Plot helpers and the default plot settings (colours, fonts) used by all plot functions."""

from colour import Color
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker
import textwrap

from cycler import cycler

from scientific_utils.publication_plotly import my_color_scale
from scientific_utils.publication_plotly import FONT_PT, TICK_FONT_PT, LEGEND_FONT_PT
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style

MAX_LEGEND_ENTRIES = 6    # more curves than this -> no legend (a colour bar or the title says what the curves are)
LEGEND_TITLE_WIDTH = 55   # characters per line of the legend title (fits the plot width at LEGEND_FONT_PT)


def Convert_cm_To_inch(*tupl):
    """Converts lengths from cm to inch (Matplotlib figure sizes are given in inch).
    Input: single numbers or one tuple in cm. Returns a tuple in inch."""
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)


def Set_Figure_Size_For_Plot_Area(fig, width_cm=None, height_cm=None):
    """Sets the figure size so that the default axes (plt.gca() / plt.subplots, placed with the subplot
    parameters of the figure) get a plot area of width_cm x height_cm (default: OVERVIEW_W_CM x OVERVIEW_H_CM, in cm)."""
    width_cm = OVERVIEW_W_CM if width_cm is None else width_cm
    height_cm = OVERVIEW_H_CM if height_cm is None else height_cm
    sp = fig.subplotpars
    fig.set_size_inches(Convert_cm_To_inch(width_cm/(sp.right-sp.left), height_cm/(sp.top-sp.bottom)))


def Matplotlib_New_Figure_With_Frame():
    """New figure with the publication style (pgf_with_latex) and the plot area that all overview plots use:
    fig.add_axes((.1,.3,1.0,0.6)) -> the plot area is OVERVIEW_W_CM x OVERVIEW_H_CM. Returns (fig, frame)."""
    fig = plt.figure()
    plt.rcParams.update(pgf_with_latex)
    frame = fig.add_axes((.1,.3,1.0,0.6))
    return fig, frame


def Set_Scientific_Tick_Labels(frame, power_limits):
    """Tick labels of both axes in the format 1x10^1 instead of 1e1, used outside of power_limits, e.g. (-3,3).
    Call it before set_xscale/set_yscale('log'): a log scale sets its own tick labels."""
    # alternativ method: https://stackoverflow.com/questions/31517156/adjust-exponent-text-after-setting-scientific-limits-on-matplotlib-axis
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits(power_limits)
    frame.yaxis.set_major_formatter(mf)
    frame.xaxis.set_major_formatter(mf)


def Has_Offset_Text(axis):
    """True if the axis shows an offset/exponent text (e.g. x10^3) at the end of the axis."""
    formatter = axis.get_major_formatter()
    if not isinstance(formatter, matplotlib.ticker.ScalarFormatter):
        return False
    formatter.set_locs(axis.get_majorticklocs())
    return formatter.get_offset() != ''


def Matplotlib_Legend_Above_And_Save(frame, legend_title, save, file_path, max_entries=None, **savefig_options):
    """Legend above the plot area (one column over the full width) and saving of the figure.
    The legend is drawn first, so it is also in the saved file.
    Curves with the same label get one legend entry. A legend is only drawn for 2 to max_entries entries
    (default MAX_LEGEND_ENTRIES); otherwise legend_title is shown as the title of the plot.
    save = 1 (or True) -> plt.savefig(file_path, **savefig_options), e.g. './images/<name>.png'."""
    max_entries = MAX_LEGEND_ENTRIES if max_entries is None else max_entries
    # one entry per label (e.g. several peaks marked with the same label)
    handles, labels = frame.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    # long titles are wrapped, so they are not cut at the edge of the plot area
    if legend_title:
        legend_title = textwrap.fill(legend_title, LEGEND_TITLE_WIDTH)
    # the x10^n text of the y axis sits above the plot area -> legend/title a bit higher, so they do not cover it
    offset_pad = 1.5 if Has_Offset_Text(frame.yaxis) else 0.

    if 1 < len(unique) <= max_entries:
        frame.legend(unique.values(), unique.keys()
            ,title= legend_title                                     # show the legend of the labelled plots
            ,loc='lower left'
            ,bbox_to_anchor=(0., 1.02, 1., .102)                           # Position of the legend
            ,ncol=1
            ,mode="expand"
            ,borderaxespad=offset_pad
            )
    elif legend_title:
        frame.set_title(legend_title, fontsize=LEGEND_FONT_PT, pad=6 + offset_pad*LEGEND_FONT_PT)

    # Saving options
    if save == 1:
        plt.savefig(file_path, **savefig_options)


def Create_ColorGradient_Between_Two_Colors(a, b):
    """Colour gradient between two colours (interpolated with the package colour).
    a = list of two colours (names or hex), b = number of colours.
    Returns (list of hex colours, Matplotlib ListedColormap)."""
    ### Define Parameters
    List_of_Selected_Colors = a
    Number_of_Points_in_ColorGradient = b

    ##### Creating the Color gradient out of the a list of colors
    #color_gradient_list = []

    ##### Color gradient can only be created out of two color --> Meaning multiple iteration of creation is needed to create a complete custom color gradient
    start_color = Color(List_of_Selected_Colors[0])
    end_color = Color(List_of_Selected_Colors[1])
    ##### Create a temporary colour gradient
    color_gradient_list = list(start_color.range_to(end_color, Number_of_Points_in_ColorGradient))
        
    print('The selected color gradient is: %s' %(color_gradient_list))
            
    ###### transfoms the color names into hex code and than to RGBA arrays
    color_gradient_hex_list = []
    for j in range(0, len(color_gradient_list)):
        ##### transform the colornames into hex code
        color_temp = color_gradient_list[j].hex
        color_gradient_hex_list.append(color_temp)
        ##### transforms the hex coded colors inta RGBA values
        color_as_RGBA = mpl.colors.to_rgba(color_temp, alpha=1)
        color_gradient_list[j] = color_as_RGBA
            
    ##### transfroms the list of RGBA values to a matplotlib colormap
    color_gradient_as_cmap = ListedColormap(color_gradient_list)
    
    return color_gradient_hex_list, color_gradient_as_cmap


def Plotly_Single_Dataframe(a, b, c, d, e, f, g, h):
    """Interactive Plotly line plot of one y column (publication style, size and legend from publication_plotly.py), saved as html and shown.
    a = dataframe, b = x column name, c = y column name, d = curve label, e = colour, f = x axis label, g = y axis label, h = html file path."""
    #### Define Parameters
    dataframe = a
    x_column_name = b
    y_column_names = c
    curve_label = d
    color = e
    XAxis_Label = f
    YAxis_Label = g
    Filepath_for_saving = h

    ##### Define Figure
    # 1. Wrap the Plotly-Figure with the FigureResampler
    fig = go.Figure()
            
    ##### Add Scatter plots and change style
    fig.add_scatter(
        x=dataframe[x_column_name], 
        y=dataframe[y_column_names], 
        name=curve_label, 
        mode='lines',  # set the mode to 'markers+lines'
        line=dict(
            color=color,  # set the line colour to red
            width=2,  # set the line width to 2
            dash='solid'  
        )
        )
    
    ##### Change Visual Layout of the Plot: publication style and size are set in publication_plotly.py
    ##### no legend: one curve, the axis labels say what it is (curve_label is the name shown when hovering)
    apply_style(fig, XAxis_Label, YAxis_Label, plot_w_cm=OVERVIEW_W_CM, plot_h_cm=OVERVIEW_H_CM,
                x_tickformat='uniform', y_tickformat='uniform', showlegend=False)

    # Save Plot as interactive html Plot
    fig.write_html(Filepath_for_saving) # images_outdir + "Comparing_specCapacites" + ".html"

    fig.show()


def Plotly_Single_Dataframe_Multiple_Columns(a, b, c, d, e, f, g, h):
    """Interactive Plotly line plot of several y columns of one dataframe (publication style), saved as html and shown.
    a = dataframe, b = list of x column names (one per y column, or one for all), c = list of y column names,
    d = list of curve labels, e = list of colours, f = x axis label, g = y axis label, h = html file path."""
    #### Define Parameters
    dataframe = a
    list_of_x_column_names = b
    list_of_y_column_names = c
    list_of_curve_label = d
    list_of_color = e
    XAxis_Label = f
    YAxis_Label = g
    Filepath_for_saving = h

    ##### Define Figure
    # 1. Wrap the Plotly-Figure with the FigureResampler
    fig = go.Figure()

    if len(list_of_x_column_names) == len(list_of_y_column_names):
        ##### Add Scatter plots and change style
        for i in range(len(list_of_y_column_names)):
            fig.add_scatter(
                x=dataframe[list_of_x_column_names[i]], 
                y=dataframe[list_of_y_column_names[i]], 
                name=list_of_curve_label[i], 
                mode='lines',  # set the mode to 'markers+lines'
                line=dict(
                    color=list_of_color[i],  # set the line colour to red
                    width=2,  # set the line width to 2
                    dash='solid'  
                )
                )

    else:    
        ##### Add Scatter plots and change style
        for i in range(len(list_of_y_column_names)):
            fig.add_scatter(
                x=dataframe[list_of_x_column_names[0]], 
                y=dataframe[list_of_y_column_names[i]], 
                name=list_of_curve_label[i], 
                mode='lines',  # set the mode to 'markers+lines'
                line=dict(
                    color=list_of_color[i],  # set the line colour to red
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


def Matplotlib_XvsY(dataframe, x_values_column_name, y_values_column_name, y_ax_label, x_ax_label, label_graph, save, name_figure, legend_title):
    """Points of one y column against x.
    dataframe, x/y_values_column_name = columns, y/x_ax_label = axis labels, label_graph = legend entry,
    save = 1 -> saved as ./images/<name_figure>.png, legend_title = title of the legend. Returns the plot."""
    #### Settings for the whole figure 1
    fig1, frame1 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig1.set_size_inches((2.5*3.4),(3.4))
    
    #### Important plot parameters based on the length of the dataframes
    # x values
    X = dataframe[x_values_column_name]

    # y values
    Y = dataframe[y_values_column_name]
       
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
    plot = plt.plot(X, Y, list_of_Hexcolors[0], linestyle='None', alpha=0.5, marker='.', label=label_graph, linewidth=1.5)
        
    #frame1.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
    
    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame1, (-3,3))

    frame1.set_ylabel(y_ax_label, labelpad=15)				                # Label of the y axis
    #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
    frame1.set_xlabel(x_ax_label)                                              # Label of the x axis
    #ax.set_xscale('log')
    #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame1.set_xticks([])                               # which values are shown on the x axis

    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame1, legend_title, save, './images/%s.png' %(name_figure))
        
    return plot


def Matplotlib_XvsY_Per_Cycle(dataframe, x_values_column_name, y_values_column_name, y_ax_label, x_ax_label, cycle_to_save, additional_name, legend_title):
    """Like Matplotlib_XvsY; the legend entry shows the number of points and the x range.
    cycle_to_save = 1 -> saved as ./images/<additional_name>.png. Returns the plot."""
    #### Settings for the whole figure 1
    fig1, frame1 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig1.set_size_inches((2.5*3.4),(3.4))
    
    #### Important plot parameters based on the length of the dataframes
    # x values
    X = dataframe[x_values_column_name]

    # y values
    Y = dataframe[y_values_column_name]
       
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
    plot = plt.plot(X, Y, list_of_Hexcolors[0], linestyle='None', alpha=0.5, marker='.', label=r'equidistant data', linewidth=1.5)
        
    #frame1.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))

    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame1, (-2,2))

    frame1.set_ylabel(y_ax_label)				                # Label of the y axis
    #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
    frame1.set_xlabel(x_ax_label)                                              # Label of the x axis
    #ax.set_xscale('log')
    #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame1.set_xticks([])                               # which values are shown on the x axis
    
    #Settings for saving
    index_to_save = cycle_to_save

    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame1, legend_title, index_to_save, './images/%s.png' %(additional_name))
        
    return plot


def Matplotlib_XvsY1Y2(dataframe, x_values_column_name, y_values_column_name_first, y_values_column_name_second, label_y_first, label_y_second, y_ax_label, x_ax_label, save, name_figure, legend_title):
    """Points of two y columns of one dataframe against the same x column.
    label_y_first/second = legend entries, save = 1 -> saved as ./images/<name_figure>.png. Returns the plot."""
    #### Settings for the whole figure 1
    fig1, frame1 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig1.set_size_inches((2.5*3.4),(3.4))
    
    #### Important plot parameters based on the length of the dataframes
    # x values
    X = dataframe[x_values_column_name]

    # y values
    Y1 = dataframe[y_values_column_name_first]
    Y2 = dataframe[y_values_column_name_second]
       
    # For the length of the x axis
    X_range = max(X) - min(X)
    Xmin = min(X) 
    Xmax = max(X) 
    Xmin_extended = Xmin - X_range*0.02
    Xmax_extended = Xmax + X_range*0.02
    
    # For the length of the y axis
    Y_range = max(Y1) - min(Y1)
    Ymin = min(Y1)
    Ymax = max(Y1)
    Ymin_extended = Ymin - Y_range*0.1
    Ymax_extended = Ymax + Y_range*0.1
    
    # For the legend
    number_of_datapoints = len(X)
    
    ### Settings for the first axis (here the dQ/dV plot)
    plt.plot(X, Y1, list_of_Hexcolors[0], linestyle='None', alpha=0.5, marker='.', label=label_y_first, linewidth=1.5)
    plt.plot(X, Y2, list_of_Hexcolors[-1], linestyle='None', alpha=0.5, marker='.', label=label_y_second, linewidth=1.5)
    
    #frame1.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
    
    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame1, (-3,3))

    frame1.set_ylabel(y_ax_label, labelpad=15)				                # Label of the y axis
    #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
    frame1.set_xlabel(x_ax_label)                                              # Label of the x axis
    #ax.set_xscale('log')
    #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame1.set_xticks([])                               # which values are shown on the x axis
    
    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame1, legend_title, save, './images/%s.png' %(name_figure))
       
    plot = plt.show(block=False)   
    
    return plot


def Matplotlib_X1Y1_X2Y2(dataframe1, dataframe2, x1_values_column_name, x2_values_column_name, y1_values_column_name, y2_values_column_name, label_y_first, label_y_second, y_ax_label, x_ax_label, save, name_figure, legend_title):
    """Points of two dataframes in one plot (x1 vs y1 and x2 vs y2).
    label_y_first/second = legend entries, save = 1 -> saved as ./images/<name_figure>.png. Returns the plot."""
    #### Settings for the whole figure 1
    fig1, frame1 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
    #fig1.set_size_inches((2.5*3.4),(3.4))
    
    #### Important plot parameters based on the length of the dataframes
    # x values
    x1 = dataframe1[x1_values_column_name]
    x2 = dataframe2[x2_values_column_name]
    
    # y values
    y1 = dataframe1[y1_values_column_name]
    y2 = dataframe2[y2_values_column_name]
       
    # For the length of the x axis
    X_range = max(x1) - min(x1)
    Xmin = min(x1) 
    Xmax = max(x1) 
    Xmin_extended = Xmin - X_range*0.02
    Xmax_extended = Xmax + X_range*0.02
    
    # For the length of the y axis
    Y_range = max(y1) - min(y2)
    Ymin = min(y2)
    Ymax = max(y1)
    Ymin_extended = Ymin - Y_range*0.1
    Ymax_extended = Ymax + Y_range*0.1
    
    ### Settings for the first axis (here the dQ/dV plot)
    plt.plot(x1, y1, list_of_Hexcolors[0], linestyle='None', alpha=0.5, marker='.', label=label_y_first, linewidth=1.5)
    plt.plot(x2, y2, list_of_Hexcolors[-1], linestyle='None', alpha=0.5, marker='.', label=label_y_second, linewidth=1.5)
    
    #frame1.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
    
    # Scientific label format changing from 1e1 to 1x10^1
    Set_Scientific_Tick_Labels(frame1, (-3,3))

    frame1.set_ylabel(y_ax_label)                # Label of the y axis
    #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
    frame1.set_xlabel(x_ax_label)                                              # Label of the x axis
    #ax.set_xscale('log')
    #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame1.set_xticks([])                               # which values are shown on the x axis
    
    # Legend above the plot and saving (legend first, so it is in the saved file)
    Matplotlib_Legend_Above_And_Save(frame1, legend_title, save, './images/%s.png' %(name_figure))
       
    plot = plt.show(block=False)   
    
    return plot


#######################################################################
########## Default plot settings used by all plot functions ##########
#######################################################################

########## Define colours by hex code ##########
yellow = '#ffa200'
orange = '#f97625'
lightpink = '#e94a3a'
pink = '#ce1b49'
lightpurple = '#a90054'
purple = '#7e0059'
darkpurple = '#4c0057'
darkblue = '#0a004d'

########## Colours in a list to access them in a for loop ##########
colors = [yellow, orange, lightpink, pink, lightpurple, purple, darkpurple, darkblue]

########## Colour gradient with the colour package
#beginnig_color = Color("yellow")
#end_color = Color("blue")
#number_of_colorpoints = 4
#color_gradient = list(beginnig_color.range_to(end_color,number_of_colorpoints))
#print(color_gradient)

########## Cologradient with Matplotlib Colormaps
# Available colormaps: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html#ibm
########## Colormap of the publication style (my_color_scale), reversed -> blue to red like coolwarm before
my_colormap = LinearSegmentedColormap.from_list('my_color_scale', my_color_scale[::-1])
number_of_colorpoints = 50 # number of colour points taken from the colour gradient with equal distance
colormap = my_colormap.resampled(number_of_colorpoints) # was: plt.get_cmap('coolwarm', number_of_colorpoints)
array_of_RGBAcolors = colormap(range(number_of_colorpoints)) # Returns the colormap as RGBA values scaled from 0 to 1
list_of_Hexcolors = [ rgb2hex(array_of_RGBAcolors[i,:]) for i in range(array_of_RGBAcolors.shape[0]) ] # Converts the scaled RGBA values to hex code and puts them in a list

########## Colour cycle for curves without a fixed colour: the 4 strong colours of my_color_scale in contrasting order
########## (blue, red, gold, teal), then the same 4 colours darker -> 8 different colours before a colour repeats
list_of_cycle_colors = [my_color_scale[4], my_color_scale[0], my_color_scale[1], my_color_scale[3]]
list_of_cycle_colors = list_of_cycle_colors + [rgb2hex([0.7*v for v in mpl.colors.to_rgb(c)]) for c in list_of_cycle_colors]

########## Font settings for the PGF file ##########
pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "xelatex",         # change this if using xetex or lautex
    "text.usetex": False,                # use LaTeX to write all text
    #"pgf.rcfonts": False,               # don't setup fonts from rc parameters
    "font.family": "sans-serif",           # standard sans-serif font of Matplotlib
    "font.sans-serif": ['Arial', 'DejaVu Sans'],   # publication style: Arial as in publication_plotly
    #"mathtext.fontset": "stixsans",
    "font.size": FONT_PT,
    "legend.title_fontsize" : LEGEND_FONT_PT,      # was 14
    "legend.fontsize": LEGEND_FONT_PT,             # was 10
    "axes.labelsize": FONT_PT,                     # was 12
    "xtick.labelsize": TICK_FONT_PT,               # was 10
    "ytick.labelsize": TICK_FONT_PT,               # was 10
    ##### publication style: ticks inside on all four sides with minor ticks, thick axis lines (2 px = 1.5 pt)
    "axes.linewidth": 1.5,
    "xtick.direction": 'in', "ytick.direction": 'in',
    "xtick.top": True, "ytick.right": True,
    "xtick.minor.visible": True, "ytick.minor.visible": True,
    "xtick.major.size": 3.75, "ytick.major.size": 3.75, "xtick.major.width": 1.5, "ytick.major.width": 1.5,
    "xtick.minor.size": 2.25, "ytick.minor.size": 2.25, "xtick.minor.width": 0.75, "ytick.minor.width": 0.75,
    "axes.prop_cycle": cycler(color=list_of_cycle_colors),   # was cycler(color=my_color_scale[::-1]) (5 colours, pale middle colour)
    "svg.fonttype": 'none',                        # text stays editable in Inkscape
    # the plot functions draw into fig.add_axes((.1,.3,1.0,0.6)) -> the axes are exactly OVERVIEW_W_CM x OVERVIEW_H_CM
    "figure.figsize" : Convert_cm_To_inch(OVERVIEW_W_CM, OVERVIEW_H_CM/0.6),   # was Convert_cm_To_inch(16, 8)
    # default axes (plt.gca(), plt.subplots) at the same position -> also exactly OVERVIEW_W_CM x OVERVIEW_H_CM
    "figure.subplot.left": 0.1, "figure.subplot.right": 1.1, "figure.subplot.bottom": 0.3, "figure.subplot.top": 0.9,
    'savefig.dpi'         : 300,   ## figure dots per inch or 'figure'
    'savefig.facecolor'   : 'white',    ## figure facecolor when saving
    'savefig.edgecolor'   : 'white',    ## figure edgecolor when saving
    'savefig.format'      : 'png',      ## png, ps, pdf, svg
    'savefig.bbox'        : 'tight', 
    "pgf.preamble": "\n".join([
        r"\usepackage[T1]{fontenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage{fontspec}",        # plots will be generated using this preamble
        r"\usepackage{fourier}",
        r"\usepackage{unicode-math}",
        r"\usepackage[basic,italic,symbolgreek,numbers]{mathastext}"
        ])
    }

########## The style is active as soon as this module is imported (also for plots written directly in a notebook)
plt.rcParams.update(pgf_with_latex)
