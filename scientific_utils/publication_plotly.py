"""Plotly helpers for publication-quality figures (fixed plot size in cm, fonts in pt, side legends)."""

import plotly.graph_objects as go
import numpy as np
import plotly.colors as pcol
import pandas as pd
import plotly.express as px
import plotly.io as pio
import re

# ── Kaleido 0.2.1 ─────────────────────────────────────────────────
# Its old Chromium can freeze write_image forever on newer PCs (kaleido.exe crashes
# with 0xc0000409). Without the V8 optimizer the export works and the SVGs stay the same.
_KALEIDO_FLAG = "--js-flags=--no-opt"
_kaleido_scope = getattr(pio.kaleido, "scope", None)
if hasattr(_kaleido_scope, "chromium_args") and _KALEIDO_FLAG not in _kaleido_scope.chromium_args:
    _kaleido_scope.chromium_args = (*_kaleido_scope.chromium_args, _KALEIDO_FLAG)

# ══ Physical basis ══════════════════════════════════════════════
# SVG defines 1 inch = 96 CSS px. Deriving every length from 96 makes
# the exported SVG physically honest in Inkscape / LaTeX: the plot
# rectangle comes out at its true cm size and fonts read as true pt.
PX_PER_IN = 96

DPI_SCREEN = PX_PER_IN  # legacy alias used by per-figure size overrides

# ── The black rectangle (plot area) — one fixed size per figure CLASS ──
PLOT_W_CM, PLOT_H_CM = 4.0, 3.3   # single spectrum / general purpose
SPEC_W_CM, SPEC_H_CM = 4.0, 6.0   # waterfall: several spectra stacked
BAR_W_CM,  BAR_H_CM  = 6.0, 3.3   # bar charts: room for the sample categories

# ── Overview plots of all other functions (battery, impedance, ToF-SIMS, ...) ──
# one place to change the size of every overview plot (Plotly and Matplotlib) and the legend
OVERVIEW_W_CM, OVERVIEW_H_CM = 8.0, 6.6
SHOW_LEGEND = True

# ── Fonts: declare in POINTS, converted to the px plotly writes ───
FONT_PT        = 11   # axis titles + body  -> Inkscape reads 11 pt
TICK_FONT_PT   = 11   # tick labels
ANNOT_FONT_PT  = 10   # annotation boxes (sample labels in the waterfall)
LEGEND_FONT_PT = 8    # side legend

# ── Fixed margins (px): room for ticks + titles. Fixed margins AND
#    automargin=False keep the rectangle identical across figures.
MARGIN     = dict(l=58, r=12, t=12, b=48)
BAR_MARGIN = dict(l=76, r=12, t=24, b=96)   # wider/deeper: long y title, rotated
                                            # category labels

# ── Colours ───────────────────────────────────────────────────────
my_color_scale = ["#b95b5b", "#daa24e", "#f6e7b1", "#a3d1d0", "#5c8b9d"]

# ── Side legend ───────────────────────────────────────────────────
LEGEND_STEP_PX  = 16     # vertical distance between two legend entries
LEGEND_SWATCH   = 16     # width of the colour swatch
LEGEND_PAD      = 5      # swatch -> text


def cm(x: float) -> float: return x * PX_PER_IN / 2.54


def pt(x: float) -> float: return x * PX_PER_IN / 72


def _uniform_tickformat(values):
    """Fixed-decimal tick format so every tick label on an axis shows the same
    number of decimal places (None keeps plotly's default integer ticks)."""
    vals = []
    for v in values:
        try:
            f = float(v)
        except (TypeError, ValueError):
            continue
        if np.isfinite(f):
            vals.append(f)
    if len(vals) < 2:
        return None
    span = max(vals) - min(vals)
    if span <= 0 or not np.isfinite(span):
        return None
    decimals = int(np.ceil(-np.log10(span / 4.0)))  # ~4-5 major ticks
    return f".{decimals}f" if decimals >= 1 else None


def color_series(n, scale=None, reverse=True, positions=None):
    '''n discrete colours sampled from `my_color_scale`.
    reverse=True -> first item is the blue end, last item the red end
    (same direction as DAY_COLORS in the ageing notebooks).
    positions=[...] samples the scale at those points instead of spreading it
    evenly - useful for 3 categories, where the even spread lands on the pale
    middle of the scale and gives a bar fill that is hard to see.'''
    scale = scale or my_color_scale
    if positions is not None:
        return px.colors.sample_colorscale(scale, list(positions))
    if n < 1:
        return []
    if n == 1:
        return px.colors.sample_colorscale(scale, [0.0 if reverse else 1.0])
    pos = [1.0 - i / (n - 1) for i in range(n)]
    if not reverse:
        pos = pos[::-1]
    return px.colors.sample_colorscale(scale, pos)


