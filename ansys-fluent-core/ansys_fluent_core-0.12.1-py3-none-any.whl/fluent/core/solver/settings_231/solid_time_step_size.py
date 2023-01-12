#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_solid_time_step import enable_solid_time_step
from .choose_auto_time_stepping import choose_auto_time_stepping
from .time_step_size_1 import time_step_size
class solid_time_step_size(Group):
    """
    'solid_time_step_size' child.
    """

    fluent_name = "solid-time-step-size"

    child_names = \
        ['enable_solid_time_step', 'choose_auto_time_stepping',
         'time_step_size']

    enable_solid_time_step: enable_solid_time_step = enable_solid_time_step
    """
    enable_solid_time_step child of solid_time_step_size.
    """
    choose_auto_time_stepping: choose_auto_time_stepping = choose_auto_time_stepping
    """
    choose_auto_time_stepping child of solid_time_step_size.
    """
    time_step_size: time_step_size = time_step_size
    """
    time_step_size child of solid_time_step_size.
    """
