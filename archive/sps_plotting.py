"""Plots of the SPS process data."""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker

from scientific_utils.general.plotting import Convert_cm_To_inch


def Matplotlib_SPS_Plot(a, b, c, d, e, f, g, h, i, j):
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
