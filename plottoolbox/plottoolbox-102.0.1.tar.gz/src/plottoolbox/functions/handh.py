import os

import matplotlib.pyplot as plt
from matplotlib import gridspec
from toolbox_utils import tsutils

from .. import plotutils


def handh(
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
    round_index=None,
    source_units=None,
    target_units=None,
    plot_styles="bright",
):
    r"""Plot data."""

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
        os.path.join(style_loc, f"{i}.mplstyle")
        if os.path.exists(os.path.join(style_loc, f"{i}.mplstyle"))
        else i
        for i in plot_styles
    ]

    plt.style.use(plot_styles)

    figsize = tsutils.make_list(figsize, n=2)

    fig = plt.figure(figsize=figsize)

    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 2])

    # HYDROGRAM CHART
    ax = plt.subplot(gs[1])
    tsd[0].plot(ax=ax, kind="time", logy=logy)
    ax.set_ylabel("Q", color="b")
    ax.set_xlabel("Time")
    ax.tick_params(axis="y", colors="b")
    ax.xaxis.grid(b=True, which="major", color=".7", linestyle="-")
    ax.yaxis.grid(b=True, which="major", color=".7", linestyle="-")
    ax.set_ylim(0, max(sQ) * 1.2)

    # PRECIPITATION/HYETOGRAPH CHART
    ax2 = plt.subplot(gs[0])
    tsd[1].plot(ax=ax2, kind="bar", color="#b0c4de")
    ax2.xaxis.grid(b=True, which="major", color=".7", linestyle="-")
    ax2.yaxis.grid(b=True, which="major", color="0.7", linestyle="-")
    ax2.set_ylabel("P")
    plt.setp(ax2.get_xticklabels(), visible=False)

    plt.tight_layout()
    ax2.invert_yaxis()
    plt.gcf().subplots_adjust(bottom=0.15)
    if ofilename is not None:
        plt.savefig(ofilename)
    return plt
