"""Baseline correction, peak areas and Gauss fits of diffractograms."""

import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse import linalg
from numpy.linalg import norm
from lmfit import Parameters, minimize
from lmfit.printfuncs import report_fit


def Baseline_arPLS(y, ratio=1e-6, lam=100, niter=10, full_output=False):
    """Baseline of a spectrum with asymmetrically reweighted penalized least squares (arPLS, Baek et al. 2015).
    y = intensities (array), ratio = stop criterion, lam = smoothness (larger -> stiffer baseline), niter = maximum number of iterations,
    full_output = True -> (baseline, y - baseline, info) instead of the baseline only."""
    # Baseline correction with asymmetrically reweighted penalized least squares (arPLS)
    # Baek et al., Analyst 140 (2015) 250: https://pubs.rsc.org/en/content/articlehtml/2015/an/c4an01061b
    # Implementation taken from: https://stackoverflow.com/questions/29156532/python-baseline-correction-library
    L = len(y)

    diag = np.ones(L - 2)
    D = sparse.spdiags([diag, -2*diag, diag], [0, -1, -2], L, L - 2)

    H = lam * D.dot(D.T)  # The transposes are flipped w.r.t the Algorithm on pg. 252

    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)

    crit = 1
    count = 0

    while crit > ratio:
        z = linalg.spsolve((W + H).tocsc(), W * y)
        d = y - z
        dn = d[d < 0]

        m = np.mean(dn)
        s = np.std(dn)

        with np.errstate(over='ignore'):  # exp overflows for points far above the baseline -> weight 0, as intended
            w_new = 1 / (1 + np.exp(2 * (d - (2*s - m))/s))

        crit = norm(w_new - w) / norm(w)

        w = w_new
        W.setdiag(w)  # Do not create a new matrix, just update diagonal values

        count += 1

        if count > niter:
            print('Maximum number of iterations exceeded')
            break

    if full_output:
        info = {'num_iter': count, 'stop_criterion': crit}
        return z, d, info
    else:
        return z


def Baseline_Correction_Whole_Dataframe(dataframe, y_values_column_name, lam):
    """Intensity minus its arPLS baseline, calculated over the whole diffractogram (before a peak range is selected).
    dataframe, y_values_column_name, lam = smoothness of the baseline. Returns the corrected series."""
    ########## Baseline of the whole diffractogram ##########
    # the baseline is calculated before a peak range is selected: in a narrow range around a peak
    # there are too few background points and the baseline is pulled up into the peak
    baseline = Baseline_arPLS(dataframe[y_values_column_name].to_numpy(), ratio=1e-6, lam=lam, niter=10, full_output=False)
    return dataframe[y_values_column_name] - baseline


def Determine_Peak_Area_Summed(dataframe, x_values_column_name, y_values_column_name, x_lower_limit, x_upper_limit, lam, color_area):
    """Peak area without fitting: baseline correction of the whole diffractogram, then the corrected points between the two limits are summed up as rectangles
    (and drawn filled into the current figure). x limits in degree 2theta; area in counts times degree. color_area = fill colour. Returns the area."""
    ########## Area of a peak by summing up the data points (instead of fitting a function) ##########
    ##### Baseline Correction
    y_corrected_complete = Baseline_Correction_Whole_Dataframe(dataframe, y_values_column_name, lam)

    # defines the x values
    x = dataframe[x_values_column_name]

    # extracting the selected range of data by the upper and lower limit
    boolean_variables = x.between(x_lower_limit,x_upper_limit) # returns 'True' for the rows where the value is in the given range (lower_limit to upper_limit)

    # defining x and y new in the selected x range
    x = x[boolean_variables]
    y_corrected = y_corrected_complete[boolean_variables]
    plt.plot(x, y_corrected, alpha=0.75, marker='.', markersize=7, markeredgecolor='black', markeredgewidth=0.1, label='baseline corrected %s° to %s°' %(x_lower_limit, x_upper_limit), linestyle='-', linewidth=0.5)

    ##### Summing up the area of every data point (rectangle between two points)
    area = 0
    for i in range(0, len(y_corrected)-1):
        plt.fill_between([x.iloc[i],x.iloc[i+1]], y_corrected.min(), y_corrected.iloc[i], facecolor=color_area, alpha=0.5)
        area += y_corrected.iloc[i] * (x.iloc[i+1] - x.iloc[i])

    print('The area of the summed up points are: %s' %(area))

    return area