def to_rgba(color, alpha):
    '''Hex or rgb() colour -> rgba() string with alpha (used for the peak fills).'''
    if color.startswith('#'):
        r, g, b = pcol.hex_to_rgb(color)
    else:
        r, g, b = [float(v) for v in color[color.index('(') + 1:color.index(')')].split(',')[:3]]
    return f'rgba({r:.0f},{g:.0f},{b:.0f},{alpha})'


def legend_size(entries, plot_h_cm):
    '''(extra_right_px, extra_bottom_px) needed to host `entries` on the right.'''
    if not entries:
        return 0, 0
    longest = max(len(str(e[0])) for e in entries)
    width = int(LEGEND_SWATCH + LEGEND_PAD + 0.56 * pt(LEGEND_FONT_PT) * longest) + 14
    height = len(entries) * LEGEND_STEP_PX + 6
    return width, max(0, height - round(cm(plot_h_cm)))


def add_side_legend(fig: go.Figure, entries, plot_w_cm, plot_h_cm,
                    extra_right_px=0, x_gap_px=6):
    '''Draw a legend into the right margin. `entries` = [(label, color, kind)].'''
    if not entries:
        return fig
    w, h = round(cm(plot_w_cm)), round(cm(plot_h_cm))   # plot rectangle in px
    x0 = 1.0 + x_gap_px / w
    x1 = x0 + LEGEND_SWATCH / w
    for i, (label, color, kind) in enumerate(entries):
        y = 1.0 - (i * LEGEND_STEP_PX + LEGEND_STEP_PX / 2) / h
        if kind in ('fill', 'box'):
            fig.add_shape(type='rect', xref='paper', yref='paper', layer='above',
                          x0=x0, x1=x1, y0=y - 4 / h, y1=y + 4 / h,
                          fillcolor=color,
                          opacity=0.45 if kind == 'fill' else 1.0,
                          line=dict(color=color if kind == 'fill' else 'black',
                                    width=1 if kind == 'fill' else 0.6))
        elif kind == 'marker':
            fig.add_shape(type='circle', xref='paper', yref='paper', layer='above',
                          x0=(x0 + x1) / 2 - 3 / w, x1=(x0 + x1) / 2 + 3 / w,
                          y0=y - 3 / h, y1=y + 3 / h,
                          fillcolor='white', line=dict(color=color, width=1))
        else:   # 'line' / 'dash'
            fig.add_shape(type='line', xref='paper', yref='paper', layer='above',
                          x0=x0, x1=x1, y0=y, y1=y,
                          line=dict(color=color, width=1.5,
                                    dash='dot' if kind == 'dash' else 'solid'))
        fig.add_annotation(xref='paper', yref='paper',
                           x=x1 + LEGEND_PAD / w, y=y, text=str(label),
                           xanchor='left', yanchor='middle', showarrow=False,
                           font=dict(family='Arial', size=pt(LEGEND_FONT_PT),
                                     color='black'))
    return fig


def save_fig(fig: go.Figure, stem: str, show: bool = True, html: bool = True, output_dir=None) -> None:
    """Saves a figure as <stem>.svg and <stem>.png (3x scale), optionally <stem>.html, into output_dir (a pathlib.Path) and shows it.
    Errors of the export (e.g. kaleido) are printed instead of stopping the notebook."""
    formats = [("svg", {}), ("png", {"scale": 3})]
    for ext, kw in formats:
        try:
            fig.write_image(str(output_dir / f"{stem}.{ext}"), **kw)
        except Exception as e:
            print(f"  Could not save .{ext}: {e}")
    if html:
        try:
            fig.write_html(str(output_dir / f"{stem}.html"))
        except Exception as e:
            print(f"  Could not save .html: {e}")
    print(f"Saved {stem}")
    if show:
        fig.show()


