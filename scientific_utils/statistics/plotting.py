"""Diagnostic plots: residuals, histograms, Q-Q plots, FFT spectra, dendrograms."""

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
from scientific_utils.general.plotting import Matplotlib_Legend_Above_And_Save, Matplotlib_New_Figure_With_Frame, Set_Scientific_Tick_Labels


def Matplotlib_Residuals_Vs_Value(list_of_dataframes, x_values_column_name, y_values_column_name_first, y_values_column_name_second, cycle_to_save, additional_name, legend_title, list_of_labels=None, cycles_to_show=None):
    """Residuals (column 1 - column 2, e.g. data - smoothed) against x, one figure per curve.
    The curve number cycle_to_save is saved as ./images/ResidualsVSValue_<Cycle|Rate><n>_<additional_name>.png; list_of_labels = None -> cycles, else rates. cycles_to_show = list of curve numbers that are plotted (None -> all)."""
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
        ################################################ Figure 2 ##################################
        ########## Residuals vs predicted value ##########
        ##### -> to check homoscedasticity
        ##### -> variance of the residuals increases with response variable magnitude. Therefore, the problem does not respect homoscedasticity and some kind of variable transformation may be needed to improve model quality.
        ##### -> When this assumption isn’t valid (constant variance), we shouldn’t believe our confidence intervals, prediction bands, or the p-values in our regression.
        #### Settings for the whole figure
        fig2, frame3 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
        #fig2.set_size_inches((2.5*3.4),(3.4))

        #### Important plot parameters based on the length of the dataframes
        # x values
        X = list_of_dataframes[i][x_values_column_name]

        # y values
        Y1 = list_of_dataframes[i][y_values_column_name_first]
        Y2 = list_of_dataframes[i][y_values_column_name_second]
        residuals = Y1 - Y2
        Y = residuals
       
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

        #### Settings for the first axis
        plt.plot(X, Y, list_of_Hexcolors[i], linestyle='None', alpha=0.5, marker='.', label=r'residuals', linewidth=1.5)
        plt.hlines(y=0,xmin=Xmin_extended,xmax=Xmax_extended,color='red',linestyle='--',lw=1, alpha=0.5)
    
        frame3.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))

        frame3.set_ylabel(r' $residuals$ ')				                # Label of the y axis
        frame3.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
        #frame3.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
    
        frame3.set_xlabel(r'$ \frac{dQ}{dV}$ / $\frac{\mathsf{mAh}}{\mathsf{V}}$')                                              # Label of the x axis
        #ax.set_xscale('log')
        frame3.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        #frame3.set_xticks([])                               # which values are shown on the x axis
    
        # Saving One Figure from one Rate
        index_to_save = cycle_to_save - 1
        
        # Legend above the plot and saving (legend first, so it is in the saved file)
        Matplotlib_Legend_Above_And_Save(frame3, legend_title + ' (%s: %s)' %(label_name, label_value), i == index_to_save, './images/ResidualsVSValue_%s%s_%s.png' %(label_name, label_value, additional_name))
    
        plot = plt.show(block=False)
        
    return plot


