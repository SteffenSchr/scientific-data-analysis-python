# archive

Code that is kept here instead of being deleted, so nothing is lost. Nothing in the repository imports from this folder.

## Functions that no notebook uses

These 76 functions were written for analyses that are not part of this repository (or were replaced later).
No notebook and no other function calls them, so they were moved out of `scientific_utils`.
Each file has the same imports as the module it came from.

| File | Moved from | Functions |
|---|---|---|
| `battery_analysis.py` | `scientific_utils/battery/analysis.py` | `Extract_OCV_And_Charging_Discharging_Steps`, `Extract_ConstantCurrent_And_ConstantPotential_Steps`, `Calculate_CRate_From_Measured_Current`, `Calculate_Mean_Ratio_And_Save`, `Calculate_Ratio_Over_Multiple_Columns` |
| `battery_io.py` | `scientific_utils/battery/io.py` | `Rename_Biologic_Columns_To_Maccor_Names`, `Reset_Capacity_To_Zero`, `Synchronize_OCV_With_Cycling_Data`, `Read_Maccor_Txt_Files_And_Filenames` |
| `battery_plotting.py` | `scientific_utils/battery/plotting.py` | `Matplotlib_EC_Plot`, `Matplotlib_EC_Plot_Multiple_Dataframes`, `Plotly_EC_Plot_Multiple_Dataframes`, `Plotly_EC_Plot_Multiple_Columns`, `Plotly_EC_Plot_List_Of_Lists`, `Matplotlib_Ratio_Curves_Sorted_By_Values` |
| `general_analysis.py` | `scientific_utils/general/analysis.py` | `Extract_Dataframes_By_Index_From_List_Of_Lists`, `Scale_To_Max`, `Scale_To_MinMax`, `Resample_XY_Data`, `Derive_XY_Data`, `Smooth_XY_Data`, `Determine_Area`, `Remove_Outliers_MAD`, `Remove_Local_Outliers`, `Offset_Dataframes`, `Offset_Dataframes_Without_Normalization`, `Offset_Dataframes_Automatic`, `Offset_Dataframes_By_Range`, `Normalize_Dataframes_For_Overlay`, `Offset_One_Column_In_List_Of_Dataframes`, `Normalize_And_Offset_One_Column_In_List_Of_Dataframes`, `Delete_List_Entries`, `Extract_Range_Of_Column_Names`, `Find_Peaks_In_XY_Data` |
| `general_io.py` | `scientific_utils/general/io.py` | `Extract_FilePaths_Advanced`, `Log_Last_Used_Notebook`, `Read_PklFiles_Via_FilePath` |
| `general_plotting.py` | `scientific_utils/general/plotting.py` | `Create_ColorMap`, `Matplotlib_Simple_Plot`, `Plotly_Multiple_Dataframes` |
| `impedance_plotting.py` | `scientific_utils/impedance/plotting.py` | `BodePlotimpedance_model`, `Matplotlib_Bode_Plot_Phase_Angle` |
| `publication_plotter.py` | `scientific_utils/publication_plotter.py` | `set_publication_style`, `create_figure`, `save_plot`, `inspect_file`, `load_csv_data`, `apply_axis_style`, `apply_legend_style`, `plot_gradient_fill`, `add_inset_zoom`, `setup_broken_xaxis`, `plot_color_evolution` |
| `sps_io.py` | `scientific_utils/sps/io.py` | `Read_SPS_CSV_Files_And_Filenames` |
| `statistics_analysis.py` | `scientific_utils/statistics/analysis.py` | `Calculate_Fast_Fourier_Transform` |
| `statistics_plotting.py` | `scientific_utils/statistics/plotting.py` | `Matplotlib_QQ_Plot_Sampled`, `Statsmodels_QQ_Plot` |
| `tof_sims_analysis.py` | `scientific_utils/tof_sims/analysis.py` | `Transfer_Multiple_Dataframes_To_One_Dataframe`, `Transform_ColumnBased_To_RowBased_Dataframe` |
| `tof_sims_io.py` | `scientific_utils/tof_sims/io.py` | `Read_SurfaceLab_SputterProfil` |
| `tof_sims_plotting.py` | `scientific_utils/tof_sims/plotting.py` | `Matplotlib_Normalized_DepthProfil`, `Plotly_BoxPlot`, `Plotly_MassSpectrum` |
| `xps_analysis.py` | `scientific_utils/xps/analysis.py` | `Extract_XPS_DetailSpectra_From_Single_Scan`, `Determine_Area_XPS`, `Resample_XY_Data_With_Plot`, `Derive_XY_Data_With_Plot`, `Smooth_XY_Data_With_Plot`, `Determine_Area_Between_Two_Curves` |
| `xps_io.py` | `scientific_utils/xps/io.py` | `Read_XPS_Files` |
| `xps_plotting.py` | `scientific_utils/xps/plotting.py` | `Matplotlib_Interactive_XPS_Plot`, `Matplotlib_XPS_Spectra_Plot`, `Plotly_XPS_Surface_Spectra_Plot`, `Plotly_XPS_Multiple_Dataframes`, `Plotly_XPS_DepthProfil_Spectra_Plot` |
| `xrd_io.py` | `scientific_utils/xrd/io.py` | `Read_XRD_Diffractogram_With_Header` |

## Copies of other functions

| File | Copy of | Difference |
|---|---|---|
| `sps_plotting.py` (was `scientific_utils/sps/plotting.py`) | `battery_plotting.py:Matplotlib_EC_Plot` (was in `scientific_utils/battery/plotting.py`) | identical, only the function name `Matplotlib_SPS_Plot` differs |
| `tof_sims_io_Read_SurfaceLab_MassSpectrum.py` (was in `scientific_utils/tof_sims/io.py`) | `scientific_utils/tof_sims/io.py:Read_SurfaceLab_ColumnBased_AreaList` | the copy lacks the line that sets the last `Mass (u)` entry to `"0,00"` |