def add_reference_lines(fig, lines, color='grey'):
    '''Dashed vertical lines at known binding energies. `lines` = [(binding_energy, label)].
    The labels stand rotated above the plot rectangle (the canvas grows, the rectangle
    keeps its size) and are pushed apart when two lines are closer than one label.
    Lines outside the plotted x range are skipped, so they cannot stretch the axis.
    Call it after the figure got its style (plot_waterfall, plot_spectrum_with_components
    in scientific_utils/xps/plotting.py).'''
    x_vals = [np.asarray(tr.x, dtype=float) for tr in fig.data if getattr(tr, 'x', None) is not None]
    if not lines or not x_vals:
        return fig
    x_vals = np.concatenate(x_vals)
    lo, hi = np.nanmin(x_vals), np.nanmax(x_vals)
    reverse = fig.layout.xaxis.autorange == 'reversed'
    # left to right as drawn (XPS: high binding energy on the left)
    lines = sorted([(x, l) for x, l in lines if lo <= x <= hi], reverse=reverse)
    if not lines:
        return fig

    # position of every line in px from the left edge of the rectangle
    m = fig.layout.margin
    plot_w_px = fig.layout.width - m.l - m.r
    pos = [((hi - x) if reverse else (x - lo)) / (hi - lo) * plot_w_px for x, _ in lines]
    label_px = pt(LEGEND_FONT_PT) + 2    # thickness of one rotated label
    shifted = []
    for p in pos:
        if shifted and p - shifted[-1] < label_px:
            p = shifted[-1] + label_px
        shifted.append(p)

    # room above the rectangle for the longest label (html tags like <sub> do not count)
    longest = max(len(re.sub(r'<[^>]+>', '', str(l))) for _, l in lines)
    extra_top = int(0.56 * pt(LEGEND_FONT_PT) * longest) + 8
    fig.update_layout(margin_t=m.t + extra_top, height=fig.layout.height + extra_top)

    for (x, label), p, s in zip(lines, pos, shifted):
        fig.add_vline(x=x, layer='below', line=dict(color=color, width=1, dash='dash'))
        fig.add_annotation(x=x, xref='x', y=1.0, yref='paper', yshift=3, xshift=s - p,
                           text=label, textangle=-90, xanchor='center', yanchor='bottom',
                           showarrow=False,
                           font=dict(size=pt(LEGEND_FONT_PT), color=color))
    return fig


def style_bars(fig, x_label='', y_label='', entries=(), *, barmode='stack',
               tickangle=-45, y_tickformat='~s', y_range=None,
               plot_w_cm=BAR_W_CM, plot_h_cm=BAR_H_CM, sample_order=None):
    """Publication style for bar charts: black bar outlines, BAR_MARGIN, category x axis (rotated labels, order sample_order),
    side legend from entries [(label, colour, kind)], optional y range. Returns the figure."""
    fig.update_traces(marker_line_color='black', marker_line_width=0.6)
    fig.update_layout(barmode=barmode, bargap=0.3, bargroupgap=0.08)

    entries = list(entries)
    right, bottom = legend_size(entries, plot_h_cm)
    apply_style(fig, x_label, y_label,
                plot_w_cm=plot_w_cm, plot_h_cm=plot_h_cm, margin=BAR_MARGIN,
                x_ticks='', x_minor=False, x_tickformat=None,     # category axis
                y_tickformat=y_tickformat,
                extra_right_px=right, extra_bottom_px=bottom)
    add_side_legend(fig, entries, plot_w_cm, plot_h_cm)
    fig.update_xaxes(tickangle=tickangle, categoryorder='array',
                     categoryarray=sample_order)
    if y_range is not None:
        fig.update_yaxes(range=y_range)
    return fig


