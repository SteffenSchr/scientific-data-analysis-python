"""Unused functions moved here from `scientific_utils/impedance/plotting.py` (nothing in the repository called them)."""

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker

from scientific_utils.general.plotting import list_of_Hexcolors
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.general.plotting import pgf_with_latex
from scientific_utils.publication_plotly import my_color_scale
from scientific_utils.impedance.analysis import Calculate_Impedance_RQ_Model


def BodePlotimpedance_model(f, ModelValues, label, impedance_model=None):
    """Model impedance against frequency (log axis). Note: the complex Z is passed to plt.plot, so Matplotlib draws only its real part.
    Same inputs as Matplotlib_Nyquist_Plot. Returns the plot."""
    # the RQ model is used if no other model is given
    if impedance_model is None:
        impedance_model = Calculate_Impedance_RQ_Model
    fig = plt.figure()
    Set_Figure_Size_For_Plot_Area(fig) # was: fig.set_size_inches((2.5*3.4),3.4)
    plt.rcParams.update(pgf_with_latex)

    plot = plt.plot(f, impedance_model(f, ModelValues, PhaseAngle=False), lw=1, label=label)
    
    ax = plt.gca()
    ax.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
    ax.set_xscale('log')

    plt.legend(fontsize=12)

    plt.title("Bode Plot", fontsize=14)
    plt.ylabel('-Z absolute / Ohm')
    plt.xlabel('frequency (Hz)')
               
    return plot


def Matplotlib_Bode_Plot_Phase_Angle(f, ModelValues, label, impedance_model=None):
    """Phase angle (degree) of an impedance model against frequency (log axis). Same inputs as Matplotlib_Nyquist_Plot. Returns the plot."""
    # the RQ model is used if no other model is given
    if impedance_model is None:
        impedance_model = Calculate_Impedance_RQ_Model
    fig = plt.figure()
    Set_Figure_Size_For_Plot_Area(fig) # was: fig.set_size_inches((2.5*3.4),3.4)
    plt.rcParams.update(pgf_with_latex)

    plot = plt.plot(f, impedance_model(f, ModelValues, PhaseAngle=True), lw=1, label=label)
    
    ax = plt.gca()
    ax.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
    ax.set_xscale('log')

    plt.legend(fontsize=12)

    plt.title("Bode Plot", fontsize=14)
    plt.ylabel('phase angle')
    plt.xlabel('frequency (Hz)')

    return plot