def Gauss_Function(pars, x):
    """Sum of one, two or three Gaussian peaks (area-normalised: amp is the peak area).
    pars = lmfit Parameters amp1, sigma1, cen1 (+ amp2, sigma2, cen2, + amp3, ...), x = x values. Returns the model y values."""
    ############ Sum of one, two or three Gaussian functions depending on the number of parameters ##############
    # defining fitting function/model with Parameter() class of lmfit module
    if len(pars) == 3:
        amp = pars['amp1'].value # the value of the entry "amp1" of the "Parameters" class is defined as amp
        sigma = pars['sigma1'].value
        cen = pars['cen1'].value

        y_model = amp*(1/(sigma*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen)/sigma)**2)))

        return y_model

    elif len(pars) == 6:
        amp1 = pars['amp1'].value
        sigma1 = pars['sigma1'].value
        cen1 = pars['cen1'].value

        amp2 = pars['amp2'].value
        sigma2 = pars['sigma2'].value
        cen2 = pars['cen2'].value

        y_model = amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2))) + \
            amp2*(1/(sigma2*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen2)/sigma2)**2)))

        return y_model

    elif len(pars) == 9:
        amp1 = pars['amp1'].value
        sigma1 = pars['sigma1'].value
        cen1 = pars['cen1'].value

        amp2 = pars['amp2'].value
        sigma2 = pars['sigma2'].value
        cen2 = pars['cen2'].value

        amp3 = pars['amp3'].value
        sigma3 = pars['sigma3'].value
        cen3 = pars['cen3'].value

        y_model = amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2))) + \
            amp2*(1/(sigma2*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen2)/sigma2)**2))) + \
            amp3*(1/(sigma3*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen3)/sigma3)**2)))

        return y_model


def Fit_Two_Gauss_Peaks(dataframe, x_values_column_name, y_values_column_name, x_lower_limit, x_upper_limit, lam, FitParameters):
    """Fits two Gaussian peaks to the baseline-corrected data between the two limits (lmfit, Nelder-Mead), prints the fit report
    and draws data, fit and both single peaks into the current figure.
    FitParameters = lmfit Parameters amp1, sigma1, cen1, amp2, sigma2, cen2 (start values and limits), lam = baseline smoothness.
    Returns the lmfit result."""
    ########## Fit of two Gaussian functions to a part of the data after a baseline correction ##########
    # FitParameters: lmfit Parameters() with amp1, sigma1, cen1, amp2, sigma2, cen2 (start, min and max values)
    ##### Baseline Correction
    y_corrected_complete = Baseline_Correction_Whole_Dataframe(dataframe, y_values_column_name, lam)

    x = dataframe[x_values_column_name]

    # extracting the selected range of data by the upper and lower limit
    boolean_variables = x.between(x_lower_limit,x_upper_limit) # returns 'True' for the rows where the value is in the given range (lower_limit to upper_limit)

    # defining x and y new in the selected x range
    x = x[boolean_variables]
    y = y_corrected_complete[boolean_variables]
    plt.plot(x, y, alpha=0.75, marker='.', markersize=7, markeredgecolor='black', markeredgewidth=0.1, label='baseline corrected data', linestyle='-', linewidth=0.5)

    ##### Fitting
    # defining the function to minimize
    def residuals(FitParameters, x, y):
        y_model = Gauss_Function(FitParameters, x)
        residuals = y - y_model
        return residuals

    # searches the minimum of the residuals function by optimizing the parameters
    result_minimize = minimize(fcn=residuals, params=FitParameters,  args=(x, y), method='nelder')

    # reports the parameters of the minimization
    report_fit(result_minimize, show_correl=False)

    # calculation of the y values with the optimized parameters (given by 'result_minimize.params')
    y_from_optimized_parameters = Gauss_Function(result_minimize.params, x)

    # plotting the result
    plt.plot(x, y_from_optimized_parameters, 'y', linestyle='None', marker='.', label=r'fitted', linewidth=1.5)

    ##### Plotting the separate functions
    # Generates a List of the values of the optimized parameters from the Parameter() class
    parameter_list_first_gauss = list(result_minimize.params.valuesdict().values())[0:3]

    ParametersFirstGauss = Parameters() # Parameters is a function of the lmfit package
    ParametersFirstGauss.add('amp1', value=parameter_list_first_gauss[0])
    ParametersFirstGauss.add('sigma1', value=parameter_list_first_gauss[1])
    ParametersFirstGauss.add('cen1', value=parameter_list_first_gauss[2])

    parameter_list_second_gauss = list(result_minimize.params.valuesdict().values())[3:6]

    ParametersSecondGauss = Parameters()
    ParametersSecondGauss.add('amp1', value=parameter_list_second_gauss[0])
    ParametersSecondGauss.add('sigma1', value=parameter_list_second_gauss[1])
    ParametersSecondGauss.add('cen1', value=parameter_list_second_gauss[2])

    # Calculating y values
    y_first_Gauss = Gauss_Function(ParametersFirstGauss, x)
    y_second_Gauss = Gauss_Function(ParametersSecondGauss, x)

    plt.fill_between(x, y_first_Gauss.min(), y_first_Gauss, facecolor="green", alpha=0.5, label='first Gauss')
    plt.fill_between(x, y_second_Gauss.min(), y_second_Gauss, facecolor="yellow", alpha=0.5, label='second Gauss')

    return result_minimize