def apply_style(fig: go.Figure, x_label: str = "", y_label: str = "", *,
                plot_w_cm=PLOT_W_CM, plot_h_cm=PLOT_H_CM, margin=None,
                x_ticklabels=True, y_ticklabels=True,
                x_tickformat="~s", y_tickformat="~s",
                x_ticks='inside', y_ticks='inside',
                x_minor=True, y_minor=True,
                extra_right_px=0, extra_bottom_px=0, showlegend=False) -> go.Figure:
    '''The one and only layout function.

    The keyword arguments only exist for the two cases where the default is
    physically wrong:
      * category axes (bar charts) have no meaningful minor ticks / SI format
      * intensity axes in a.u. carry no tick labels
    `extra_right_px` / `extra_bottom_px` enlarge the CANVAS for the side legend
    without touching the plot rectangle itself.
    x_tickformat / y_tickformat = 'uniform' -> same number of decimals on every tick (_uniform_tickformat).
    showlegend=True -> plotly legend right of the plot area (overview plots), False -> add_side_legend is used.
    '''
    # Collect the plotted values so both axes can get a uniform decimal tick format
    if x_tickformat == 'uniform' or y_tickformat == 'uniform':
        x_vals, y_vals = [], []
        for tr in fig.data:
            if getattr(tr, "x", None) is not None:
                x_vals.extend(np.ravel(tr.x))
            if getattr(tr, "y", None) is not None:
                y_vals.extend(np.ravel(tr.y))
        if x_tickformat == 'uniform':
            x_tickformat = _uniform_tickformat(x_vals)
        if y_tickformat == 'uniform':
            y_tickformat = _uniform_tickformat(y_vals)
    if showlegend:
        # plotly legend right of the plot area: the canvas grows, the plot area keeps its size
        entries = [(tr.name, None, 'line') for tr in fig.data if tr.name and tr.showlegend is not False]
        legend_right_px, legend_bottom_px = legend_size(entries, plot_h_cm)
        extra_right_px += legend_right_px + 30          # + 30: plotly draws longer swatches than add_side_legend
        extra_bottom_px += legend_bottom_px
    m = dict(margin or MARGIN)
    m['r'] += extra_right_px
    m['b'] += extra_bottom_px
    m['autoexpand'] = False    # otherwise a legend/label would steal space
                               # from the rectangle and break the fixed size
    plot_w_px, plot_h_px = round(cm(plot_w_cm)), round(cm(plot_h_cm))
    minor_on = dict(ticks='inside', ticklen=3, tickwidth=1)

    fig.update_layout(
        width=plot_w_px + m['l'] + m['r'],
        height=plot_h_px + m['t'] + m['b'],
        margin=m,                            # fixed -> plot rectangle is constant
        font=dict(family='Arial', size=pt(FONT_PT), color='black'),
        legend_title_text=None,
        title=None,
        showlegend=showlegend,               # False: legends are drawn by add_side_legend
        legend=dict(x=1.02, y=1.0, xanchor='left', yanchor='top',     # right of the plot area (room: extra_right_px)
                    bgcolor='rgba(255,255,255,0)', font=dict(size=pt(LEGEND_FONT_PT))),
        xaxis=dict(
            title=x_label,
            ticklen=5, tickwidth=2, showticklabels=x_ticklabels,
            ticks=x_ticks, mirror=True,
            showgrid=False, gridcolor='lightgrey', gridwidth=0.5,
            showline=True, linewidth=2, linecolor='black',
            minor=minor_on if x_minor else dict(ticks=''),
            title_font=dict(size=pt(FONT_PT)),
            tickfont=dict(size=pt(TICK_FONT_PT)),
            automargin=False,                # keep margins exact -> equal rects
            tickformat=x_tickformat,
        ),
        yaxis=dict(
            title=y_label,
            ticklen=5, tickwidth=2, ticks=y_ticks,
            showticklabels=y_ticklabels, mirror=True,
            showgrid=False, gridcolor='lightgrey', gridwidth=0.5,
            showline=True, linewidth=2, linecolor='black',
            minor=minor_on if y_minor else dict(ticks=''),
            title_font=dict(size=pt(FONT_PT)),
            tickfont=dict(size=pt(TICK_FONT_PT)),
            automargin=False,
            tickformat=y_tickformat,
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    return fig


def apply_style_simple(fig, x_label="", y_label="", width_px=655, height_px=374):
    """Older, smaller version of apply_style: Arial 11 px, inside ticks, mirrored axes, fixed size in px (width_px x height_px). Returns the figure."""
    fig.update_layout(
        width=width_px,
        height=height_px,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family='Arial', size=11, color='black'),
        legend_title_text=None,
        title=None,
        xaxis=dict(
            title=x_label,
            ticklen=5, tickwidth=2, showticklabels=True,
            ticks='inside', mirror=True,
            showgrid=False, gridcolor='lightgrey', gridwidth=0.5,
            showline=True, linewidth=2, linecolor='black',
            title_font=dict(size=11)
        ),
        yaxis=dict(
            title=y_label,
            ticklen=5, tickwidth=2, ticks='inside',
            showticklabels=True, mirror=True,
            showgrid=False, gridcolor='lightgrey', gridwidth=0.5,
            showline=True, linewidth=2, linecolor='black',
            title_font=dict(size=11)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig
