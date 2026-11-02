"""XPS spectra and depth profile plots."""

from colour import Color
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import re
import pandas as pd
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from scientific_utils.general.plotting import Convert_cm_To_inch
from scientific_utils.general.plotting import my_colormap
from scientific_utils.general.plotting import Set_Figure_Size_For_Plot_Area
from scientific_utils.publication_plotly import OVERVIEW_W_CM, OVERVIEW_H_CM, SHOW_LEGEND
from scientific_utils.publication_plotly import apply_style
from scientific_utils.general.plotting import pgf_with_latex
from scientific_utils.publication_plotly import add_side_legend, color_series, legend_size, pt, to_rgba
from scientific_utils.publication_plotly import ANNOT_FONT_PT, PLOT_H_CM, PLOT_W_CM, SPEC_H_CM, SPEC_W_CM


def radar_factory(num_vars, frame='circle'):
    # taken from the Matplotlib gallery example "Radar chart (aka spider or star chart)":
    # https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)


        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)


                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def Matplotlib_SpiderWeb_Plot(dataframe, SpiderWebParameters):
    """Spider web (radar) plot: one closed curve per row of the dataframe over the selected columns (e.g. atomic % of the elements).
    SpiderWebParameters = dictionary with 'list_of_column_names', curve styles, labels, axis styles, title/legend options and
    'list_for_saving_options' = [True/False, name] -> ./images/<name>.png."""
    ##### Define which Dataframe is used for plotting
    data = dataframe

    ##### Define the Columns used
    column_names = SpiderWebParameters.get('list_of_column_names')

    ##### Extract Data for Plotting in form of a Dictonary
    extract_data_dict = {}
    for i in column_names:
        dict_values = data[i].values.tolist()
        extract_data_dict[i] = dict_values

    ##### Tranform Dictonary to Dataframe
    data_new = pd.DataFrame.from_dict(extract_data_dict)

    ##### Define the Shape of the Plot according to the amount of columns
    N = len(data_new.columns)
    theta = radar_factory(N, frame='polygon')

    ##### Use of the Defined Paramterts for Font, Font Size, .....
    plt.rcParams.update(pgf_with_latex)

    ##### Define the Figure
    fig, ax = plt.subplots(figsize=(Convert_cm_To_inch(12, 12)), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    Set_Figure_Size_For_Plot_Area(fig, OVERVIEW_W_CM, OVERVIEW_W_CM) # square radar plot, was figsize 12 x 12 cm

    ##### Plot for every row in the Daraframe a curve
    list_of_list_of_Curve_style_options = SpiderWebParameters.get('list_of_list_of_Curve_style_options')
    for i in data_new.index:
        color_graph = list_of_list_of_Curve_style_options[i][0]
        transparency = list_of_list_of_Curve_style_options[i][1]
        graph_name = list_of_list_of_Curve_style_options[i][2]
        data_list = data_new.iloc[i].tolist()
        ax.plot(theta, data_list, color=color_graph, label=graph_name)
        ax.fill(theta, data_list,  alpha=transparency, color=color_graph)

    ##### Set the labels
    list_of_labels = SpiderWebParameters.get('list_of_labels')
    ax.set_varlabels(list_of_labels)

    ##### Axis Styles
    list_of_axis_style_options = SpiderWebParameters.get('list_of_axis_style_options')
    if list_of_axis_style_options[0] == 'Yes':
        ax.set_rgrids(list_of_axis_style_options[1])

    ##### Title Options
    list_for_title_legend_options = SpiderWebParameters.get('list_for_title_legend_options')
    ax.set_title(list_for_title_legend_options[0],  position=(0.5, 1.3), ha='center')

    ax.legend(title=list_for_title_legend_options[1], loc='upper left', bbox_to_anchor=(1.1, 1.0))

    ##### Options for Saving
    list_for_saving_options = SpiderWebParameters.get('list_for_saving_options')
    if list_for_saving_options[0] == True:
        plt.savefig('./images/%s.png' %(list_for_saving_options[1]))

    plot = plt.show(block=False)

    return plot


# ── Publication style spectra (Plotly, CasaXPS exports) ───────────
# moved here from publication_plotly.py: they need the CasaXPS column layout

# Waterfall
DEFAULT_OFFSET = 1.15

# Filled peak components
COMPONENT_ALPHA = 0.35

_ORBITAL = re.compile(r'^[A-Z][a-z]?\s*\d\s*[spdf]\d?\s*/\s*')

_trapz = getattr(np, 'trapezoid', None) or np.trapz   # np.trapz is gone in NumPy 2


def split_columns(df: pd.DataFrame) -> dict:
    '''CasaXPS column layout: x | raw | components... | background | envelope | unnamed'''
    return dict(x=df.columns[0], raw=df.columns[1], comps=list(df.columns[2:-3]),
                bg=df.columns[-3], env=df.columns[-2])


def clean_names(cols) -> list:
    ''''C1s 3:C 1s / C-C/C-H.4' -> 'C-C/C-H'  (duplicates get a running number).'''
    out, seen = [], {}
    for c in cols:
        n = str(c).split(':')[-1].strip()
        n = re.sub(r'\.\d+$', '', n)      # pandas de-duplication suffix
        n = _ORBITAL.sub('', n).strip()   # leading 'C 1s / '
        seen[n] = seen.get(n, 0) + 1
        out.append(n if seen[n] == 1 else f'{n} ({seen[n]})')
    return out


def add_filled_component(fig, x, y_comp, y_base, name, color,
                         alpha=COMPONENT_ALPHA, group=None):
    '''Fitted component drawn as an area between the component and the background.'''
    group = group or name
    # invisible baseline: the reference curve that 'tonexty' fills down to
    fig.add_scatter(x=x, y=y_base, mode='lines', line=dict(width=0),
                    hoverinfo='skip', showlegend=False, legendgroup=group)
    fig.add_scatter(x=x, y=y_comp, mode='lines', name=name, fill='tonexty',
                    fillcolor=to_rgba(color, alpha),
                    line=dict(color=color, width=1.0, dash='solid'),
                    legendgroup=group, showlegend=False)
    return fig


def plot_spectrum_with_components(df, label=None, legend=True):
    '''One spectrum: raw data, background, envelope and the filled components.'''
    c = split_columns(df)
    x = df[c['x']]
    comps, names = c['comps'], clean_names(c['comps'])
    colors = color_series(max(len(comps), 1))

    fig = go.Figure()
    for k, col in enumerate(comps):
        add_filled_component(fig, x, df[col], df[c['bg']], names[k], colors[k])
    fig.add_scatter(x=x, y=df[c['bg']], mode='lines', name='Background',
                    line=dict(color='grey', width=1.0, dash='dot'), showlegend=False)
    if comps:
        fig.add_scatter(x=x, y=df[c['env']], mode='lines', name='Envelope',
                        line=dict(color='black', width=1.2), showlegend=False)
    fig.add_scatter(x=x, y=df[c['raw']], mode='markers', name='Raw data',
                    marker=dict(color='black', size=2.5, symbol='circle-open',
                                line=dict(width=0.8)), showlegend=False)

    entries = [(n, colors[k], 'fill') for k, n in enumerate(names)]
    entries.append(('Background', 'grey', 'dash'))
    if comps:
        entries.append(('Envelope', 'black', 'line'))
    entries.append(('Raw data', 'black', 'marker'))
    if not legend:
        entries = []

    right, bottom = legend_size(entries, PLOT_H_CM)
    apply_style(fig, '<i>Binding Energy</i> / eV', '<i>Intensity</i> / a.u.',
                plot_w_cm=PLOT_W_CM, plot_h_cm=PLOT_H_CM,
                x_tickformat=None,                       # eV, no SI prefixes
                y_ticklabels=False, y_ticks='', y_minor=False, y_tickformat=None,
                extra_right_px=right, extra_bottom_px=bottom)
    add_side_legend(fig, entries, PLOT_W_CM, PLOT_H_CM)
    if label:
        fig.add_annotation(xref='paper', x=0.03, yref='paper', y=0.97, text=label,
                           xanchor='left', yanchor='top', showarrow=False,
                           font=dict(size=pt(ANNOT_FONT_PT), color='black'))
    fig.update_xaxes(autorange='reversed')               # XPS convention
    return fig


def area_between(df, x_col, y_col, bg_col, lower=None, upper=None) -> float:
    '''Area between a curve and the background, optionally within [lower, upper] eV.'''
    d = df
    if lower is not None and upper is not None:
        d = df[df[x_col].between(min(lower, upper), max(lower, upper))]
    if d.empty:
        return 0.0
    return float(np.abs(_trapz(d[y_col].values - d[bg_col].values, d[x_col].values)))


def sample_of(df: pd.DataFrame, sample_labels=None) -> str:
    '''Sample label from the CasaXPS raw-data column name.'''
    m = re.search(r'\(\s*\d+\s*,\s*([^)]+)\)', str(df.columns[1]))
    key = m.group(1).strip() if m else str(df.columns[1])
    return sample_labels.get(key, key)


def plot_waterfall(dfs, labels, with_components=False, offset=DEFAULT_OFFSET,
                   legend=True, annotate=True, annot_x=0.03, annot_dy=0.55,
                   plot_w_cm=SPEC_W_CM, plot_h_cm=SPEC_H_CM, sample_colors=None):
    '''All samples of one element stacked on top of each other.

    with_components=False -> one coloured line per sample (sample colours)
    with_components=True  -> black raw curve + filled components per sample,
                             the samples are told apart by the annotation.
    Each spectrum is scaled to 0...1 first so the stacking distance is
    independent of the count rate.

    annot_x / annot_dy place the sample label inside the plot (paper x, data y);
    move annot_x to the right for spectra that are busy on the high-BE side
    (e.g. the survey scan).
    '''
    fig = go.Figure()
    comp_names = clean_names(split_columns(dfs[0])['comps']) if dfs else []
    comp_colors = color_series(max(len(comp_names), 1))

    for j, (df, lab) in enumerate(zip(dfs, labels)):
        c = split_columns(df)
        x, raw = df[c['x']], df[c['raw']]
        lo = raw.min()
        span = (raw.max() - lo) or 1.0
        shift = j * offset
        norm = lambda s: (s - lo) / span + shift

        if with_components:
            for k, col in enumerate(c['comps']):
                add_filled_component(fig, x, norm(df[col]), norm(df[c['bg']]),
                                     comp_names[k], comp_colors[k],
                                     group=comp_names[k])
            fig.add_scatter(x=x, y=norm(df[c['bg']]), mode='lines', name='Background',
                            line=dict(color='grey', width=0.8, dash='dot'),
                            showlegend=False, legendgroup='bg')
            fig.add_scatter(x=x, y=norm(raw), mode='lines', name=f'{lab} raw',
                            line=dict(color='black', width=1.2), showlegend=False)
        else:
            fig.add_scatter(x=x, y=norm(raw), mode='lines', name=lab,
                            line=dict(color=sample_colors.get(lab, 'black'), width=1.5),
                            showlegend=False)

        if annotate:
            # xref='paper' -> the label cannot stretch the binding-energy range
            fig.add_annotation(xref='paper', x=annot_x, y=shift + annot_dy, text=lab,
                               xanchor='left', yanchor='bottom', showarrow=False,
                               font=dict(size=pt(ANNOT_FONT_PT), color='black'))

    if not legend:
        entries = []
    elif with_components:
        entries = [(n, comp_colors[k], 'fill') for k, n in enumerate(comp_names)]
        entries += [('Background', 'grey', 'dash'), ('Raw data', 'black', 'line')]
    elif annotate:
        entries = []   # the sample names are already written next to the curves
    else:
        entries = [(lab, sample_colors.get(lab, 'black'), 'line') for lab in labels]

    right, bottom = legend_size(entries, plot_h_cm)
    apply_style(fig, '<i>Binding Energy</i> / eV', '<i>Intensity</i> / a.u.',
                plot_w_cm=plot_w_cm, plot_h_cm=plot_h_cm,
                x_tickformat=None,
                y_ticklabels=False, y_ticks='', y_minor=False, y_tickformat=None,
                extra_right_px=right, extra_bottom_px=bottom)
    add_side_legend(fig, entries, plot_w_cm, plot_h_cm)
    fig.update_xaxes(autorange='reversed')
    return fig
