#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .cell_distance import cell_distance
from .normal_distance import normal_distance
from .volume_distance import volume_distance
class distance_option(Group):
    """
    'distance_option' child.
    """

    fluent_name = "distance-option"

    child_names = \
        ['option', 'cell_distance', 'normal_distance', 'volume_distance']

    option: option = option
    """
    option child of distance_option.
    """
    cell_distance: cell_distance = cell_distance
    """
    cell_distance child of distance_option.
    """
    normal_distance: normal_distance = normal_distance
    """
    normal_distance child of distance_option.
    """
    volume_distance: volume_distance = volume_distance
    """
    volume_distance child of distance_option.
    """
