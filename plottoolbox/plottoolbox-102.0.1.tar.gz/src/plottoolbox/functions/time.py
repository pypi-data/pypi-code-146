"""Collection of functions for the manipulation of time series."""

import os
import warnings

import matplotlib
import pandas as pd
from toolbox_utils import tsutils

from .. import plotutils

matplotlib.use("Agg")
warnings.filterwarnings("ignore")


def time(
    input_ts="-",
    columns=None,
    start_date=None,
    end_date=None,
    clean=False,
    skiprows=None,
    index_type="datetime",
    names=None,
    ofilename="plot.png",
    xtitle="",
    ytitle="",
    title="",
    figsize="10,6.0",
    legend=None,
    legend_names=None,
    subplots=False,
    sharex=True,
    sharey=False,
    colors="auto",
    linestyles="auto",
    markerstyles=" ",
    style="auto",
    xaxis="arithmetic",
    yaxis="arithmetic",
    xlim=None,
    ylim=None,
    secondary_y=False,
    mark_right=True,
    grid=False,
    drawstyle="default",
    por=False,
    invert_xaxis=False,
    invert_yaxis=False,
    round_index=None,
    source_units=None,
    target_units=None,
    plot_styles="bright",
    hlines_y=None,
    hlines_xmin=None,
    hlines_xmax=None,
    hlines_colors=None,
    hlines_linestyles="-",
    vlines_x=None,
    vlines_ymin=None,
    vlines_ymax=None,
    vlines_colors=None,
    vlines_linestyles="-",
    **kwds,
):
    r"""Plot data."""

    import matplotlib.pyplot as plt

    # set up dataframe
    tsd = tsutils.common_kwds(
        input_ts,
        skiprows=skiprows,
        names=names,
        index_type=index_type,
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna="all",
        source_units=source_units,
        target_units=target_units,
        clean=clean,
        por=por,
    )
    # check dataframe
    if not isinstance(tsd.index, pd.DatetimeIndex):
        raise ValueError(
            tsutils.error_wrapper(
                """
                The index is not a datetime index and cannot be plotted as
                a time-series. Instead of "time" you might want "xy" or change
                the index to a datetime index.
                """
            )
        )

    # Need to work around some old option defaults with the implementation of
    # cltoolbox
    legend = legend == "" or legend == "True" or legend is None or legend is True
    plottype = "time"
    lnames = tsutils.make_list(legend_names)
    tsd, lnames = plotutils.check_column_legend(plottype, tsd, lnames)

    # check axis scales
    logx = xaxis == "log"
    logy = yaxis == "log"
    xlim = plotutils.know_your_limits(xlim, axis=xaxis)
    ylim = plotutils.know_your_limits(ylim, axis=yaxis)

    # process styles: colors, linestyles, markerstyles
    (
        style,
        colors,
        linestyles,
        markerstyles,
        icolors,
        ilinestyles,
        imarkerstyles,
    ) = plotutils.prepare_styles(
        len(tsd.columns), style, colors, linestyles, markerstyles
    )

    plot_styles = tsutils.make_list(plot_styles) + ["no-latex"]
    style_loc = os.path.join(
        os.path.dirname(__file__), os.pardir, "SciencePlots_styles"
    )
    plot_styles = [
        os.path.join(style_loc, i + ".mplstyle")
        if os.path.exists(os.path.join(style_loc, i + ".mplstyle"))
        else i
        for i in plot_styles
    ]
    plt.style.use(plot_styles)

    figsize = tsutils.make_list(figsize, n=2)
    _, ax = plt.subplots(figsize=figsize)

    ax = tsd.plot(
        legend=legend,
        subplots=subplots,
        sharex=sharex,
        sharey=sharey,
        logx=logx,
        logy=logy,
        xlim=xlim,
        ylim=ylim,
        secondary_y=secondary_y,
        mark_right=mark_right,
        figsize=figsize,
        drawstyle=drawstyle,
    )
    for line in ax.lines:
        c = next(icolors) if icolors is not None else None
        m = next(imarkerstyles) if imarkerstyles is not None else None
        l = next(ilinestyles) if ilinestyles is not None else None
        if c is not None:
            plt.setp(line, color=c)
        plt.setp(line, marker=m)
        plt.setp(line, linestyle=l)

    xtitle = xtitle or "Time"
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    if legend:
        plt.legend(loc="best")

    plt = plotutils.hv_lines(
        plt,
        hlines_y=hlines_y,
        hlines_xmin=hlines_xmin,
        hlines_xmax=hlines_xmax,
        hlines_colors=hlines_colors,
        hlines_linestyles=hlines_linestyles,
        vlines_x=None,
        vlines_ymin=None,
        vlines_ymax=None,
        vlines_colors=None,
        vlines_linestyles=None,
    )

    if invert_xaxis is True:
        plt.gca().invert_xaxis()
    if invert_yaxis is True:
        plt.gca().invert_yaxis()

    plt.grid(grid)

    plt.title(title)
    plt.tight_layout()
    if ofilename is not None:
        plt.savefig(ofilename)
    return plt
