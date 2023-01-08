"""Collection of functions for the manipulation of time series."""


import warnings

import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
from toolbox_utils import tsutils

from .. import plotutils

matplotlib.use("Agg")
warnings.filterwarnings("ignore")


def autocorrelation(
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
    xlim=None,
    ylim=None,
    grid=False,
    xlabel_rotation=0,
    ylabel_rotation=0,
    por=False,
    round_index=None,
    source_units=None,
    target_units=None,
    plot_styles="bright",
):
    r"""Autocorrelation plot.

    The "autocorrelation" creates an autocorrelation plot.

    The horizontal lines in the plot correspond to 95% and 99% confidence
    bands.

    The dashed line is 99% confidence band.

    Only available for a single time-series.

    ${yone}

    Parameters
    ----------
    ${input_ts}
    ${columns}
    ${start_date}
    ${end_date}
    ${clean}
    ${skiprows}
    ${index_type}
    ${names}
    ${ofilename}
    ${xtitle}
    ${ytitle}
    ${title}
    ${figsize}
    ${legend}
    ${legend_names}
    ${xlim}
    ${ylim}
    ${grid}
    ${xlabel_rotation}
    ${ylabel_rotation}
    ${por}
    ${round_index}
    ${source_units}
    ${target_units}
    ${plot_styles}
    """

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

    # Need to work around some old option defaults with the implementation of
    # cltoolbox
    legend = legend == "" or legend == "True" or legend is None or legend is True
    plottype = "autocorrelation"
    lnames = tsutils.make_list(legend_names)
    tsd, lnames = plotutils.check_column_legend(plottype, tsd, lnames)

    plt.style.use(plot_styles)

    figsize = tsutils.make_list(figsize, n=2)
    _, ax = plt.subplots(figsize=figsize)

    autocorrelation_plot(tsd, ax=ax)
    # This is to help pretty print the frequency
    try:
        tsd = tsutils.asbest_freq(tsd)
        try:
            pltfreq = str(tsd.index.freq, "utf-8").lower()
        except TypeError:
            pltfreq = str(tsd.index.freq).lower()
        beginstr = 3 if pltfreq.split(" ")[0][1:] == "1" else 1
        short_freq = "" if pltfreq == None else f"({pltfreq[beginstr:-1]})"
    except AttributeError:
        short_freq = ""
    xtitle = xtitle or f"Time Lag {short_freq}"

    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    plt.xticks(rotation=xlabel_rotation)
    plt.yticks(rotation=ylabel_rotation)

    plt.grid(grid)

    plt.title(title)

    plt.xlim(xlim)
    plt.ylim(ylim)

    plt.tight_layout()
    if ofilename is not None:
        plt.savefig(ofilename)
    return plt
