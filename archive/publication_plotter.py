"""Matplotlib helpers for publication-quality figures.

Moved here from `scientific_utils/publication_plotter.py` (nothing in the repository called these functions)."""

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import matplotlib.colors as mcolors
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt


def set_publication_style(base_font_size=12, font_family='sans-serif', use_latex=False):
    """
    Configures Matplotlib to output publication-quality figures meant for Inkscape.
    """
    # RESET defaults
    plt.rcParams.update(plt.rcParamsDefault)

    # 1. INKSCAPE COMPATIBILITY (CRITICAL)
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['pdf.fonttype'] = 42
    
    # 2. FONTS
    plt.rcParams['font.family'] = font_family
    if font_family == 'sans-serif':
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    elif font_family == 'serif':
        plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
    
    plt.rcParams['font.size'] = base_font_size
    plt.rcParams['axes.labelsize'] = base_font_size + 2
    plt.rcParams['axes.titlesize'] = base_font_size + 4
    plt.rcParams['legend.fontsize'] = base_font_size
    plt.rcParams['xtick.labelsize'] = base_font_size
    plt.rcParams['ytick.labelsize'] = base_font_size
    
    # 3. TICKS & AXES
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    
    print("✅ Style set for publication. Text export set to editable.")


def create_figure(width_cm=16.0, height_cm=10.0, dpi=300, layout='constrained'):
    """
    Creates a figure with exact dimensions in centimeters.
    """
    figsize_inch = (width_cm / 2.54, height_cm / 2.54)
    fig, ax = plt.subplots(figsize=figsize_inch, dpi=dpi, layout=layout)
    return fig, ax


def save_plot(filename, dpi=300, fig=None):
    """
    Saves the figure in both SVG (for Inkscape) and PNG (for preview) formats.
    """
    if filename.endswith('.svg') or filename.endswith('.png'):
        filename = filename.rsplit('.', 1)[0]

    if fig is None:
        fig = plt.gcf()

    fig.savefig(f"{filename}.svg", format='svg', bbox_inches='tight')
    fig.savefig(f"{filename}.png", format='png', dpi=dpi, bbox_inches='tight')
    print(f"💾 Saved: {filename}.svg & {filename}.png")


def inspect_file(filepath, delimiter=None):
    """
    Prints column names and indices of a file.
    """
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    try:
        if delimiter is None:
            df = pd.read_csv(filepath, sep=None, engine='python', nrows=5)
        else:
            df = pd.read_csv(filepath, delimiter=delimiter, nrows=5)
            
        print(f"📂 File: {os.path.basename(filepath)}")
        print("-" * 40)
        print(f"{'INDEX':<8} | {'COLUMN NAME'}")
        print("-" * 40)
        for i, col in enumerate(df.columns):
            print(f"{i:<8} | {col}")
        print("-" * 40)
        
    except Exception as e:
        print(f"Error reading file: {e}")