def Matplotlib_FFT_Spectra_Comparison(list_of_dataframes, x_values_column_name, y_values_column_name_first, y_values_column_name_second, cycle_to_save, additional_name, legend_title, y_ax_label, x_ax_label, list_of_labels=None, cycles_to_show=None):
    """Power spectra (FFT) of two columns (e.g. data and smoothed data), one figure per curve.
    The curve number cycle_to_save is saved as ./images/FFTSpectraComparison_<Cycle|Rate><n>_<additional_name>.png. cycles_to_show = list of curve numbers that are plotted (None -> all)."""
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
        ################################################ Figure 3 ##################################
        ########## Choosing Optimal Savitzky-Golay Parameter with the help of Fourier Transformation ##########
        # according to: https://nirpyresearch.com/choosing-optimal-parameters-savitzky-golay-smoothing-filter/
    
        # x values (only for calculation)
        X_for_calculation = list_of_dataframes[i][x_values_column_name]
    
        # y values (only for calculation)
        Y_for_calculation = list_of_dataframes[i][y_values_column_name_first]
        Y2_for_calculation = list_of_dataframes[i][y_values_column_name_second]
    
    
        # Calculating Power spectrum of Y (This Y is plottet)
        Y = np.abs(np.fft.fftshift(np.fft.fft(Y_for_calculation)))**2 # shifted the array by half its length with the np.fft.fftshift function. FT results in imaginary and real values for this reason we calculate the absolute value
        Y2 = np.abs(np.fft.fftshift(np.fft.fft(Y2_for_calculation)))**2
    
        # Calculating the X axes in the Fourier space
        X = np.arange(Y.shape[0]) - Y.shape[0]//2 # hat the Fourier transform of a (real-valued) signal of size N (N pixels) has only N/2 independent values. You can see in the second plot that the power spectrum is symmetric with respect to the central point.
        # In this way the power spectrum values close to the central point (fpix close to zero) correspond to the ‘low frequencies’ of our signal, i.e. the amount of signal associated with slowly varying parts of the spectrum. 
        #Conversely, the ‘high frequency’ part of the power spectrum is associated with the fast moving regions of the original signal (should be the noise in the original signal). 
    
        # To check the Savitzky Golay filter, choose a part of the curve where little happens, because then mainly noise is seen
        # Procedure
        # 1. Calculate 2-3 different smoothed spectra, with different parameters of the SG function.
        # 2. Calculate the power spectrum of a relatively featureless region of the spectrum, in both the original and the smoothed versions.
        # 3. Compare the power spectra in a lin-log plot.
        # -> the low frequency part should match completely between the original data and the filter. The 'high' frequency part should be smoothed by the Savitzky Golay filter. Where the change from low to high frequency is depends on the analysed curve. The smaller the change of the original curve, the smaller the low frequency range in the FFT plot!
    
    
        #### Settings for the whole figure
        fig3, frame4 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
        #fig3.set_size_inches((2.5*3.4),(3.4))
    
    
        #### Important plot parameters based on the length of the dataframes

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

        #### Settings for the first axis
        plt.plot(X, Y, list_of_Hexcolors[i], linestyle='None', alpha=0.5, marker='.', label=r'data', linewidth=1.5)
        plt.plot(X, Y2, 'g', linestyle='None', alpha=0.5, marker='.', label=r'Savitzky-Golay smoothed', linewidth=1.5)

        # activating of the scientific notation
        #frame4.ticklabel_format(axis='both', style='sci', scilimits=(-2,2))
        
        # Scientific label format changing from 1e1 to 1x10^1
        Set_Scientific_Tick_Labels(frame4, (-2,2))

        frame4.set_ylabel(y_ax_label)				                # Label of the y axis
        #frame3.set_ylim(ymin, ymax)                                                             # minimum and maximum value shown on the y axis
        #frame3.set_yticks(np.arange(0, 1.5, 0.25))                                        # which values are shown on the y axis
        frame4.set_yscale('log')
    
        frame4.set_xlabel(x_ax_label)                                              # Label of the x axis
        #ax.set_xscale('log')
        frame4.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        #frame3.set_xticks([])                               # which values are shown on the x axis
    
        # Saving One Figure from one Rate
        index_to_save = cycle_to_save - 1
        
        # Legend above the plot and saving (legend first, so it is in the saved file)
        Matplotlib_Legend_Above_And_Save(frame4, legend_title + ' (%s: %s)' %(label_name, label_value), i == index_to_save, './images/FFTSpectraComparison_%s%s_%s.png' %(label_name, label_value, additional_name))
        
        plot = plt.show(block=False)
    
    return plot


def Matplotlib_Histogram_Residuals(list_of_dataframes, y_values_column_name_first, y_values_column_name_second, cycle_to_save, additional_name, legend_title, list_of_labels=None, cycles_to_show=None):
    """Histogram (20 bins) of the residuals column 1 - column 2, one figure per curve (check if the errors are normally distributed).
    The curve number cycle_to_save is saved as ./images/Histogram_residuals_<Cycle|Rate><n>_<additional_name>.png. cycles_to_show = list of curve numbers that are plotted (None -> all)."""
    ################################################ Figure 4 ##################################
    ########## Histogram of normalized residuals
    ##### -> for checking the normality of the data generating process. The error of a measurement should always be normally distributed.
    ##### ->  if the residual tend to be larger in magnitude than what we would expect from the normal distribution, then our p-values and confidence intervals may be too optimisitic. i.e., we may fail to adequately account for the full variability of the data.
    
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
        #### Settings for the whole figure
        Y1 = list_of_dataframes[i][y_values_column_name_first]
        Y2 = list_of_dataframes[i][y_values_column_name_second]
        residuals = Y1 - Y2
        Y = residuals
        
        fig4, frame5 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
        #fig4.set_size_inches((2.5*3.4),(3.4))
        
    
        plt.hist(residuals,bins=20,edgecolor='k', color=list_of_Hexcolors[i], label='residuals')
        
        frame5.set_ylabel(r'$Count$')
        
        frame5.set_xlabel(r'$Normalized$ $residuals$')
    
        # Saving One Figure from one Rate
        index_to_save = cycle_to_save - 1
        
        # Legend above the plot and saving (legend first, so it is in the saved file)
        Matplotlib_Legend_Above_And_Save(frame5, legend_title + ' (%s: %s)' %(label_name, label_value), i == index_to_save, './images/Histogram_residuals_%s%s_%s.png' %(label_name, label_value, additional_name))
        plot = plt.show(block=False)

    return plot


