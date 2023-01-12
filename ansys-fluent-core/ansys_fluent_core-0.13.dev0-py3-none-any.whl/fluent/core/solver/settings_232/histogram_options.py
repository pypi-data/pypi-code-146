#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .auto_range_1 import auto_range
from .correlation import correlation
from .cumulation_curve import cumulation_curve
from .diameter_statistics import diameter_statistics
from .histogram_mode import histogram_mode
from .percentage import percentage
from .variable_3 import variable_3
from .logarithmic import logarithmic
from .weighting import weighting
class histogram_options(Group):
    """
    Enter the settings menu for the histogram.
    """

    fluent_name = "histogram-options"

    child_names = \
        ['auto_range', 'correlation', 'cumulation_curve',
         'diameter_statistics', 'histogram_mode', 'percentage', 'variable_3',
         'logarithmic', 'weighting']

    auto_range: auto_range = auto_range
    """
    auto_range child of histogram_options.
    """
    correlation: correlation = correlation
    """
    correlation child of histogram_options.
    """
    cumulation_curve: cumulation_curve = cumulation_curve
    """
    cumulation_curve child of histogram_options.
    """
    diameter_statistics: diameter_statistics = diameter_statistics
    """
    diameter_statistics child of histogram_options.
    """
    histogram_mode: histogram_mode = histogram_mode
    """
    histogram_mode child of histogram_options.
    """
    percentage: percentage = percentage
    """
    percentage child of histogram_options.
    """
    variable_3: variable_3 = variable_3
    """
    variable_3 child of histogram_options.
    """
    logarithmic: logarithmic = logarithmic
    """
    logarithmic child of histogram_options.
    """
    weighting: weighting = weighting
    """
    weighting child of histogram_options.
    """
