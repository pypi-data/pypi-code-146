#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .time_step_method import time_step_method
from .pseudo_time_step_size import pseudo_time_step_size
from .length_scale_methods import length_scale_methods
from .time_step_size_scale_factor_1 import time_step_size_scale_factor
from .length_scale_1 import length_scale
from .auto_time_size_calc_solid_zone import auto_time_size_calc_solid_zone
from .time_solid_scale_factor import time_solid_scale_factor
from .time_step_size_for_solid_zone import time_step_size_for_solid_zone
class time_step_method(Group):
    """
    'time_step_method' child.
    """

    fluent_name = "time-step-method"

    child_names = \
        ['time_step_method', 'pseudo_time_step_size', 'length_scale_methods',
         'time_step_size_scale_factor', 'length_scale',
         'auto_time_size_calc_solid_zone', 'time_solid_scale_factor',
         'time_step_size_for_solid_zone']

    time_step_method: time_step_method = time_step_method
    """
    time_step_method child of time_step_method.
    """
    pseudo_time_step_size: pseudo_time_step_size = pseudo_time_step_size
    """
    pseudo_time_step_size child of time_step_method.
    """
    length_scale_methods: length_scale_methods = length_scale_methods
    """
    length_scale_methods child of time_step_method.
    """
    time_step_size_scale_factor: time_step_size_scale_factor = time_step_size_scale_factor
    """
    time_step_size_scale_factor child of time_step_method.
    """
    length_scale: length_scale = length_scale
    """
    length_scale child of time_step_method.
    """
    auto_time_size_calc_solid_zone: auto_time_size_calc_solid_zone = auto_time_size_calc_solid_zone
    """
    auto_time_size_calc_solid_zone child of time_step_method.
    """
    time_solid_scale_factor: time_solid_scale_factor = time_solid_scale_factor
    """
    time_solid_scale_factor child of time_step_method.
    """
    time_step_size_for_solid_zone: time_step_size_for_solid_zone = time_step_size_for_solid_zone
    """
    time_step_size_for_solid_zone child of time_step_method.
    """
