"""Unused functions moved here from `scientific_utils/tof_sims/plotting.py` (nothing in the repository called them)."""

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
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style
from scientific_utils.publication_plotly import cm, pt, MARGIN, FONT_PT, TICK_FONT_PT, ANNOT_FONT_PT, LEGEND_FONT_PT


def Matplotlib_Normalized_DepthProfil(a, b, c, d, e, f, g, h, i, j, k):
    """Like Matplotlib_DepthProfil, but every ion column is divided by the maximum of its reference column.
    a = dataframe, b = x column, c = list of y columns, d = list of reference columns (one per y column), e = colours, f/g = limits, h = y scale, i/j = labels, k = file path."""
    ### Functions needed from other Package
    
    ### Define Parameters
    Dataframe = a
    x_column_name = b
    list_of_y_column_names = c
    list_of_y_column_names_for_norm = d
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
        x = Dataframe[x_column_name]
        y = Dataframe[list_of_y_column_names[i]]/Dataframe[list_of_y_column_names_for_norm[i]].max()
        
        plt.plot(x, y, label=list_of_y_column_names[i], color=list_of_colors[i], alpha=0.75, marker='.', markersize=2.0, markeredgecolor='black', markeredgewidth=0.1, linestyle='-', linewidth=1.5)
    
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


def Plotly_BoxPlot(a, b, c , d, e, f, g):
    """Interactive box plot (all points, mean shown) of one column for several samples, saved as html.
    a = list of dataframes, b = column name, c = sample names, d = colours, e/f = x/y axis label, g = html file path."""
    ### This Function Reads the Area Lists given by SurfaceLab and transforms them into a Dataframe
    
    #### Define Parameters
    list_of_dataframes = a
    y_column_name = b
    list_of_curve_label  = c
    list_of_colors = d
    XAxis_Label = e
    YAxis_Label = f
    Filepath_for_saving = g

    ##### Define Figure
    # 1. Wrap the Plotly-Figure with the FigureResampler
    fig = go.Figure()
    
    for j in range(len(list_of_dataframes)):
        
        dataframe = list_of_dataframes[j]
        
        #Plotting Components
        fig.add_trace(go.Box( 
            y=dataframe[y_column_name],
            name=list_of_curve_label[j],
            boxpoints='all', # can also be outliers, or suspectedoutliers, or False
            jitter=0.3, # add some jitter for a better separation between points
            pointpos=-1.8, # relative position of points wrt box
            boxmean=True, # True --> only shows mean line # represent mean and standard deviation
            whiskerwidth = 0.75,
            fillcolor = list_of_colors[j], # was 'royalblue'
            width = 0.25,
            opacity = 0.6,
            line = dict(
                color = 'black',
                width = 1.0),
            marker = dict(
                color = list_of_colors[j], # was 'royalblue'
                opacity = 0.6,
                size = 5,
                line = dict(
                    width = 0.75,
                    color = 'black'))
        ))
    
    ##### Change Visual Layout of the Plot: publication style, size and legend are set in publication_plotly.py
    apply_style(fig, XAxis_Label, YAxis_Label, plot_w_cm=OVERVIEW_W_CM, plot_h_cm=OVERVIEW_H_CM,
                x_tickformat='uniform', y_tickformat='uniform', showlegend=False, x_minor=False) # legend would only repeat the x axis labels

    # Save Plot as interactive html Plot
    fig.write_html(Filepath_for_saving) # images_outdir + "Comparing_specCapacites" + ".html"

    fig.show()


def Plotly_MassSpectrum(a, b, c , d, e, f, g, h):
    """Interactive mass spectra (plotly-resampler for many points), one curve per dataframe, saved as html and shown in a Dash app.
    a = list of dataframes, b/c = x/y column per dataframe, d = curve labels, e = colours, f/g = axis labels, h = html file path."""
    ### This Function Reads the Area Lists given by SurfaceLab and transforms them into a Dataframe
    
    ### Define Variables ###
    list_of_dataframes = a
    list_of_x_column_names = b
    list_of_y_column_names = c
    list_of_curve_label = d
    list_of_colors = e
    XAxis_Label = f
    YAxis_Label = g
    Filepath_for_saving = h

    ##### Define Figure with Plotly resampler
    ###
    fig = FigureResampler(go.Figure())
    ###   

    for i in range(len(list_of_dataframes)):
        ##### Add Scatter plots and change style
        fig.add_scatter(
        x=list_of_dataframes[i][list_of_x_column_names[i]], 
        y=list_of_dataframes[i][list_of_y_column_names[i]],
        name=list_of_curve_label[i], 
        mode='markers+lines',  # set the mode to 'markers+lines'
        marker=dict(
            color=list_of_colors[i],  # set the marker colour
            size=2.5,  # set the marker size to 8
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

    # Show figure in dash for automatic resample mode
    fig.show_dash(mode='inline')
