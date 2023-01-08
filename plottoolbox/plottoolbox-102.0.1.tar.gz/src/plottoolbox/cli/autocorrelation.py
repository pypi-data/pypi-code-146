"""Collection of functions for the manipulation of time series."""


import warnings

import cltoolbox
import matplotlib
from cltoolbox.rst_text_formatter import RSTHelpFormatter
from toolbox_utils import tsutils

from .. import plotutils
from ..functions.autocorrelation import autocorrelation

matplotlib.use("Agg")
warnings.filterwarnings("ignore")


@cltoolbox.command("autocorrelation", formatter_class=RSTHelpFormatter)
@tsutils.doc(plotutils.ldocstrings)
def autocorrelation_cli(
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
    autocorrelation(
        input_ts=input_ts,
        columns=columns,
        start_date=start_date,
        end_date=end_date,
        clean=clean,
        skiprows=skiprows,
        index_type=index_type,
        names=names,
        ofilename=ofilename,
        xtitle=xtitle,
        ytitle=ytitle,
        title=title,
        figsize=figsize,
        legend=legend,
        legend_names=legend_names,
        xlim=xlim,
        ylim=ylim,
        grid=grid,
        xlabel_rotation=xlabel_rotation,
        ylabel_rotation=ylabel_rotation,
        por=por,
        round_index=round_index,
        source_units=source_units,
        target_units=target_units,
        plot_styles=plot_styles,
    )


autocorrelation_cli.__doc__ = autocorrelation.__doc__
