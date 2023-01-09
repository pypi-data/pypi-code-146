from typing import Optional, Union, Tuple

import os

import numpy as np
import pandas as pd

from more_itertools import intersperse

import holoviews as hv
from bokeh.layouts import gridplot
from bokeh.plotting import show, output_file, save
from bokeh.plotting.figure import Figure
from bokeh.models import BoxZoomTool, WheelZoomTool, PanTool, ResetTool, CrosshairTool
# from bokeh.models import ColumnDataSource, HoverTool

import chromedriver_binary
from bokeh.io import export_png

import panel as pn

from html2image import Html2Image

hv.extension("bokeh")


class RubixHeatmap:
    """
    Class creating a RubixHeatmap object for plotting rather complex heatmaps with metadata.

    Three input files (CSV) or pandas DataFrames (in any combination) are expected:

    - Main data (clusterized by applying, for example, NMTF to raw data).
      Example of rows: biomarkers at different timepoints.
      Example of columns: patients.

    - Metadata for rows. Example: column 1 = timepoint, column 2 = biomarker.

    - Metadata for columns. Example: row 1 = score (Y/N), row 2 = treatment (several options), row 3 = cluster no.

    The resulting plot is composed of the following elements, all rendered using holoviews.HeatMap().
    Their disposition generally looks like :

    ### [CA] ###

    [RA] [MP] [RL]

    ### [CL] ###

    - MP : main plot (with colorbar on the right)
    - RA : row annotations (from metadata for rows)
    - CA : column annotations (from metadata for columns) : can be duplicated under the main plot for long DFs
    - RL : row legend (RA explained) : optional
    - CL : column legend (CA explained) : optional
    - ### : white space filler

    plot() method will save one of the following, or both :
        - HTML plot : if `save_html` evaluates to True, or in any case if `save_png` evaluates to False
        - PNG image corresponding to the HTML plot (without toolbar) : if `save_png` evaluates to True

    With `plot_save_path` specified, HTML and PNG are saved according to it,
    otherwise, HTML only is saved in current working directory to be able to show the plot.

    Parameters
    ----------

    data: Optional[pd.DataFrame]
        File with main data
    metadata_rows: Optional[pd.DataFrame]
        Fle with metadata for row annotations
    metadata_cols: Optional[pd.DataFrame]
        File with metadata for column annotations
    data_path: Optional[str]
        Path to a folder with data and metadata
    data_file: Optional[str]
        Name of the file with main data
    metadata_rows_file: Optional[str]
        Name of the file with metadata for row annotations
    metadata_cols_file: Optional[str]
        Name of the file with metadata for column annotations
    plot_save_path: Optional[str]
        Path to an HTML file for saving the plot. If none is provided, HTML is saved in current working directory
        under the name <your_python_script_name>.html and automatically opened in a web browser.

    save_html: Union[bool, int, str]
        If equal to True / string starting with "T" or "t", e.g. "True" / "1" or 1, save HTML plot
        (if save_png is False, will always save HTML)
    save_png: Union[bool, int, str]
        If equal to True / string starting with "T" or "t", e.g. "True" / "1" or 1,
        save a PNG screenshot of HTML plot
    png_tool: str
        // "native" (default) = with Bokeh's export_png() (requires Selenium + ChromeDriver installed, takes more time)
        // "hti" = with html2image library (only requires a Chromium-based browser on the machine,
        but leaves transparent background and crops PNG to screen size, thus unreliable for large plots)

    color_scaling_quantile: Union[int, float]
        Quantile for capping and scaling the data to get rid of outliers (read more about it in the README)
    scale_along: Union[int, str, None]
        // 0 or "columns" = per columns : x => x / max(column)
        // 1 or "rows" = per rows : x => x / max(row)
        // None (default, and also any other value except for 0 or 1) = do not scale
    normalize_along: Union[int, str, None]
        // 0 or "columns" = per columns : x => (x - median(column)) / MAD(column)
        // 1 or "rows" = per rows : x => (x - median(row)) / MAD(row)
        // None (default, and also any other value except for 0 or 1) = do not normalize

    colorbar_title: str
        Title of the colorbar for main heatmap
    colorbar_height: Optional[int]
        Height of the colorbar (default = 1/3 of main heatmap height)
    colorbar_location: str
        Location of the colorbar: "top", "center" or "bottom" (default), always to the right of the heatmap
    show_colorbar: bool
        Whether to show the colorbar for main heatmap

    show_metadata_rows: bool
        Whether to plot row annotations (default True)
    show_metadata_rows_labels: bool
        Whether to show row annotations' labels along vertical axis (default False)
    show_metadata_cols: bool
        Whether to plot column annotations (default True)
    duplicate_metadata_cols: Optional[bool]
        Whether to duplicate column annotations under the main heatmap.
        If None, will be set automatically to True for dataframes longer that 70 rows.
    show_rows_legend: bool
        Whether to plot the legend for row annotations (default True)
    rows_legend_onecol: bool
        // True (default) = plot row annotations in one column, analogously to column annotations (WIP)
        // False = plot row annotations in multiple columns (WIP)
    show_cols_legend: bool
        Whether to plot the legend for column annotations (default True)

    colormap_main: str
        Main colormap name, must be known by holoviews (default "coolwarm" / "YlOrRd" for non-negative data).
        Ref. 1 https://holoviews.org/user_guide/Colormaps.html#perceptually-uniform-sequential-colormaps
        Ref. 2 https://holoviews.org/user_guide/Colormaps.html#diverging-colormaps
    nan_color: str
        Hex color string "#xxxxxx" or named HTML color for filling NaN values in the main heatmap (default "black")
    sep_color: str
        Hex color string "#xxxxxx" or named HTML color for filling separators in the main heatmap (default "white")
    colormap_metarows: str
        Colormap for row annotations, must be known by holoviews (default "Glasbey").
        Ref. https://holoviews.org/user_guide/Colormaps.html#categorical-colormaps
    colormap_metacols: str
        Colormap for column annotations, must be known by holoviews (default "Category20").
        Ref. https://holoviews.org/user_guide/Colormaps.html#categorical-colormaps

    axes_labels_style: str
        Style of row annotations and column annotations names (default "bold", can be "italic")
    legend_axes_labels_style: str
        Style of legends names (default "italic", can be "bold")
    data_columns_label: str
        Label to use for main data columns (normally not shown on the plot)
    metadata_label: str
        Label to use for metadata (default "Metadata")

    pixel_size: str
        Size of the colorbar "pixel", in screen pixels (default 6)
    heatmap_width: Union[int, str, None]
        Fixed main plot width in screen pixels (ignores `pixel_size` specified)
        // int = in screen pixels
        // "proportional" = proportional to fixed main plot height
    heatmap_height: Union[int, str, None]
        Fixed main plot height in screen pixels (ignores `pixel_size` specified)
        // int = in screen pixels
        // "proportional" = proportional to fixed main plot width

    mrcol_for_legend: Optional[str]
        Column of metadata for row annotations to be explained in the legend.
        If not specified, the rightmost column is explained.
    proper_labels_for_metadata_cols_legend: Optional[dict]
        Dict of correspondence between metadata_cols rows' names and names we'd like to show in the legend
        (enables to use shorter names for better display)
    row_labels_for_highlighting: Optional[list]
        Keywords for identifying row labels to be highlighted i.e. specified on the plot (optional)
    index_label: Optional[str]
        Name of a column in main data DF to set as rows index (optional)
    columns_label: Optional[str]
        Name of a row in main data DF to set as columns index (optional)

    data_rows_to_drop: Optional[list]
        Names of rows in main data not intended to be plotted (optional). Nonexistent names will be skipped.
    data_cols_to_drop: Optional[list]
        Names of columns in main data not intended to be plotted (optional). Nonexistent names will be skipped.
    metadata_rows_sep: Optional[str]
        Insert row separators in the main DF and the metadata-rows DF before plotting,
        according to the specified column (between groups of labels with identical values).
        A separator is a row or a group of rows (depending on the DF length and heatmap height)
        filled with either minimum value for non-normalized data, or median value for normalized one.
    metadata_cols_sep: Optional[str]
        Insert column separators in the main DF and the metadata-cols DF before plotting,
        according to the specified rows (between groups of labels with identical values).
        A separator is a column or a group of columns (depending on the DF length and heatmap height)
        filled with either minimum value for non-normalized data, or median value for normalized one.
    sep_value: str
        // None (default) = separators will be plotted in `sep_color` (default "white")
        // "min" = with mininum value of the DF (color will depend on the colormap)
        // "median" = with median value of the DF (color will depend on the colormap)
        // "adapt" = with mininum value of the DF if data normalisation is not called, median value if called
    """

    def __init__(
            self,
            data: Optional[pd.DataFrame] = None,
            metadata_rows: Optional[pd.DataFrame] = None,
            metadata_cols: Optional[pd.DataFrame] = None,
            data_path: Optional[str] = None,
            data_file: Optional[str] = None,
            metadata_rows_file: Optional[str] = None,
            metadata_cols_file: Optional[str] = None,
            plot_save_path: Optional[str] = None,
            save_html: Union[bool, int, str] = True,
            save_png: Union[bool, int, str] = False,
            png_tool: str = "native",
            color_scaling_quantile: Union[int, float] = 95,
            scale_along: Union[int, str, None] = None,
            normalize_along: Union[int, str, None] = None,
            colorbar_title: str = "",
            colorbar_height: Optional[int] = None,
            colorbar_location: str = "bottom",
            show_colorbar: bool = True,
            show_metadata_rows: bool = True,
            show_metadata_rows_labels: bool = False,
            show_metadata_cols: bool = True,
            duplicate_metadata_cols: Optional[bool] = None,
            show_rows_legend: bool = True,
            rows_legend_onecol: bool = True,
            show_cols_legend: bool = True,
            colormap_main: str = "coolwarm",
            nan_color: str = "black",
            sep_color: str = "white",
            colormap_metarows: str = "glasbey",
            colormap_metacols: str = "Category20",
            axes_labels_style: str = "bold",
            legend_axes_labels_style: str = "italic",
            data_columns_label: str = "subjects",
            metadata_label: str = "Metadata",
            pixel_size: str = 6,
            heatmap_width: Union[int, str, None] = None,
            heatmap_height: Union[int, str, None] = None,
            mrcol_for_legend: Optional[str] = None,
            proper_labels_for_metadata_cols_legend: Optional[dict] = None,
            row_labels_for_highlighting: Optional[list] = None,
            index_label: Optional[str] = None,
            columns_label: Optional[str] = None,
            data_rows_to_drop: Optional[list] = None,
            data_cols_to_drop: Optional[list] = None,
            metadata_rows_sep: Optional[str] = None,
            metadata_cols_sep: Optional[str] = None,
            sep_value: Optional[str] = None
    ) -> None:

        # Auxiliary
        self.df_titles = ["Data", "Metadata rows", "Metadata cols"]
        self.uniform_colormaps = [
            "blues",
            "kb", "kbc", "kg", "kgy", "kr",
            "bmw", "bmy", "bgy", "bgyw",
            "fire", "inferno", "magma", "plasma",
            "gray", "dimgray",
            "cividis", "viridis"
        ]
        self.sequential_colormaps = [
            "Greens", "YlGn", "YlGnBu", "PuBuGn", "PuBu", "Purples", "BuPu",
            "Oranges", "OrRd", "Reds", "YlOrRd",
            "Greys"
        ]

        self.relevant_tools = [
            BoxZoomTool(),
            WheelZoomTool(),
            PanTool(),
            ResetTool()
        ]
        self.relevant_tools_with_crosshair = self.relevant_tools + [CrosshairTool()]
        # self.relevant_tools_with_crosshair_horiz = self.relevant_tools + [CrosshairTool(dimensions="width")]
        # self.relevant_tools_with_crosshair_vert = self.relevant_tools + [CrosshairTool(dimensions="height")]
        # self.relevant_tools_plus = self.relevant_tools + [HoverTool(tooltips=[('index', '$index')])]

        """ SET """

        # Set directly provided dataframes
        self.data = data
        self.metadata_rows = metadata_rows
        self.metadata_cols = metadata_cols

        # Set data path and files
        self.data_path = data_path
        self.data_file = data_file
        self.metadata_rows_file = metadata_rows_file
        self.metadata_cols_file = metadata_cols_file
        self.plot_save_path = plot_save_path

        self.save_png = False
        if (
                isinstance(save_png, bool) and save_png
                or isinstance(save_png, str) and save_png.lower()[0] == "t"
                or isinstance(save_png, str) and save_png == "1"
                or isinstance(save_png, int) and save_png == 1
        ):
            self.save_png = True
        self.png_tool = png_tool

        if self.save_png:
            self.save_html = False
            if (
                    isinstance(save_html, bool) and save_html
                    or isinstance(save_html, str) and save_html.lower()[0] == "t"
                    or isinstance(save_html, str) and save_html == "1"
                    or isinstance(save_html, int) and save_html == 1
            ):
                self.save_html = True
        else:
            self.save_html = True

        # Set data scaling and normalization
        self.color_scaling_quantile = color_scaling_quantile

        if scale_along in (0, "columns", "cols"):
            self.scale_along = 0
        elif scale_along == (1, "rows"):
            self.scale_along = 1
        else:
            self.scale_along = None

        if normalize_along in (0, "columns", "cols"):
            self.normalize_along = 0
        elif normalize_along == (1, "rows"):
            self.normalize_along = 1
        else:
            self.normalize_along = None

        if (
                (self.scale_along == 0 and self.normalize_along == 0)
                or (self.scale_along == 1 and self.normalize_along == 1)
        ):
            raise ValueError("You cannot apply both `scale_along` and `normalize_along` to the same axis!")

        # Set view options
        self.show_metadata_rows = show_metadata_rows
        self.show_metadata_rows_labels = show_metadata_rows_labels
        self.show_metadata_cols = show_metadata_cols
        self.duplicate_metadata_cols = duplicate_metadata_cols
        self.show_rows_legend = show_rows_legend
        self.rows_legend_onecol = rows_legend_onecol
        self.show_cols_legend = show_cols_legend

        # Set colormap parameters
        self.colorbar_title = colorbar_title
        self.colorbar_height = colorbar_height
        self.colorbar_location = colorbar_location
        self.show_colorbar = show_colorbar
        self.colormap_main = colormap_main
        self.nan_color = nan_color
        self.sep_color = sep_color
        self.sep_value = sep_value
        self.colormap_metarows = colormap_metarows
        self.colormap_metacols = colormap_metacols

        # Set plot parameters
        self.axes_labels_style = axes_labels_style
        self.legend_axes_labels_style = legend_axes_labels_style
        self.data_columns_label = data_columns_label
        self.metadata_label = metadata_label
        self.pixel_size = pixel_size
        self.heatmap_width = heatmap_width
        self.heatmap_height = heatmap_height
        self.mrcol_for_legend = mrcol_for_legend
        self.proper_labels_for_metadata_cols_legend = proper_labels_for_metadata_cols_legend
        self.row_labels_for_highlighting = row_labels_for_highlighting

        # Set dataprep parameters
        self.index_label = index_label
        self.columns_label = columns_label
        self.data_rows_to_drop = data_rows_to_drop
        self.data_cols_to_drop = data_cols_to_drop
        self.metadata_rows_sep = metadata_rows_sep
        self.metadata_cols_sep = metadata_cols_sep

        # Set labels for axes
        self.dummy_label = "."  # label for plotting purposes but not intended to be shown on the plot
        self.z_axis_label = "value"  # label for heatmaps' color axes (not shown on the plot)

        # Set plot dimensions
        self.meta_bar_width = 12 * self.pixel_size
        self.legend_bar_width = 5 * self.pixel_size

        """ READ """

        # Read data & metadata
        self.data = self.read_data(self.data, self.data_file, 1)
        self.metadata_rows = self.read_data(self.metadata_rows, self.metadata_rows_file, 2)
        self.metadata_cols = self.read_data(self.metadata_cols, self.metadata_cols_file, 3).T

        """ DATAPREP """

        # Set proper indexes
        if self.index_label or self.columns_label:
            self.set_proper_indexes()

        # Drop data not intended to be plotted + force convert to float
        if self.data_rows_to_drop or self.data_cols_to_drop:
            self.drop_rows_or_cols()

        # Align data with metadata
        self.align_data()

        # Scale and/or normalize data, if required
        if self.scale_along is not None:
            self.scale_data()

        if self.normalize_along is not None:
            self.normalize_data()

        # Determine proper separator value
        if self.sep_value == "adapt":
            if self.normalize_along is not None:
                self.sep_value = self.data.median().median()
            else:
                if self.data.min().min() >= 0:
                    self.sep_value = self.data.min().min()
                else:
                    self.sep_value = self.data.median().median()

        elif self.sep_value == "min":
            self.sep_value = self.data.min().min()

        elif self.sep_value == "median":
            self.sep_value = self.data.median().median()

        elif self.sep_value is None:
            self.sep_value = np.inf

        else:
            raise ValueError(f"Wrong `sep_value`: {self.sep_value}. Expected : 'nan', 'main', 'median' or 'adapt'")

        # Insert separators into data, if required
        if self.metadata_rows_sep is not None or self.metadata_cols_sep is not None:
            self.split_data()

        if self.duplicate_metadata_cols is None:
            if len(self.data) <= 70:
                self.duplicate_metadata_cols = False
            else:
                self.duplicate_metadata_cols = True

        # Change colormap for a perceptually uniform one, if all the data are non-negative
        if (
                self.data.min().min() >= 0
                and self.colormap_main not in self.uniform_colormaps
                and self.colormap_main not in self.sequential_colormaps
        ):
            self.colormap_main = "YlOrRd"

        # Row & column annotations: convert categorical values into integer codes
        if self.rows_legend_onecol:
            self.metadata_rows_codes, self.corr_legend_rows_onecol = self.convert_metadata_rows_onecol()
        else:
            self.metadata_rows_codes, self.corr_legend_rows = self.convert_metadata_rows()
        self.metadata_cols_codes, self.corr_legend_cols = self.convert_metadata_cols()

        # Pick important rows to be highlighted at the plot
        self.rows_to_highlight = self.find_rows_to_highlight()

        # Main data : replace categorical index labels with their locations numbers
        # (to be compatible with `yticks` option of holoviews)
        if self.rows_to_highlight:
            self.data_relabeled = self.data.set_index(pd.Index([i for i in range(0, len(self.data))]))
        else:
            self.data_relabeled = self.data

        # Transform DFs to be plotted to take into account separators, if required
        def replace_index_duplicates_with_dots(df: pd.DataFrame, axis: int = 0):
            """
            When repeated values are found in index, starting from the second occurence,
            they are replaced with ".", "..", "..." etc.
            """
            if axis == 1:
                df = df.T

            df = df.reset_index()
            dfgbc = df.groupby(["index"]).cumcount()
            df["gbc"] = dfgbc.map({i: i * "." for i in range(0, dfgbc.max() + 1)})
            df["index"] = df["index"].mask(df["gbc"] != "", df["gbc"])
            df = df.drop("gbc", axis=1).set_index("index")

            if axis == 1:
                df = df.T
            return df

        if self.metadata_rows_sep:
            self.metadata_rows_codes = replace_index_duplicates_with_dots(self.metadata_rows_codes)
            self.data_relabeled = replace_index_duplicates_with_dots(self.data_relabeled)

        if self.metadata_cols_sep:
            self.metadata_cols_codes = replace_index_duplicates_with_dots(self.metadata_cols_codes, axis=1)
            self.data_relabeled = replace_index_duplicates_with_dots(self.data_relabeled, axis=1)

        print("RubixHeatmap object instantiation : SUCCESS")

    def read_data(
            self,
            df: Optional[pd.DataFrame] = None,
            file: Optional[str] = None,
            num: int = 0
    ) -> pd.DataFrame:
        """
        Read data or metadata from a CSV file, if no DF is provided directly.
        Also, force convert DF labels to str, to make sure they are treated as categorical by Bokeh.

        Parameters
        ----------
        df: Optional[pd.DataFrame]
            DataFrame of data or metadata
        file: Optional[str]
            File with data or metadata
        num: int
            Auxiliary numerical ID

        Returns
        -------
        pd.DataFrame
        """

        # No DF is provided
        if df is None:

            if self.data_path is None:
                raise FileNotFoundError("Data path is not set!")

            if file is None:
                raise FileNotFoundError(f"{self.df_titles[num]} file name is not set!")
            else:

                if not file.endswith(".csv"):
                    raise TypeError(f"File '{file}' is expected to be a CSV file")

                try:
                    df = pd.read_csv(f"{self.data_path}{file}", header=0, index_col=0)
                except FileNotFoundError:
                    raise FileNotFoundError(f"File '{file}' not found!")
                except UnicodeDecodeError:
                    raise TypeError(f"File '{file}' does not contain valid CSV!")

        # DF is directly provided
        else:
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"{self.df_titles[num]}: you have to provide a valid DataFrame!")

        # Convert relevant labels to str
        df = df.rename(
            index={label: str(label).strip() for label in df.index},
            columns={label: str(label).strip() for label in df.columns}
        )
        return df

    def set_proper_indexes(self) -> None:
        """
        If the input DataFrames are not properly indexed yet,
        main data column and/or main data row with specified names are used to set indexes.
        """
        if self.index_label:
            self.data = self.data.set_index(self.index_label)
            self.metadata_rows = self.metadata_rows.set_index(self.index_label)

        if self.columns_label:
            self.data = self.data.T.set_index(self.columns_label).T
            self.metadata_cols = self.metadata_cols.T.set_index(self.columns_label).T

    def drop_rows_or_cols(self) -> None:
        """
        Drop rows and/or columns not intended to be plotted.
        Also convert data values to float, in case they might have been read as str.
        """
        if self.data_rows_to_drop:
            data_rows_to_drop = pd.Index(self.data_rows_to_drop).intersection(self.data.index).to_list()
            if data_rows_to_drop:
                self.data = self.data.drop(data_rows_to_drop, axis=0)
            else:
                print("WARNING : Main data don't contain any rows among the specified ones intended for dropping")

        if self.data_cols_to_drop:
            data_cols_to_drop = pd.Index(self.data_cols_to_drop).intersection(self.data.columns).to_list()
            if data_cols_to_drop:
                self.data = self.data.drop(data_cols_to_drop, axis=1)
            else:
                print("WARNING : Main data don't contain any columns among the specified ones intended for dropping")

        self.data = self.data.astype(float)

    def align_data(self) -> None:
        """
        Align data with metadata
        """
        common_index = self.data.index.intersection(self.metadata_rows.index)
        common_columns = self.data.columns.intersection(self.metadata_cols.columns)

        self.data = self.data.reindex(index=common_index)
        self.metadata_rows = self.metadata_rows.reindex(index=common_index)

        self.data = self.data.reindex(columns=common_columns)
        self.metadata_cols = self.metadata_cols.reindex(columns=common_columns)

        if len(self.data) == 0 or len(self.data.columns) == 0:
            raise IndexError("Main data and metadata have no rows or no columns in common! Please check your data.")

    def scale_data(self) -> None:
        """
        Scale main data along columns (scale_along = 0) or rows (scale_along = 1)
        """
        quant = self.color_scaling_quantile

        if quant < 80 or quant > 100:
            raise ValueError(f"Wrong quantile value: {quant}. Please use percentage from 80 to 100")

        def cap_scale(x):
            quantile = np.percentile(x, quant)
            x = x.apply(lambda x: quantile if x > quantile else x)
            x /= quantile
            return x

        self.data = self.data.apply(cap_scale, axis=self.scale_along)

    def normalize_data(self) -> None:
        """
        Normalize main data along columns (normalize_along = 0) or rows (normalize_along = 1)
        """
        quant = self.color_scaling_quantile

        if quant < 80 or quant > 100:
            raise ValueError(f"Wrong quantile value: {quant}. Please use percentage from 80 to 100")

        def cap_scale(x):
            quant_high = 50 + quant / 2
            quant_low = 50 - quant / 2
            quantile_high = np.percentile(x, quant_high)
            quantile_low = np.percentile(x, quant_low)
            x = x.apply(lambda x: quantile_high if x > quantile_high else (quantile_low if x < quantile_low else x))
            x /= quantile_high
            return x

        def center_reduce(x):
            median = np.median(x)
            dev = x - median
            median_abs_dev = np.median(abs(dev))
            x = dev / median_abs_dev
            x = x.apply(lambda x: 1 if x > 1 else (-1 if x < -1 else x))
            return x

        self.data = self.data.apply(cap_scale, axis=self.normalize_along)
        self.data = self.data.apply(center_reduce, axis=self.normalize_along).fillna(0.0)

    def split_data(self):
        """
        Insert row and/or column separators in the main DF and the corresponding metadata DF before plotting,
        according to the specified column or row (between groups of labels with identical values).
        A separator is a row or column or a group of these (depending on the DF size and heatmap size)
        filled with either minimum value for non-normalized data, or median value for normalized one.
        """

        main_width, main_height = self.get_plot_size()

        def split_df(
                df: pd.DataFrame,
                label: Union[str, int],
                axis: int,
                sep_value: Union[float, str] = np.nan
        ) -> pd.DataFrame:
            """
            Split one DataFrame along the specified axis, according to the provided label.
            """

            if axis == 1:
                df = df.T
                plot_size_factor = main_width / 1400
            elif axis == 0:
                plot_size_factor = main_height / 1000
            else:
                raise ValueError(f"Wrong 'axis' value: {axis}. Expected: 0 or 1")

            mult = round(len(df) / 100)
            mult = round(mult / plot_size_factor)
            if mult < 1:
                mult = 1

            gb = df.groupby(by=label, axis=0, sort=False)
            df_split = [gb.get_group(i) for i in gb.groups]

            sep = pd.DataFrame(index=[""] * mult, columns=df.columns, data=[[sep_value] * len(df.columns)] * mult)

            df_split_with_seps = pd.concat(list(intersperse(sep, df_split)), axis=0)
            if axis == 1:
                df_split_with_seps = df_split_with_seps.T

            return df_split_with_seps

        # Split along rows
        if self.metadata_rows_sep is not None:

            data = pd.concat([self.metadata_rows, self.data], axis=1)

            self.metadata_rows = split_df(
                df=self.metadata_rows,
                label=self.metadata_rows_sep,
                axis=0
            )
            self.data = split_df(
                df=data,
                label=self.metadata_rows_sep,
                axis=0,
                sep_value="#sep#"
            )
            self.data = self.data.drop(columns=self.metadata_rows.columns)

        # Split along columns
        if self.metadata_cols_sep is not None:

            data = pd.concat([self.metadata_cols, self.data], axis=0)

            self.metadata_cols = split_df(
                df=self.metadata_cols,
                label=self.metadata_cols_sep,
                axis=1
            )
            self.data = split_df(
                df=data,
                label=self.metadata_cols_sep,
                axis=1,
                sep_value="#sep#"
            )
            self.data = self.data.drop(index=self.metadata_cols.index)

        # Fill separators with proper value
        self.data = self.data.replace("#sep#", self.sep_value)

    def find_rows_to_highlight(self) -> list:
        """
        Pick important rows to be highlighted at the plot
        """
        rows_to_highlight = []
        if self.row_labels_for_highlighting:
            for col in self.metadata_rows.columns:
                rows_to_highlight += self.metadata_rows.loc[
                    self.metadata_rows[col].isin(self.row_labels_for_highlighting)
                ].index.to_list()
        rows_to_highlight = self.metadata_rows[self.metadata_rows.index.isin(rows_to_highlight)].index.to_list()

        if self.row_labels_for_highlighting and not rows_to_highlight:
            print(
                "WARNING : No rows in main data could have been identified as containing the labels "
                "specified for highlighting.\nIt may be useful to check the arguments passed to RubixHeatmap."
            )

        return rows_to_highlight

    def convert_metadata_rows(self, stretch_codes: bool = False) -> Tuple[pd.DataFrame, dict]:
        """
        Row annotations : convert categorical values in index to integer codes (for plotting purposes).
        Rows legend : prepare value-code correspondence DFs.

        Parameters
        ----------
        stretch_codes: bool
            Whether to align codes in inner columns with max code value in the outer (rightmost) column
        """
        metadata_rows_tmp = self.metadata_rows.copy(deep=True)
        metadata_rows_codes = self.metadata_rows.copy(deep=True)

        metadata_rows_no_sep = self.metadata_rows.copy(deep=True)
        metadata_rows_no_sep = metadata_rows_no_sep[~metadata_rows_no_sep.index.duplicated(keep=False)]

        # Substitute categorical values to numerical codes (row numbers)
        for col in self.metadata_rows.columns:
            mapper = {
                label: pd.Index(metadata_rows_no_sep[col].unique()).get_loc(label)
                for label in metadata_rows_no_sep[col]
            }
            mapper[np.nan] = np.nan
            metadata_rows_codes[col] = metadata_rows_no_sep[col].map(mapper)

        if stretch_codes:
            max_outer = metadata_rows_codes.iloc[:, -1].max()
            for col_number in range(2, len(metadata_rows_codes.columns) + 1):
                max_inner = metadata_rows_codes.iloc[:, -col_number].max()
                mapper = {
                    i: i * int(max_outer / max_inner)
                    for i in metadata_rows_codes.iloc[:, -col_number].to_list()
                }
                metadata_rows_codes.iloc[:, -col_number] = metadata_rows_codes.iloc[:, -col_number].map(mapper)

        # Prepare value-code correspondence DFs
        corr_legend_rows = {}
        for mrcol in self.metadata_rows.columns:

            metadata_rows_tmp[f"{mrcol}_code"] = metadata_rows_codes[mrcol]
            corr_legend_rows[mrcol] = metadata_rows_tmp[[mrcol, f"{mrcol}_code"]].drop_duplicates().set_index(mrcol)

            corr_legend_rows[mrcol] = corr_legend_rows[mrcol][~corr_legend_rows[mrcol].index.duplicated()]
            corr_legend_rows[mrcol] = corr_legend_rows[mrcol][corr_legend_rows[mrcol].index.notnull()]

            def remove_dot_zero(txt: str) -> str:
                if txt.endswith(".0"):
                    txt = txt.replace(".0", "")
                return txt
            corr_legend_rows[mrcol].index = corr_legend_rows[mrcol].index.map(str).map(remove_dot_zero)

        # TODO (afedorov) : make multicol rows legend display correct colors

        return metadata_rows_codes, corr_legend_rows

    def convert_metadata_rows_onecol(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        ONE-COLUMN VERSION.
        Row annotations : convert categorical values in index to integer codes (for plotting purposes).
        Rows legend : prepare value-code correspondence DFs.
        """
        metadata_rows_tmp = self.metadata_rows.copy(deep=True)
        metadata_rows_codes = self.metadata_rows.copy(deep=True)

        metadata_rows_no_sep = self.metadata_rows.copy(deep=True)
        metadata_rows_no_sep = metadata_rows_no_sep[~metadata_rows_no_sep.index.duplicated(keep=False)]

        # Calculate the increment between columns for spreading metadata cols' values along the same colormap.
        # This may be less reasonable compared to metadata rows.
        max_len_unique = 0
        for col in metadata_rows_codes.columns:
            max_len_unique = max(max_len_unique, len(self.metadata_rows[col].unique()))
        base = 5
        incr = base * round(max_len_unique / base)

        # Spreading metadata rows' values along the same colormap
        i = 0
        for col in metadata_rows_codes.columns:
            mapper = {
                label: pd.Index(metadata_rows_no_sep[col].unique()).get_loc(label) + i * incr
                for label in metadata_rows_no_sep[col]
            }
            metadata_rows_codes[col] = metadata_rows_no_sep[col].map(mapper)
            i += 1

        metadata_rows_codes = metadata_rows_codes.reindex(index=self.metadata_rows.index)

        # Prepare value-code correspondence DF
        dum_list = []
        for i in range(len(self.metadata_rows.columns) + 1):
            dum = pd.DataFrame(columns=["code"], index=["." * (i + 1)], data=np.nan)
            dum_list.append(dum)

        corr_list = []
        for col in metadata_rows_codes.columns:
            metadata_rows_tmp[f"{col}_code"] = metadata_rows_codes[col]
            corr = metadata_rows_tmp.loc[:, [col, f"{col}_code"]].T.drop_duplicates().T.set_index(col)
            corr.rename(columns={f"{col}_code": "code"}, inplace=True)
            if np.nan in corr.index:
                try:
                    corr = corr.drop([np.nan], axis=0)
                except KeyError:
                    pass

            corr_list.append(corr)
            corr_list.append(dum_list[metadata_rows_codes.columns.get_loc(col)])

        del corr_list[-1]
        corr_legend_rows = pd.concat(corr_list, axis=0)

        corr_legend_rows = corr_legend_rows[~corr_legend_rows.index.duplicated()]
        corr_legend_rows = corr_legend_rows[corr_legend_rows.index.notnull()]

        def remove_dot_zero(txt: str) -> str:
            if txt.endswith(".0"):
                txt = txt.replace(".0", "")
            return txt
        corr_legend_rows.index = corr_legend_rows.index.map(str).map(remove_dot_zero)

        return metadata_rows_codes, corr_legend_rows

    def convert_metadata_cols(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Column annotations : convert categorical values in index to integer codes (for plotting purposes).
        Columns legend : prepare value-code correspondence DF.
        """
        metadata_cols_tmp = self.metadata_cols.copy(deep=True)
        metadata_cols_codes = self.metadata_cols.copy(deep=True)

        metadata_cols_no_sep = self.metadata_cols.copy(deep=True)
        metadata_cols_no_sep = metadata_cols_no_sep.T[~metadata_cols_no_sep.T.index.duplicated(keep=False)].T

        # Calculate the increment between rows for spreading metadata rows' values along the same colormap.
        # This is reasonable as normally each row of metadata for columns would not contain many unique values
        # (typically less than 5...10), otherwise visually the plot would not be instantly clear.
        max_len_unique = 0
        for row in metadata_cols_codes.index:
            max_len_unique = max(max_len_unique, len(self.metadata_cols.loc[row].unique()))
        base = 5
        incr = base * round(max_len_unique / base)

        # Spreading metadata cols' values along the same colormap
        i = 0
        for row in metadata_cols_codes.index:
            mapper = {
                label: pd.Index(metadata_cols_no_sep.loc[row].unique()).get_loc(label) + i * incr
                for label in metadata_cols_no_sep.loc[row]
            }
            metadata_cols_codes.loc[row] = metadata_cols_no_sep.loc[row].map(mapper)
            i += 1

        # Prepare value-code correspondence DF
        dum_list = []
        for i in range(len(self.metadata_cols) + 1):
            dum = pd.DataFrame(index=["code"], columns=["." * (i + 1)], data=np.nan)
            dum_list.append(dum)

        corr_list = []
        for row in metadata_cols_codes.index:

            metadata_cols_tmp.loc[f"{row}_code"] = metadata_cols_codes.loc[row]
            corr = metadata_cols_tmp.loc[[row, f"{row}_code"]].T.drop_duplicates().set_index(row).T
            corr.rename(index={f"{row}_code": "code"}, inplace=True)
            if np.nan in corr.columns:
                try:
                    corr = corr.drop([np.nan], axis=1)
                except KeyError:
                    pass

            if self.proper_labels_for_metadata_cols_legend:
                corr.rename(
                    columns={
                        val: f"{self.proper_labels_for_metadata_cols_legend[row]}{val}"
                        for val in corr.columns
                        if val != np.nan
                    },
                    inplace=True
                )

            corr_list.append(corr)
            corr_list.append(dum_list[metadata_cols_codes.index.get_loc(row)])

        del corr_list[-1]
        corr_legend_cols = pd.concat(corr_list, axis=1)

        corr_legend_cols = corr_legend_cols.T[~corr_legend_cols.T.index.duplicated()].T
        corr_legend_cols = corr_legend_cols.T[corr_legend_cols.T.index.notnull()].T

        def remove_dot_zero(txt: str) -> str:
            if txt.endswith(".0"):
                txt = txt.replace(".0", "")
            return txt
        corr_legend_cols.columns = corr_legend_cols.columns.map(str).map(remove_dot_zero)

        return metadata_cols_codes, corr_legend_cols

    def get_plot_size(self) -> Tuple[int, int]:
        """
        Get main heatmap size in pixels depending on the specified parameters
        """

        # Main heatmap dimensions by default
        main_height = self.pixel_size * len(self.data)
        main_width = self.pixel_size * len(self.data.columns)

        # Check for specified dimensions validity
        if self.heatmap_width and self.heatmap_height:
            if not (
                    (
                            isinstance(self.heatmap_width, int)
                            and (self.heatmap_height == "proportional" or isinstance(self.heatmap_height, int))
                    )
                    or (
                            isinstance(self.heatmap_height, int)
                            and (self.heatmap_width == "proportional" or isinstance(self.heatmap_width, int))
                    )
            ):
                raise ValueError(
                    f"ERROR : invalid combination of `heatmap_width` and `heatmap_height`. "
                    f"Both should be int, or one int and the other 'proportional'."
                )

        # Custom main heatmap width
        if self.heatmap_width and isinstance(self.heatmap_width, int):
            main_width = self.heatmap_width

        # Custom main heatmap height
        if self.heatmap_height and isinstance(self.heatmap_height, int):
            main_height = self.heatmap_height

        # Proportional main heatmap width
        if self.heatmap_width and self.heatmap_width == "proportional":
            main_width = int(main_height * len(self.data.columns) / len(self.data))
        elif self.heatmap_width and not isinstance(self.heatmap_width, int):
            print(
                f"WARNING : invalid `heatmap_width` value ('{self.heatmap_width}'). "
                f"Expected : int or 'proportional'. Default value (multiple of pixel size) will be used."
            )

        # Proportional main heatmap height
        if self.heatmap_height and self.heatmap_height == "proportional":
            main_height = int(main_width * len(self.data) / len(self.data.columns))
        elif self.heatmap_height and not isinstance(self.heatmap_height, int):
            print(
                f"WARNING : invalid `heatmap_height` value ('{self.heatmap_height}'). "
                f"Expected : int or 'proportional'. Default value (multiple of pixel size) will be used."
            )

        return main_width, main_height

    def plot(self) -> None:
        """
        Draw and show the heatmap + the additional elements:
        row annotations, column annotations, rows legend, columns legend
        """

        metarows_fig = None
        metacols_fig = None
        legend_cols_fig = None

        main_width, main_height = self.get_plot_size()

        # Create main data heatmap
        hm_fig = self.plot_main_heatmap(main_width, main_height)
        hm_fig.tools = self.relevant_tools_with_crosshair

        # Create the heatmap of the metadata for rows
        if self.show_metadata_rows:
            metarows_fig = self.plot_metadata_rows(main_height)
            metarows_fig.tools = self.relevant_tools
            # Linking zoom between main heatmap and metadata for rows only works if there is no rows to highlight
            if not self.rows_to_highlight:
                metarows_fig.y_range = hm_fig.y_range

        # Create the heatmap of the metadata for columns
        if self.show_metadata_cols:
            metacols_fig = self.plot_metadata_cols(main_width)
            metacols_fig.tools = self.relevant_tools
            metacols_fig.x_range = hm_fig.x_range

        # Create the heatmap of rows legend
        legend_rows_figs = []
        if self.show_rows_legend:
            if self.rows_legend_onecol:
                legend_rows_fig = self.plot_rows_legend(main_height)
                legend_rows_fig.tools = self.relevant_tools
                legend_rows_figs = [legend_rows_fig]
            else:
                for i in range(1, len(self.metadata_rows.columns) + 1):
                    legend_rows_fig = self.plot_rows_legend(main_height, i)
                    legend_rows_fig.tools = self.relevant_tools
                    legend_rows_figs.append(legend_rows_fig)

        # Create the heatmap of columns legend
        if self.show_cols_legend:
            legend_cols_fig = self.plot_cols_legend(main_width)
            legend_cols_fig.tools = self.relevant_tools

        # Compose the complete plot
        plot_level_one = [None, metacols_fig] + [None] * len(legend_rows_figs)
        plot_level_two = [metarows_fig, hm_fig] + legend_rows_figs
        plot_level_four = [None, legend_cols_fig] + [None] * len(legend_rows_figs)

        # For long dataframes, duplicate columns annotations below main heatmap
        if not self.duplicate_metadata_cols:
            plot_children = [
                plot_level_one,
                plot_level_two,
                plot_level_four
            ]
        else:
            metacols_fig_double = self.plot_metadata_cols(main_width, invert_yaxis=True)
            metacols_fig_double.tools = self.relevant_tools
            metacols_fig_double.x_range = hm_fig.x_range
            plot_level_three = [None, metacols_fig_double] + [None] * len(legend_rows_figs)
            plot_children = [
                plot_level_one,
                plot_level_two,
                plot_level_three,
                plot_level_four
            ]

        fig = gridplot(children=plot_children, sizing_mode="stretch_both", toolbar_location="left")

        # Show or save the plot
        if self.plot_save_path is None:
            show(fig)
            print("RubixHeatmap plot shown : SUCCESS")

        else:
            if not self.plot_save_path.endswith(".html"):
                raise ValueError(f"Save path must end with '.html', but you provided: {self.plot_save_path}")

            if '/' in self.plot_save_path:
                sep = '/'
            elif '\\' in self.plot_save_path:
                sep = '\\'
            else:
                raise ValueError(
                    f"Seems like you are trying to save your plot in root directory: {self.plot_save_path}\n"
                    "Please set a meaningful save path."
                )
            dir_for_saving = sep.join(self.plot_save_path.split(sep)[:-1])
            file_name = self.plot_save_path.split(sep)[-1].split('.')[0]
            os.makedirs(dir_for_saving, exist_ok=True)

            # Save HTML
            if self.save_html:
                output_file(self.plot_save_path)
                save(fig)
                print(f"RubixHeatmap plot saved to {self.plot_save_path} : SUCCESS")

            # Save PNG (requires Chrome browser installed on your machine)
            if self.save_png:
                png_path = f"{dir_for_saving}{sep}{file_name}.png"

                # Temporary HTML plot without toolbar
                tmp_fig = gridplot(children=plot_children, sizing_mode="stretch_both", toolbar_location=None)

                # With Html2image : DEPRECATED
                if self.png_tool == "hti":

                    # Some magic to avoid Bokeh error while saving two plots in one script
                    pn.io.model.remove_root(fig)

                    tmp_path = self.plot_save_path.replace(".html", "_tmp.html")
                    output_file(tmp_path)
                    save(tmp_fig)

                    hti = Html2Image(output_path=dir_for_saving)
                    hti.screenshot(
                        html_file=tmp_path,
                        save_as=f"{file_name}.png"
                    )
                    os.unlink(tmp_path)
                    print(f"RubixHeatmap plot saved to {png_path} with html2image : SUCCESS")

                # Natively : PREFERRED and by default
                elif self.png_tool == "native":
                    print(f"ChromeDriver initialized at {chromedriver_binary.chromedriver_filename} : SUCCESS")

                    print(f"Saving RubixHeatmap plot to {png_path} natively... ", end="")
                    export_png(tmp_fig, filename=png_path)
                    print(f"SUCCESS")

                else:
                    raise ValueError(
                        f"Wrong `png_tool` value: '{self.png_tool}'. Expected: 'hti' or 'native'"
                    )

    def plot_main_heatmap(self, main_width: int, main_height: int) -> Figure:
        """
        Plot main data heatmap

        Parameters
        ----------
        main_width: int
            Width of main heatmap in screen pixels
        main_height: int
            Height of main heatmap in screen pixels
        """

        # Colorbar options
        if self.colorbar_height:
            colorbar_height = self.colorbar_height
        else:
            colorbar_height = int(main_height / 4)

        colorbar_opts = {
            "height": colorbar_height,
            "location": self.colorbar_location,
            "bar_line_color": None,
            "major_tick_line_color": "white",
            "title": self.colorbar_title
        }

        hm = hv.HeatMap(
            {
                self.data_columns_label: self.data_relabeled.columns,
                self.dummy_label: self.data_relabeled.index,
                self.z_axis_label: self.data_relabeled
            },
            [self.data_columns_label, self.dummy_label], self.z_axis_label
        )

        hm.opts(
            cmap=self.colormap_main,
            colorbar=self.show_colorbar,
            colorbar_opts=colorbar_opts,
            frame_width=main_width,
            frame_height=main_height,
            xaxis=None,
            invert_yaxis=True,
            clipping_colors={"NaN": self.nan_color, "max": self.sep_color}
        )

        # Highlight specified rows, or not if nothing to highlight
        if self.rows_to_highlight:
            hm.opts(
                yaxis="right",
                yticks=[(self.data.index.get_loc(label), label) for label in self.rows_to_highlight]
            )
        else:
            hm.opts(yaxis=None)

        fig = hv.render(hm)
        fig.outline_line_color = None
        fig.yaxis.axis_line_color = None
        fig.yaxis.axis_label_text_color = "white"
        fig.yaxis.major_label_text_font_style = "italic"
        fig.yaxis.major_label_text_color = "red"

        return fig

    def plot_metadata_rows(self, main_height: int) -> Figure:
        """
        Plot metadata for rows

        Parameters
        ----------
        main_height: int
            Height of main heatmap in screen pixels
        """

        metarows = hv.HeatMap(
            {
                self.metadata_label: self.metadata_rows_codes.columns,
                self.dummy_label: self.metadata_rows_codes.index,
                self.z_axis_label: self.metadata_rows_codes
            },
            [self.metadata_label, self.dummy_label], self.z_axis_label
        )

        metarows.opts(
            cmap=self.colormap_metarows,
            frame_width=self.meta_bar_width,
            frame_height=main_height,
            invert_xaxis=True,
            invert_yaxis=True,
            yaxis="right"
        )

        if not self.show_metadata_rows_labels:
            metarows.opts(yaxis=None)

        fig = hv.render(metarows)
        fig.outline_line_color = None
        fig.xaxis.axis_label_text_font_style = self.axes_labels_style
        fig.xaxis.axis_line_color = None

        if self.show_metadata_rows_labels:

            # Adapt font size for metadata rows index following DF length and heatmap height
            metarows_index_font_size = int(
                main_height * (1137 - 4 * len(self.data)) / 89_000
            )
            if metarows_index_font_size < 5:
                metarows_index_font_size = 5
            if metarows_index_font_size > 10:
                metarows_index_font_size = 10
            fig.yaxis.major_label_text_font_size = f"{metarows_index_font_size}pt"

            fig.yaxis.axis_label_text_color = None
            fig.yaxis.axis_line_color = None
            fig.yaxis.axis_line_color = None
            fig.yaxis.major_tick_out = 0
            fig.yaxis.major_tick_line_color = None
            fig.yaxis.minor_tick_line_color = None

        return fig

    def plot_metadata_cols(self, main_width: int, invert_yaxis: bool = False) -> Figure:
        """
        Plot metadata for columns

        Parameters
        ----------
        main_width: int
            Width of main heatmap in screen pixels
        invert_yaxis: bool
            Set the order of rows in column annotations for plotting
        """

        metacols = hv.HeatMap(
            {
                self.data_columns_label: self.metadata_cols_codes.columns,
                self.metadata_label: self.metadata_cols_codes.index,
                self.z_axis_label: self.metadata_cols_codes
            },
            [self.data_columns_label, self.metadata_label], self.z_axis_label
        )

        metacols.opts(
            cmap=self.colormap_metacols,
            frame_width=main_width,
            frame_height=self.meta_bar_width,
            xaxis=None,
            yaxis="right"
        )

        if invert_yaxis:
            metacols.opts(invert_yaxis=True)

        fig = hv.render(metacols)
        fig.outline_line_color = None
        fig.yaxis.axis_label_text_font_style = self.axes_labels_style
        fig.yaxis.axis_line_color = None

        return fig

    def plot_rows_legend(self, main_height: int, col_num: int = 1) -> Figure:
        """
        Plot the legend of the metadata for rows

        Parameters
        ----------
        main_height: int
            Height of main heatmap in screen pixels
        col_num: int
            Number of a column in the metadata for rows, starting from the right
        """

        # Plot in one column
        if self.rows_legend_onecol:

            # Specific column of metadata_rows for the legend name (optional)
            if self.mrcol_for_legend:
                mrcol = self.mrcol_for_legend
                visible_label = f"{mrcol}s"
            else:
                visible_label = f"{self.metadata_label} legend"

            legend_rows = hv.HeatMap(
                {
                    self.dummy_label: self.corr_legend_rows_onecol.columns,
                    visible_label: self.corr_legend_rows_onecol.index,
                    self.z_axis_label: self.corr_legend_rows_onecol
                },
                [self.dummy_label, visible_label], self.z_axis_label
            )

        # Plot in multicolumns (WIP! colors are not correct for some columns)
        else:
            mrcol = self.metadata_rows.columns.to_list()[-col_num]
            visible_label = f"{mrcol}s"

            legend_rows = hv.HeatMap(
                {
                    visible_label: self.corr_legend_rows[mrcol].columns,
                    self.dummy_label: self.corr_legend_rows[mrcol].index,
                    self.z_axis_label: self.corr_legend_rows[mrcol]
                },
                [visible_label, self.dummy_label], self.z_axis_label
            )

        legend_rows.opts(
            cmap=self.colormap_metarows,
            frame_width=self.legend_bar_width,
            frame_height=main_height,
            yaxis="right",
            invert_yaxis=True
        )

        fig = hv.render(legend_rows)
        fig.outline_line_color = None

        fig.xaxis.axis_label_text_font_style = self.legend_axes_labels_style
        fig.xaxis.axis_line_color = None
        fig.xaxis.major_tick_out = 0
        fig.xaxis.major_tick_line_color = None
        fig.xaxis.major_label_text_color = None

        if self.rows_legend_onecol:
            fig.xaxis.axis_label_text_color = None
            fig.xaxis.axis_line_color = None
        else:
            fig.yaxis.axis_label_text_color = None
            fig.yaxis.axis_line_color = None

        # Adapt font size for rows legend index following DF length and heatmap height
        if self.rows_legend_onecol:
            len_data = len(self.corr_legend_rows_onecol["code"].unique())
        else:
            len_data = len(self.corr_legend_rows[mrcol].iloc[:, 0].unique())

        rows_legend_index_font_size = int(
            main_height * (1137 - 4 * len_data) / 89_000
        )
        if rows_legend_index_font_size < 5:
            rows_legend_index_font_size = 5
        if rows_legend_index_font_size > 10:
            rows_legend_index_font_size = 10

        fig.yaxis.major_label_text_font_size = f"{rows_legend_index_font_size}pt"

        fig.yaxis.axis_line_color = None
        fig.yaxis.major_tick_out = 0
        fig.yaxis.major_tick_line_color = None
        fig.yaxis.minor_tick_line_color = None

        return fig

    def plot_cols_legend(self, main_width: int) -> Figure:
        """
        Plot the legend of the metadata for columns

        Parameters
        ----------
        main_width: int
            Width of main heatmap in screen pixels
        """

        visible_label = f"{self.metadata_label} legend"
        legend_cols = hv.HeatMap(
            {
                visible_label: self.corr_legend_cols.columns,
                self.dummy_label: self.corr_legend_cols.index,
                self.z_axis_label: self.corr_legend_cols
            },
            [visible_label, self.dummy_label], self.z_axis_label
        )

        legend_cols.opts(
            cmap=self.colormap_metacols,
            frame_width=main_width,
            frame_height=self.legend_bar_width,
            yaxis=None
        )

        fig = hv.render(legend_cols)
        fig.outline_line_color = None
        fig.xaxis.axis_label_text_font_style = self.legend_axes_labels_style
        fig.xaxis.axis_line_color = None
        fig.xaxis.major_tick_out = 0
        fig.xaxis.major_tick_line_color = None

        return fig
