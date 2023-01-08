"""Collection of functions for the manipulation of time series."""

import os.path
import sys
import warnings

from cltoolbox import command, main

from .cli.autocorrelation import autocorrelation
from .cli.bar import bar
from .cli.bar_stacked import bar_stacked
from .cli.barh import barh
from .cli.barh_stacked import barh_stacked
from .cli.bootstrap import bootstrap
from .cli.boxplot import boxplot
from .cli.double_mass import double_mass
from .cli.heatmap import heatmap
from .cli.histogram import histogram
from .cli.kde import kde
from .cli.kde_time import kde_time
from .cli.lag_plot import lag_plot
from .cli.lognorm_xaxis import lognorm_xaxis
from .cli.lognorm_yaxis import lognorm_yaxis
from .cli.norm_xaxis import norm_xaxis
from .cli.norm_yaxis import norm_yaxis
from .cli.probability_density import probability_density
from .cli.scatter_matrix import scatter_matrix
from .cli.target import target
from .cli.taylor import taylor
from .cli.time import time
from .cli.weibull_xaxis import weibull_xaxis
from .cli.weibull_yaxis import weibull_yaxis
from .cli.xy import xy

warnings.filterwarnings("ignore")


@command()
def about():
    """Display version number and system information."""
    from toolbox_utils import tsutils

    tsutils.about(__name__)


def lmain():
    """Set debug and run cltoolbox.main function."""
    if not os.path.exists("debug_plottoolbox"):
        sys.tracebacklimit = 0
    main()


if __name__ == "__main__":
    lmain()
