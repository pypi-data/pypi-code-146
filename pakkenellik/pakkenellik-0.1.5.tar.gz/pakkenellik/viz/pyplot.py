# Helper functions for pyplot
# Found here: https://github.com/agude/Jupyter-Notebook-Template-Library/

from typing import Callable, Dict, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd

# We should be able to just set rcParams, expect Jupyter has a bug:
# https://github.com/jupyter/notebook/issues/3385
#
# So we have to call this function every time we want to plot.


def setup_plot(  # type: ignore[no-any-unimported]
    title: Optional[str] = "None",
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Set up a simple, single pane plot with custom configuration.

    Args:
        title (str, optional): The title of the plot.
        xlabel (str, optional): The xlabel of the plot.
        ylabel (str, optional): The ylabel of the plot.

    Returns:
        (fig, ax): A Matplotlib figure and axis object.

    """
    # Plot Size
    plt.rcParams["figure.figsize"] = (12, 7)  # (Width, height)

    # Text Size
    SMALL = 12
    MEDIUM = 16
    LARGE = 20
    HUGE = 28
    plt.rcParams["axes.titlesize"] = HUGE
    plt.rcParams["figure.titlesize"] = HUGE
    plt.rcParams["axes.labelsize"] = LARGE
    plt.rcParams["legend.fontsize"] = LARGE
    plt.rcParams["xtick.labelsize"] = MEDIUM
    plt.rcParams["ytick.labelsize"] = MEDIUM
    plt.rcParams["font.size"] = SMALL

    # Legend
    plt.rcParams["legend.frameon"] = True
    plt.rcParams["legend.framealpha"] = 1
    plt.rcParams["legend.facecolor"] = "white"
    plt.rcParams["legend.edgecolor"] = "black"

    # Figure output
    plt.rcParams["savefig.dpi"] = 300

    # Make the plol
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Make the title and label area opaque instead of transparent
    fig.patch.set_facecolor(ax.get_facecolor())

    return fig, ax


# https://stackoverflow.com/questions/19073683/matplotlib-overlapping-annotations-text


def draw_left_legend(  # type: ignore[no-any-unimported]
    ax: plt.Axes,
    nudges: Optional[Dict[str, Union[int, float]]] = None,
    fontsize: Optional[int] = 20,
) -> None:
    """Draw legend labels at the end of each line.

    Args:
        ax (matplotlib axis): The axis to draw on.
        nudges (Dict[str, float], default None): An optional mapping of line label
            to y adjustment for the label. Useful for preventing overlap. If a key
            is missing then that line is not adjusted.
        fontsize (int, default 20): A fontsize understood by matplotlib. Either an
            int or a size string.

    Returns: None

    """
    ax.get_legend().remove()
    for line in ax.lines:
        label: str = line.get_label()
        color = line.get_color()

        y = line.get_ydata()[-1]
        x = line.get_xdata()[-1]

        nudge_y: Union[int, float] = 0
        if nudges is not None:
            nudge_y = nudges.get(label, 0)

        ax.annotate(
            s=label,
            xy=(x, y),
            xytext=(10, 0 + nudge_y),
            textcoords="offset points",
            color=color,
            size=fontsize,
            weight="bold",
            va="center",
        )


def plot_time_series(  # type: ignore[no-any-unimported]
    df: pd.DataFrame,
    ax: plt.Axes,
    date_col: str,
    category_col: str,
    resample_frequency: Optional[str] = None,
    aggfunc: Union[str, Callable] = "size",
    linewidth: Optional[int] = 3,
) -> None:
    """Draws a timeseries for each distinct item in the category column

    Args:
        df (Pandas DataFrame): The dataframe of data, containing `date_col` and
            `category_col`.
        ax (matplotlib axis): The axis to draw on.
        date_col (str): The name of the column containing datetime objects.
            Converted to a DatetimeIndex with `pandas.to_datetime()`.
        category_col (str): The name of the column containing the categorical
            variable to plot. Will draw one time series per value.
        resample_frequency (str, default None): A frequency string understood
            by `pandas.DataFrame.resample`. If not provided uses the natural
            frequency of the data.
        aggfunc (string or function, default 'size'): Any object understood by
            `pandas.pivot_table(aggfunc=...)`, used to aggregate rows in time.
        linewidth (int, default 3): Width of the lines to draw.

    Returns: None

    """

    # Save label because it will be over-writen by Pandas
    xlabel = ax.get_xlabel()

    tmp_df = df.set_index(date_col)
    tmp_df.index = pd.to_datetime(tmp_df.index)
    pivot = tmp_df.pivot_table(
        index=tmp_df.index,
        columns=category_col,
        aggfunc=aggfunc,
        fill_value=0,
    )

    if resample_frequency is not None:
        pivot = pivot.resample(resample_frequency).sum()

    pivot.plot(ax=ax, linewidth=linewidth)

    # Restore the label
    ax.set_xlabel(xlabel)


def draw_colored_legend(ax: plt.Axes) -> None:  # type: ignore[no-any-unimported]
    """Draw a legend for the plot with the text colored to match the points.

    Args:
        ax (matplotlib axis): The axis to draw on.

    """
    # Draw a legend where there is no space around the line/point so
    # that the text is in the right place when we turn off the line/point.
    legend = ax.legend(handlelength=0, handletextpad=0)

    handles = legend.legendHandles
    texts = legend.get_texts()
    for handle, text in zip(handles, texts):
        # Change the color of the text to match the line or points
        try:
            # Points and some other objects have this
            color = handle.get_facecolor()[0]
        except AttributeError:
            # Lines have this
            color = handle.get_color()

        text.set_color(color)

        # Turn off the point
        handle.set_visible(False)


def draw_bands(  # type: ignore[no-any-unimported]
    ax: plt.Axes, color: Optional[plt.Color] = "0.95", alpha: Optional[float] = 1.0
) -> None:
    """Add grey bands between x-axis ticks.

    Args:
        ax (matplotlib axis): The axis to draw on.
        color (matplotlib color, default "0.95"): An object that
            matplotlib understands as a color, used to set the
            color of the bands.
        alpha (float, default 1.0): A float that controls the
            transparency of the bands. 1 is opague and 0 is
            completely transparent.

    """
    ticks = ax.get_xticks(minor=False)
    x_min, x_max = ax.get_xlim()

    lefts = []
    rights = []
    # There is a more elegant way to do this, but it assumes there is always a
    # tick outside the plot range on the left and right. It seems to be true,
    # but I don't think it is guarnteed.
    for left, right in zip(ticks[:-1], ticks[1:]):
        # Sometimes the ticks are outside the plot, so keep going until we
        # find one inside the plot. Then end when we find a ticket off the
        # right side.
        if left < x_min:
            continue
        elif x_max < left:
            break
        # The tick on the left (which starts the band) can't also be a
        # right tick (which ends a band). Otherwise we would have two
        # bands next to eachother.
        elif left in rights:
            continue

        lefts.append(left)
        rights.append(right)

    for (left, right) in zip(lefts, rights):
        ax.axvspan(left, right, color=color, alpha=alpha, zorder=-2)

    # Reset the x range so that we do not have a weird empty area on the right
    # side if we have to add one last band.
    ax.set_xlim((x_min, x_max))


def save_plot(  # type: ignore[no-any-unimported]
    fig: plt.Figure, metadata: Dict[str, str], filename: str
) -> None:
    """Save the plot with metadata and tight layout.

    Args:
        fig (matplotlib figure): The figure to save.
        metadata (dict): Example { "Contributor": "bord4@bt.no" }
        filename (str): The loction to save the file to.

    """

    fig.savefig(
        fname=f"{filename}",
        bbox_inches="tight",
        metadata=metadata,
    )
