#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .minimum_val import minimum_val
from .maximum_val import maximum_val
from .division_val import division_val
class histogram_parameters(Group):
    """
    Enter the parameter menu for the histogram.
    """

    fluent_name = "histogram-parameters"

    child_names = \
        ['minimum_val', 'maximum_val', 'division_val']

    minimum_val: minimum_val = minimum_val
    """
    minimum_val child of histogram_parameters.
    """
    maximum_val: maximum_val = maximum_val
    """
    maximum_val child of histogram_parameters.
    """
    division_val: division_val = division_val
    """
    division_val child of histogram_parameters.
    """
