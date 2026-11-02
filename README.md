# Scientific data analysis with Python

Python code from my Master's thesis and my PhD in battery materials research (NCM cathode materials).
It reads, processes and plots data from the measurement methods I used:

- **Battery testing**: cycling and rate tests (Maccor and Biologic cyclers), dQ/dV analysis
- **Impedance spectroscopy**: equivalent circuit models and fitting
- **ToF-SIMS**: depth profiles, ion images, peak lists, PCA of surface spectra
- **XPS** and **XRD**: spectra, depth profiles, peak areas, atomic percentages, Gauss fits

The code was written between 2020 and 2026. The notebooks import them from there, the code runs with current library versions and the comments are in English.

## Contents

| Folder | What it does |
|---|---|
| `scientific_utils/` | The package with the functions the notebooks use (124, almost all with a short docstring), sorted by topic, see below |
| `battery-cycling/` | Cycling and rate test pipelines (01 → 06/07; the readers for Maccor and Biologic files are in `scientific_utils.battery.io`), merging all results of one battery into one table (`data-handling`) |
| `impedance/` | Simulation and fitting of equivalent circuits (RC, RQ, CPE), plots of measured impedance spectra |
| `tof-sims/` | Depth profiles, diffusion fit of depth profiles, ion images, peak list alignment, PCA of surface spectra |
| `xps/` | XPS spectra, depth profiles, peak areas and atomic percentages (also as spider web plot), publication style plots |
| `xrd/` | Plot of XRD diffractograms, peak areas after a baseline correction, Gauss fit of a double peak |
| `signal-analysis/` | Autocorrelation of OCV measurements |
| `archive/` | Functions that are not used by any notebook (76) and exact copies of other functions; kept instead of deleted (see `archive/README.md`) |

### The package `scientific_utils`

Every topic has the same structure: `io.py` (reading files), `analysis.py` (calculations) and `plotting.py` (plots).

```
scientific_utils/
├── general/      file handling (file selection and start row of a table, shared by all readers), normalising, plot helpers and the plot style
├── battery/      cycler files, charge/discharge steps, capacities, potential drops, dQ/dV peaks
├── impedance/    circuit models, residual functions for fitting, Nyquist plots
├── tof_sims/     IONTOF SurfaceLab exports, mass list alignment, depth profile plots
├── xps/          CasaXPS exports, detail spectra, publication style spectra (waterfall, fitted components), peak areas, spider web plot
├── xrd/          diffractograms, baseline correction, peak areas, Gauss fits
├── statistics/   autocorrelation, residuals, FFT spectra, histograms, Q-Q plots, dendrograms
├── fitting/      diffusion models
├── lab/          lab calculations (masses for synthesis, sheet casting, AES samples, washing solutions)
└── publication_plotly.py    Plotly figures for publications (fixed size in cm, fonts in pt)
```

Example:

```python
from scientific_utils.tof_sims.io import Read_SurfaceLab_DepthProfil_Combined_Header
from scientific_utils.general.analysis import Normalize_Column_To_Reference_Column
```

## Plot style

All plots use one style: a plot area of 8.0 × 6.6 cm, Arial 11 pt, ticks inside on all four sides with minor ticks,
and the colours of `my_color_scale` (`#b95b5b`, `#daa24e`, `#f6e7b1`, `#a3d1d0`, `#5c8b9d`).

- **Size and legend** are set in one place, `scientific_utils/publication_plotly.py`: `OVERVIEW_W_CM`, `OVERVIEW_H_CM`, `SHOW_LEGEND`.
- **Plotly** plots get the style from `apply_style()` in the same file (the legend is placed right of the plot area).
- **Matplotlib** plots get it from `pgf_with_latex` in `scientific_utils/general/plotting.py`, which is applied as soon as
  the module is imported (colours of the curves: blue, red, gold, teal, then the same colours darker).
- Exceptions on purpose: Nyquist plots and PCA score plots keep the same scale on both axes (the plot area can be smaller),
  the loading plot of the surface spectra PCA is three times as wide (about 100 fragment names), and the 3D plot keeps its own size.

## Getting started

```bash
git clone https://github.com/SteffenSchr/scientific-data-analysis-python.git
cd scientific-data-analysis-python
pip install -e ".[notebooks]"
jupyter lab
```

The code was tested with Python 3.13, NumPy 2.4, pandas 3.0, Matplotlib 3.10, SciPy 1.17 and scikit-learn 1.8.

## Data

Every analysis folder has a `data/` folder:

- `data/raw/` the measurement files (exports of the instruments)
- `data/processed/` intermediate results (`.pkl`) that are written by one notebook and read by the next one

The battery data (one test cell, `Batt15`) is in `battery-cycling/data/Batt15/` and is used by the cycling,
rate test and data handling notebooks.

Please note:

- The **pipelines must run in order** (`01`, `02`, `03`, ...), because every step reads the results of the step before.
  The `processed/` folders of the battery (`battery-cycling/data/Batt15/processed/`) and impedance
  (`impedance/plotting/data/processed/`) pipelines already contain the results, so every notebook can also be opened
  and run on its own. Running a pipeline again from `01` overwrites these files with the same results.
- The parsers (`01_parse_...`) read the files in `data/raw/`. If this folder is empty, they save empty lists.
- Results that depend on interpolation can differ slightly from the original results of 2020: NumPy 1.25 changed
  the order in which equal values are sorted, which changes the equidistant resampling of curves with repeated
  voltage values. For the cycling data this changes the dQ/dV peaks by up to 8 % (discharge) and 0.7 % (charge).
  Capacities, potential drops and impedance results are identical.

## Credits

Some parts of this repository are based on the work of others:

- **`Matplotlib_Dendrogram`** (`scientific_utils/statistics/plotting.py`) is taken from the scikit-learn example
  [Plot Hierarchical Clustering Dendrogram](https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html).
- **`Baseline_arPLS`** (`scientific_utils/xrd/analysis.py`) is taken from
  [this StackOverflow answer](https://stackoverflow.com/questions/29156532/python-baseline-correction-library), an implementation of
  the arPLS method by Baek et al., [Analyst 140 (2015) 250](https://pubs.rsc.org/en/content/articlehtml/2015/an/c4an01061b).
- **`radar_factory`** (`scientific_utils/xps/plotting.py`) is taken from the Matplotlib example
  [Radar chart](https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html).

## License

MIT, see [LICENSE](LICENSE).