def load_csv_data(filepath, x_col=0, y_col=1, delimiter=None, skip_rows=0):
    """
    Robust data loader using Pandas.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        if delimiter is None:
            df = pd.read_csv(filepath, sep=None, engine='python', skiprows=skip_rows)
        else:
            df = pd.read_csv(filepath, delimiter=delimiter, skiprows=skip_rows)
    except Exception as e:
        print(f"Error reading file: {e}")
        return np.array([]), np.array([])

    # Helper to safely extract column by index or name
    def get_col(df, col_id):
        if isinstance(col_id, int):
            return df.iloc[:, col_id].values
        return df[col_id].values

    return get_col(df, x_col), get_col(df, y_col)


def apply_axis_style(
    ax, 
    # Titles & Labels
    title=None, xlabel=None, ylabel=None,
    font_size_label=12, font_weight_label='normal', label_color='black',
    
    # Limits & Scales
    x_lim=None, y_lim=None, x_scale='linear', y_scale='linear', aspect='auto',
    
    # Spines
    spines_visible=['left', 'bottom'], spine_linewidth=1.5, spine_color='black',
    
    # Grid
    grid=False, grid_axis='both', grid_linestyle=':', grid_linewidth=0.5, grid_color='#bdbdbd',
    
    # Ticks
    x_ticks=None, y_ticks=None, x_tick_labels=None, y_tick_labels=None,
    x_tick_direction='in', y_tick_direction='in',
    x_tick_length=6, y_tick_length=6, x_tick_width=1.0, y_tick_width=1.0,
    tick_color='black',
    x_minor_ticks=False, y_minor_ticks=False
):
    """
    Applies precise styling to a specific axis. 
    You can call this AFTER you have plotted your data.
    """
    # 1. Labels & Title
    if xlabel: ax.set_xlabel(xlabel, fontsize=font_size_label, fontweight=font_weight_label, color=label_color)
    if ylabel: ax.set_ylabel(ylabel, fontsize=font_size_label, fontweight=font_weight_label, color=label_color)
    if title: ax.set_title(title, fontsize=font_size_label + 2, fontweight='bold', color=label_color)
    
    # 2. Limits & Scales
    if x_lim: ax.set_xlim(x_lim)
    if y_lim: ax.set_ylim(y_lim)
    ax.set_xscale(x_scale)
    ax.set_yscale(y_scale)
    ax.set_aspect(aspect)
    
    # 3. Spines (Borders)
    for spine_loc, spine in ax.spines.items():
        if spine_loc in spines_visible:
            spine.set_visible(True)
            spine.set_linewidth(spine_linewidth)
            spine.set_color(spine_color)
        else:
            spine.set_visible(False)
            
    # Handle ticks for hidden spines
    if 'bottom' not in spines_visible: ax.xaxis.set_ticks_position('none')
    if 'left' not in spines_visible: ax.yaxis.set_ticks_position('none')

    # 4. Ticks
    # Major ticks
    ax.tick_params(axis='x', direction=x_tick_direction, length=x_tick_length, 
                   width=x_tick_width, colors=tick_color)
    ax.tick_params(axis='y', direction=y_tick_direction, length=y_tick_length, 
                   width=y_tick_width, colors=tick_color)
    
    if x_ticks is not None: ax.set_xticks(x_ticks)
    if y_ticks is not None: ax.set_yticks(y_ticks)
    if x_tick_labels is not None: ax.set_xticklabels(x_tick_labels)
    if y_tick_labels is not None: ax.set_yticklabels(y_tick_labels)
    
    # Minor ticks
    if x_minor_ticks: 
        ax.minorticks_on()
        ax.tick_params(axis='x', which='minor', direction=x_tick_direction, length=x_tick_length*0.5)
    if y_minor_ticks: 
        ax.minorticks_on()
        ax.tick_params(axis='y', which='minor', direction=y_tick_direction, length=y_tick_length*0.5)
        
    # 5. Grid
    if grid:
        ax.grid(True, axis=grid_axis, linestyle=grid_linestyle, 
                linewidth=grid_linewidth, color=grid_color)


def apply_legend_style(
    ax, 
    title=None, loc='best', bbox_to_anchor=None, 
    frameon=False, ncol=1, font_size=10
):
    """
    Helper to style the legend separately.
    """
    # Only create legend if labels exist
    if ax.get_legend_handles_labels()[1]:
        ax.legend(title=title, loc=loc, bbox_to_anchor=bbox_to_anchor,
                  frameon=frameon, ncol=ncol, fontsize=font_size, title_fontsize=font_size)


def plot_gradient_fill(ax, x, y, color_start, color_end, y_base=0):
    """
    Fills the area under a curve with a vertical color gradient.
    """
    # 1. Plot the main line
    line, = ax.plot(x, y, color=color_end, linewidth=2, zorder=10)
    
    # 2. Create gradient background
    z = np.empty((100, 1, 4), dtype=float)
    rgb_start = mcolors.to_rgba(color_start)
    rgb_end = mcolors.to_rgba(color_end)
    
    for i in range(100):
        factor = i / 99.0
        z[i, 0, :] = [rgb_start[j] * (1 - factor) + rgb_end[j] * factor for j in range(4)]

    # 3. Determine extent (bounds) ensuring we cover negative values
    xmin, xmax = x.min(), x.max()
    ymin = min(y.min(), y_base) 
    ymax = max(y.max(), y_base) * 1.1 

    im = ax.imshow(z, aspect='auto', extent=[xmin, xmax, ymin, ymax], origin='lower', zorder=1)

    # 4. Clip the image to the shape of the curve
    from matplotlib.patches import Polygon
    verts = [(x[0], y_base)] + list(zip(x, y)) + [(x[-1], y_base)]
    poly = Polygon(verts, facecolor='none')
    ax.add_patch(poly)
    im.set_clip_path(poly)
    return line


def add_inset_zoom(ax, x, y, x_range, y_range, loc='upper right'):
    """
    Adds a magnified inset to the plot.
    """
    axins = inset_axes(ax, width="40%", height="30%", loc=loc)
    axins.plot(x, y, color=ax.lines[0].get_color(), linewidth=1.5)
    axins.set_xlim(*x_range)
    axins.set_ylim(*y_range)
    axins.tick_params(axis='both', which='major', labelsize=8)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
    return axins


def setup_broken_xaxis(fig, break_start, break_end, ratio=[1, 3]):
    """
    Creates two subplots side-by-side to simulate a broken X-axis.
    """
    gs = fig.add_gridspec(1, 2, width_ratios=ratio, wspace=0.05)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    ax1.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax1.tick_params(labelright=False)
    ax2.tick_params(left=False)
    
    d = .015
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
    ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)
    ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
    
    kwargs.update(transform=ax2.transAxes)
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)
    ax2.plot((-d, +d), (-d, +d), **kwargs)
    
    return ax1, ax2


def plot_color_evolution(fig, ax, x, y_data_list, param_values, cmap_name='viridis', cb_label='Parameter'):
    """
    Plots multiple curves with a color gradient.
    """
    cmap = plt.get_cmap(cmap_name)
    norm = mcolors.Normalize(vmin=min(param_values), vmax=max(param_values))
    scalar_mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    for i, y_curve in enumerate(y_data_list):
        val = param_values[i]
        color = cmap(norm(val))
        ax.plot(x, y_curve, color=color, linewidth=1.5, alpha=0.8)
        
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = fig.colorbar(scalar_mappable, cax=cax, orientation='vertical')
    cbar.set_label(cb_label)
    return cbar
