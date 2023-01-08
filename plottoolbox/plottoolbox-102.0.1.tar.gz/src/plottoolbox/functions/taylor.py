"""Collection of functions for the manipulation of time series."""

import os
import warnings

import cltoolbox
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from cltoolbox.rst_text_formatter import RSTHelpFormatter
from toolbox_utils import tsutils

from .. import plotutils
from ..skill_metrics import centered_rms_dev, taylor_diagram

matplotlib.use("Agg")


warnings.filterwarnings("ignore")


def taylor(
    input_ts="-",
    columns=None,
    start_date=None,
    end_date=None,
    clean=False,
    skiprows=None,
    index_type="datetime",
    names=None,
    ofilename="plot.png",
    title="",
    figsize="10,6.0",
    legend=None,
    legend_names=None,
    colors="auto",
    linestyles="auto",
    markerstyles=" ",
    style="auto",
    por=False,
    round_index=None,
    source_units=None,
    target_units=None,
    plot_styles="bright",
    **kwds,
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

    # Need to work around some old option defaults with the implementation of
    # cltoolbox
    legend = legend == "" or legend == "True" or legend is None or legend is True
    plottype = "taylor"
    lnames = tsutils.make_list(legend_names)
    tsd, lnames = plotutils.check_column_legend(plottype, tsd, lnames)

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
    _, ax = plt.subplots(figsize=figsize)

    ref = tsd.iloc[:, 0]
    std = [np.std(ref)]
    ccoef = [1.0]
    crmsd = [0.0]
    for col in range(1, len(tsd.columns)):
        std.append(np.std(tsd.iloc[:, col]))
        ccoef.append(np.corrcoef(tsd.iloc[:, col], ref)[0][1])
        crmsd.append(centered_rms_dev(tsd.iloc[:, col].values, ref.values))

    taylor_diagram(np.array(std), np.array(crmsd), np.array(ccoef))

    plt.title(title)
    plt.tight_layout()
    if ofilename is not None:
        plt.savefig(ofilename)
    return plt
