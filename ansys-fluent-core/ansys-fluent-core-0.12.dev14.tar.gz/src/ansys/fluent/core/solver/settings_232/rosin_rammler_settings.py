#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .min_diam import min_diam
from .max_diam import max_diam
from .mean_diam import mean_diam
from .spread import spread
from .number_of_diameters import number_of_diameters
class rosin_rammler_settings(Group):
    """
    'rosin_rammler_settings' child.
    """

    fluent_name = "rosin-rammler-settings"

    child_names = \
        ['min_diam', 'max_diam', 'mean_diam', 'spread', 'number_of_diameters']

    min_diam: min_diam = min_diam
    """
    min_diam child of rosin_rammler_settings.
    """
    max_diam: max_diam = max_diam
    """
    max_diam child of rosin_rammler_settings.
    """
    mean_diam: mean_diam = mean_diam
    """
    mean_diam child of rosin_rammler_settings.
    """
    spread: spread = spread
    """
    spread child of rosin_rammler_settings.
    """
    number_of_diameters: number_of_diameters = number_of_diameters
    """
    number_of_diameters child of rosin_rammler_settings.
    """
