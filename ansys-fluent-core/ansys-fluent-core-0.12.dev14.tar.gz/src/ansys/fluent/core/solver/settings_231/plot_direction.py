#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .direction_vector_2 import direction_vector
from .curve_length import curve_length
class plot_direction(Group):
    """
    'plot_direction' child.
    """

    fluent_name = "plot-direction"

    child_names = \
        ['option', 'direction_vector', 'curve_length']

    option: option = option
    """
    option child of plot_direction.
    """
    direction_vector: direction_vector = direction_vector
    """
    direction_vector child of plot_direction.
    """
    curve_length: curve_length = curve_length
    """
    curve_length child of plot_direction.
    """
