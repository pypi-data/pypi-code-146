"""Collection of functions for the manipulation of time series."""

import warnings

import cltoolbox
import matplotlib
from cltoolbox.rst_text_formatter import RSTHelpFormatter
from toolbox_utils import tsutils

from .. import plotutils
from ..functions.target import target

matplotlib.use("Agg")


warnings.filterwarnings("ignore")


@cltoolbox.command("target", formatter_class=RSTHelpFormatter)
@tsutils.doc(plotutils.ldocstrings)
def target_cli(
    obs_col=None,
    sim_col=None,
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
):
    r"""Creates a "target" diagram to plot goodness of fit.

    "target" creates a target diagram that compares three goodness of fit
    statistics on one plot.  The three goodness of fit statistics calculated
    and displayed are bias, root mean square deviation, and centered root mean
    square deviation.  The data columns have to be organized as
    'observed,simulated1,simulated2,simulated3,...etc.'

    Parameters
    ----------
    obs_col
        If integer represents the column number of standard input. Can be
        If integer represents the column number of standard input. Can be
        a csv, wdm, hdf or xlsx file following format specified in
        'tstoolbox read ...'.
    sim_col
        If integer represents the column number of standard input. Can be
        a csv, wdm, hdf or xlsx file following format specified in
        'tstoolbox read ...'.
    ${input_ts}
    ${columns}
    ${start_date}
    ${end_date}
    ${clean}
    ${skiprows}
    ${index_type}
    ${names}
    ${ofilename}
    ${title}
    ${figsize}
    ${legend}
    ${legend_names}
    ${colors}
    ${linestyles}
    ${markerstyles}
    ${style}
    ${por}
    ${round_index}
    ${source_units}
    ${target_units}
    ${plot_styles}
    """
    obs_col = obs_col or 1
    sim_col = sim_col or 2
    target(
        obs_col=None,
        sim_col=None,
        input_ts=input_ts,
        columns=columns,
        start_date=start_date,
        end_date=end_date,
        clean=clean,
        skiprows=skiprows,
        index_type=index_type,
        names=names,
        ofilename=ofilename,
        title=title,
        figsize=figsize,
        legend=legend,
        legend_names=legend_names,
        colors=colors,
        linestyles=linestyles,
        markerstyles=markerstyles,
        style=style,
        por=por,
        round_index=round_index,
        source_units=source_units,
        target_units=target_units,
        plot_styles=plot_styles,
    )


target.__doc__ = target_cli.__doc__
