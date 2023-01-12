#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .method_1 import method
from .time_step_interval import time_step_interval
from .time_interval import time_interval
from .iteration_interval import iteration_interval
class solve_frequency(Group):
    """
    Enter radiation solve frequency.
    """

    fluent_name = "solve-frequency"

    child_names = \
        ['method', 'time_step_interval', 'time_interval',
         'iteration_interval']

    method: method = method
    """
    method child of solve_frequency.
    """
    time_step_interval: time_step_interval = time_step_interval
    """
    time_step_interval child of solve_frequency.
    """
    time_interval: time_interval = time_interval
    """
    time_interval child of solve_frequency.
    """
    iteration_interval: iteration_interval = iteration_interval
    """
    iteration_interval child of solve_frequency.
    """
