#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .none_1 import none
from .scale_by_global_average import scale_by_global_average
from .scale_by_zone_average import scale_by_zone_average
from .scale_by_global_maximum import scale_by_global_maximum
from .scale_by_zone_maximum import scale_by_zone_maximum
class scaling(Group):
    """
    'scaling' child.
    """

    fluent_name = "scaling"

    child_names = \
        ['option', 'none', 'scale_by_global_average', 'scale_by_zone_average',
         'scale_by_global_maximum', 'scale_by_zone_maximum']

    option: option = option
    """
    option child of scaling.
    """
    none: none = none
    """
    none child of scaling.
    """
    scale_by_global_average: scale_by_global_average = scale_by_global_average
    """
    scale_by_global_average child of scaling.
    """
    scale_by_zone_average: scale_by_zone_average = scale_by_zone_average
    """
    scale_by_zone_average child of scaling.
    """
    scale_by_global_maximum: scale_by_global_maximum = scale_by_global_maximum
    """
    scale_by_global_maximum child of scaling.
    """
    scale_by_zone_maximum: scale_by_zone_maximum = scale_by_zone_maximum
    """
    scale_by_zone_maximum child of scaling.
    """