def Matplotlib_QQ_Plot(list_of_dataframes, y_values_column_name_first, y_values_column_name_second, cycle_to_save, additional_name, list_of_labels=None, cycles_to_show=None):
    """Q-Q plot of the residuals column 1 - column 2 against a normal distribution, one figure per curve.
    The curve number cycle_to_save is saved as ./images/qq_plot_<Cycle|Rate><n>_<additional_name>.png. cycles_to_show = list of curve numbers that are plotted (None -> all)."""
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
        # Defining the variables
        Y1 = list_of_dataframes[i][y_values_column_name_first]
        Y2 = list_of_dataframes[i][y_values_column_name_second]
        residuals = list_of_dataframes[i][y_values_column_name_first] - list_of_dataframes[i][y_values_column_name_second]
        
        number_of_datapoints = len(residuals)
        
        # Calculation of the Quanitels for the QQ-Plot
        qq = np.ones([number_of_datapoints, 2]) # retunr a array of given shape with ones for saving the calculated quantiels
        residuals = residuals.to_numpy().copy() # writable numpy array instead of pandas Series for np.random.shuffle
        np.random.shuffle(residuals)
        qq[:, 0] = (np.sort(residuals[0:number_of_datapoints])- np.mean(residuals))/stats.tstd(residuals) # standarized distribution of the data
        model_dist = np.random.normal(size = number_of_datapoints) 
        qq[:, 1] = (np.sort(model_dist) - np.mean(model_dist))/stats.tstd(model_dist) # standardized distribution of the model distribution
    
        # Calcualting the values for the 45 degree line
        max_sample_quantile = max(qq[:, 0])
        min_sample_quantile = min(qq[:, 0])
        max_theoretical_quantile = max(qq[:, 1])
        min_theoretical_quantile = min(qq[:, 1])
        
        # Deciding which value is bigger or smaller and than use the bigger and smaller value for printing the line in QQ plot
        if max_sample_quantile > max_theoretical_quantile :
            max_value_line = max_sample_quantile
        else:
            max_value_line = max_theoretical_quantile
            
        if min_sample_quantile < min_theoretical_quantile :
            min_value_line = min_sample_quantile
        else:
            min_value_line = min_theoretical_quantile
        
        
        # Plotting of the calculated quantiels
        fig1, frame1 = Matplotlib_New_Figure_With_Frame() # figure, publication style and plot area
        plt.plot(qq[:,1], qq[:, 0], alpha=0.5, marker='.', linestyle='None', label=r'residuals' , color=list_of_Hexcolors[i])
        plt.plot([min_value_line, max_value_line], [min_value_line, max_value_line], color = 'black', label='normal distribution')

        # Scientific label format changing from 1e1 to 1x10^1
        Set_Scientific_Tick_Labels(frame1, (-2,2))
    
        frame1.set_ylabel(r'$ Sample$ $Quantile $')                # Label of the y axis
        #frame1.set_ylim(Ymin_extended, Ymax_extended)                                                             # minimum and maximum value shown on the y axis
        #frame1.set_yticks(np.arange(0, 1.5, 0.25Savgol-Filter dQ/dV / mAh/V'))                                        # which values are shown on the y axis
    
        frame1.set_xlabel(r'$ Theoretical$ $Quantile $')                                              # Label of the x axis
        #ax.set_xscale('log')
        #frame1.set_xlim(Xmin_extended, Xmax_extended)                                                         # minimum and maximum value shown on the x axis
        #frame1.set_xticks([])                               # which values are shown on the x axis

        # Saving setups
        index_to_save = cycle_to_save - 1
        
        # Legend above the plot and saving (legend first, so it is in the saved file)
        Matplotlib_Legend_Above_And_Save(frame1, 'Q-Q Plot for %s: %s'  %(label_name, label_value), i == index_to_save, './images/qq_plot_%s%s_%s.png' %(label_name, label_value, additional_name))
        
        plot = plt.show(block=False)
    
    return plot


def Matplotlib_Correlogram(acf_array_lag, acf_array, color):
    """Plot of the autocorrelation function against the lag.
    acf_array_lag = lags, acf_array = ACF values, color = colour."""
    ##### Plot the autocorrelation function against the lag
    fig = plt.figure()
    Set_Figure_Size_For_Plot_Area(fig) # was: fig.set_size_inches(3.4,3.4)
    plt.rcParams.update(pgf_with_latex)

    plt.plot(acf_array_lag ,acf_array , color, linestyle='None', marker='.', linewidth=1.5)

    ax = plt.gca()
    ax.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))

    ax.set_ylabel(r'$Autocorrelation$')				                # Label of the y axis
    ax.set_xlabel(r'$Lag$ / points')                                              # Label of the x axis

    plot = plt.show(block=False)                                                       # Shows the plot, but the following code keeps running

    return plot


def Matplotlib_Dendrogram(model, **kwargs):
    """Dendrogram of a fitted sklearn AgglomerativeClustering model (from the scikit-learn example).
    model = fitted model (with distance_threshold set), **kwargs = passed to scipy dendrogram."""
    # Taken from the scikit-learn example "Plot Hierarchical Clustering Dendrogram"
    # https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html

    # Children of hierarchical clustering
    children = model.children_

    # Distances between each pair of children
    # Since we don't have this information, we can use a uniform one for plotting
    distance = np.arange(children.shape[0])

    # The number of observations contained in each cluster level
    no_of_observations = np.arange(2, children.shape[0]+2)

    # Create linkage matrix and then plot the dendrogram
    linkage_matrix = np.column_stack([children, distance, no_of_observations]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
