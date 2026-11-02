"""Unused functions moved here from `scientific_utils/statistics/analysis.py` (nothing in the repository called them)."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


def Calculate_Fast_Fourier_Transform(dataframe, x_values_column_name, y_values_column_name):
    """Power spectrum |FFT(y)|^2 (shifted so that the low frequencies are in the middle), also drawn into the current figure.
    dataframe, x_values_column_name (not used for the calculation), y_values_column_name.
    Returns [X, Y]: X = frequency index (-N/2 ... N/2), Y = power."""
    ################################################
    ########## defines the x and y values ##########
    ################################################
    x = dataframe[x_values_column_name]
    y = dataframe[y_values_column_name]
    
    ##### Calculating Power spectrum of Y (This Y is plottet)
    Y = np.abs(np.fft.fftshift(np.fft.fft(y)))**2 # shifted the array by half its length with the np.fft.fftshift function. FT results in imaginary and real values for this reason we calculate the absolute value

    ##### Calculating the X axes in the Fourier space
    X = np.arange(Y.shape[0]) - Y.shape[0]//2 # hat the Fourier transform of a (real-valued) signal of size N (N pixels) has only N/2 independent values. You can see in the second plot that the power spectrum is symmetric with respect to the central point.
    # In this way the power spectrum values close to the central point (fpix close to zero) correspond to the ‘low frequencies’ of our signal, i.e. the amount of signal associated with slowly varying parts of the spectrum. 
    #Conversely, the ‘high frequency’ part of the power spectrum is associated with the fast moving regions of the original signal (should be the noise in the original signal). 
    
    ##### plotting
    plt.plot(X, Y, color='violet', alpha=0.80, marker='.', markersize=8, markeredgecolor='black', markeredgewidth=0.1, label='Y-Data Fast Fourier Transformed', linestyle='-', linewidth=0.8)
   
    return [X, Y]
