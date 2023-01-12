#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_11 import option
from .min_allowed import min_allowed
from .max_allowed import max_allowed
from .wall_zones import wall_zones
from .phase_26 import phase
class yplus_ystar(Group):
    """
    'yplus_ystar' child.
    """

    fluent_name = "yplus-ystar"

    child_names = \
        ['option', 'min_allowed', 'max_allowed', 'wall_zones', 'phase']

    option: option = option
    """
    option child of yplus_ystar.
    """
    min_allowed: min_allowed = min_allowed
    """
    min_allowed child of yplus_ystar.
    """
    max_allowed: max_allowed = max_allowed
    """
    max_allowed child of yplus_ystar.
    """
    wall_zones: wall_zones = wall_zones
    """
    wall_zones child of yplus_ystar.
    """
    phase: phase = phase
    """
    phase child of yplus_ystar.
    """
