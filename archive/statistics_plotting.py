"""Unused functions moved here from `scientific_utils/statistics/plotting.py` (nothing in the repository called them)."""

from scipy.cluster.hierarchy import dendrogram
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot
from scipy import stats
import matplotlib.ticker

from scientific_utils.general.plotting import list_of_Hexcolors
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.general.plotting import pgf_with_latex


def Matplotlib_QQ_Plot_Sampled(data, sample_size):
    """Q-Q plot of the first sample_size values of data (standardised) against random normal values.
    data = array, sample_size = number of points."""
    i=0
    # Calculation of the Quanitels for the QQ-Plot
    qq = np.ones([sample_size, 2]) # retunr a array of given shape with ones for saving the calculated quantiels
    data = np.array(data) # numpy array (copy) instead of pandas Series for np.random.shuffle
    np.random.shuffle(data)
    qq[:, 0] = (np.sort(data[0:sample_size])- np.mean(data))/stats.tstd(data) # standarized distribution of the data
    model_dist = np.random.normal(size = sample_size) 
    qq[:, 1] = (np.sort(model_dist) - np.mean(model_dist))/stats.tstd(model_dist) # standardized distribution of the model distribution
    
    # Calcualting the values for the 45 degree line
    max_sample_quantile = max(qq[:, 0])
    min_sample_quantile = min(qq[:, 0])
    
    number_of_datapoints = len(qq[:, 0])
    
    # Plotting of the calculated quantiels
    fig1 = plt.figure()
    plt.rcParams.update(pgf_with_latex) # important when worked with latex and pgfplot
    frame1 = fig1.add_axes((.1,.3,1.0,0.6))
    plt.plot(qq[:,1], qq[:, 0], alpha=0.5, marker='.', linestyle='None', label=r'Data; Datapoints: %s' %(number_of_datapoints) , color=list_of_Hexcolors[i])
    plt.plot([min_sample_quantile, max_sample_quantile], [min_sample_quantile, max_sample_quantile], color = 'black', label='Theoretical Line when the sample distribution matches the theoretical distribution')

    # Scientific label format changing from 1e1 to 1x10^1 (alternativ method: https://stackoverflow.com/questions/31517156/adjust-exponent-text-after-setting-scientific-limits-on-matplotlib-axis)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    frame1.yaxis.set_major_formatter(mf)
    frame1.xaxis.set_major_formatter(mf)
    
    frame1.set_ylabel(r'$ Sample$ $Quantile $')                # Label of the y axis
    #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
    #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
    frame1.set_xlabel(r'$ Theoretical$ $Quantile $')                                              # Label of the x axis
    #ax.set_xscale('log')
    #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
    #frame1.set_xticks([])                               # which values are shown on the x axis

    #if i == 9:
    #    plt.savefig('./images/dQdV_fromEquidistantData_10thChargeCycle.png', dpi=1000, facecolor='w', edgecolor='w', format='png',bbox_inches='tight')
    
    frame1.legend(title='Q-Q Plot'                                     # show the legend of the labelled plots
    ,loc='lower left' 
    ,bbox_to_anchor=(0., 1.02, 1., .102)                           # Position of the legend
    ,ncol=1
    ,mode="expand"
    ,borderaxespad=0.
    ) 
        
    plot = plt.show(block=False)
    
    return plot


def Statsmodels_QQ_Plot(list_of_dataframes, y_values_column_name_first, y_values_column_name_second):
    """Q-Q plot of the residuals column 1 - column 2 with statsmodels (qqplot, 45 degree line), one figure per dataframe."""
    ################################################ Figure 5 ##################################
    ########## qq-plot
    ##### -> for checking the normality of the data generating process. The error of a measurement should always be normally distributed.
    ##### ->  if the residual tend to be larger in magnitude than what we would expect from the normal distribution, then our p-values and confidence intervals may be too optimisitic. i.e., we may fail to adequately account for the full variability of the data.
    
    for i in range(0, len(list_of_dataframes)):
        Y1 = list_of_dataframes[i][y_values_column_name_first]
        Y2 = list_of_dataframes[i][y_values_column_name_second]
        residuals = Y1 - Y2
        Y = residuals
        
        qqplot(residuals,line='45',fit='True')
        
        #if i == 9:
        #    plt.savefig('./images/dQdV_fromEquidistantData_qqplot_10thChargeCycle.png', dpi=1000, facecolor='w', edgecolor='w', format='png',bbox_inches='tight')
    
        ### Settings for showing the plot
        plot = plt.show(block=False)                                                       # Shows the plot, but the following code keeps running
    
    return plot
