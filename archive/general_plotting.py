"""Unused functions moved here from `scientific_utils/general/plotting.py` (nothing in the repository called them)."""

from colour import Color
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker

from cycler import cycler

from scientific_utils.publication_plotly import my_color_scale
from scientific_utils.publication_plotly import FONT_PT, TICK_FONT_PT, LEGEND_FONT_PT
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style


def Create_ColorMap(a):
    """Colour gradient through all colours of a list (one step between neighbouring colours).
    a = list of colours (names or hex). Returns (list of RGBA colours, Matplotlib ListedColormap)."""
    ### Define Parameters
    List_of_Selected_Colors = a

    ##### Creating the Color gradient out of the a list of colors
    color_gradient_list = []
    for y in range(0, (len(List_of_Selected_Colors)-1)):
        ##### Color gradient can only be created out of two color --> Meaning multiple iteration of creation is needed to create a complete custom color gradient
        start_color = Color(List_of_Selected_Colors[y])
        end_color = Color(List_of_Selected_Colors[y+1])
        ##### Create a temporary colour gradient
        color_gradient_temp = list(start_color.range_to(end_color,2))
        if y == 0:
            color_gradient_list = color_gradient_list + color_gradient_temp
        else:
            color_gradient_list = color_gradient_list + color_gradient_temp[1:]
        
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
    
    return color_gradient_list, color_gradient_as_cmap


def Matplotlib_Simple_Plot(a, b, c, d, e, f, g, h, i):
    """Simple x-y line plot, saved and shown.
    a = x data, b = y data, c = colour, d = x limits, e = y limits, f = y scale ('linear' or 'log'),
    g = x axis label, h = y axis label, i = file path for saving."""
    ### Functions needed from other Package
    
    ### Define Parameters
    x_data = a
    y_data = b
    color = c
    XLims = d
    YLims = e
    YScale = f
    XAxis_Label = g
    YAxis_Label = h
    Filepath_for_saving = i
    
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
    plt.plot(x_data, y_data, color=color, alpha=0.75, marker='.', markersize=2.0, markeredgecolor='black', markeredgewidth=0.1, linestyle='-', linewidth=1.5)
    
    ### Scientific label format changing from 1e1 to 1x10^1 (alternativ method: https://stackoverflow.com/questions/31517156/adjust-exponent-text-after-setting-scientific-limits-on-matplotlib-axis)
    mf = mpl.ticker.ScalarFormatter(useMathText=True)
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
    
    ### Show Figure
    plt.show()
    
    return


def Plotly_Multiple_Dataframes(a, b, c, d, e, f, g, h):
    """Interactive Plotly line plot with one curve per dataframe (publication style), saved as html and shown.
    a = list of dataframes, b = list of x column names, c = list of y column names (one per dataframe),
    d = list of curve labels, e = list of colours, f = x axis label, g = y axis label, h = html file path."""
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

    #fig.update_xaxes(autorange='reversed')
    
    ##### Change Visual Layout of the Plot: publication style, size and legend are set in publication_plotly.py
    apply_style(fig, XAxis_Label, YAxis_Label, plot_w_cm=OVERVIEW_W_CM, plot_h_cm=OVERVIEW_H_CM,
                x_tickformat='uniform', y_tickformat='uniform', showlegend=SHOW_LEGEND)

    # Save Plot as interactive html Plot
    fig.write_html(Filepath_for_saving) # images_outdir + "Comparing_specCapacites" + ".html"

    fig.show()
