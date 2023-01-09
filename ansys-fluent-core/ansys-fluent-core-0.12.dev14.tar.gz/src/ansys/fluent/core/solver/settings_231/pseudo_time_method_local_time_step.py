#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .pseudo_time_courant_number import pseudo_time_courant_number
from .pseudo_time_step_method_solid_zone import pseudo_time_step_method_solid_zone
from .time_step_size_scale_factor import time_step_size_scale_factor
class pseudo_time_method_local_time_step(Group):
    """
    'pseudo_time_method_local_time_step' child.
    """

    fluent_name = "pseudo-time-method-local-time-step"

    child_names = \
        ['pseudo_time_courant_number', 'pseudo_time_step_method_solid_zone',
         'time_step_size_scale_factor']

    pseudo_time_courant_number: pseudo_time_courant_number = pseudo_time_courant_number
    """
    pseudo_time_courant_number child of pseudo_time_method_local_time_step.
    """
    pseudo_time_step_method_solid_zone: pseudo_time_step_method_solid_zone = pseudo_time_step_method_solid_zone
    """
    pseudo_time_step_method_solid_zone child of pseudo_time_method_local_time_step.
    """
    time_step_size_scale_factor: time_step_size_scale_factor = time_step_size_scale_factor
    """
    time_step_size_scale_factor child of pseudo_time_method_local_time_step.
    """
