#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .method import method
from .samp_time_period import samp_time_period
from .samp_time_steps import samp_time_steps
from .avg_time_period import avg_time_period
from .avg_time_steps import avg_time_steps
class statistics_controls(Command):
    """
    'statistics_controls' command.
    
    Parameters
    ----------
        method : int
            'method' child.
        samp_time_period : real
            'samp_time_period' child.
        samp_time_steps : int
            'samp_time_steps' child.
        avg_time_period : real
            'avg_time_period' child.
        avg_time_steps : int
            'avg_time_steps' child.
    
    """

    fluent_name = "statistics-controls"

    argument_names = \
        ['method', 'samp_time_period', 'samp_time_steps', 'avg_time_period',
         'avg_time_steps']

    method: method = method
    """
    method argument of statistics_controls.
    """
    samp_time_period: samp_time_period = samp_time_period
    """
    samp_time_period argument of statistics_controls.
    """
    samp_time_steps: samp_time_steps = samp_time_steps
    """
    samp_time_steps argument of statistics_controls.
    """
    avg_time_period: avg_time_period = avg_time_period
    """
    avg_time_period argument of statistics_controls.
    """
    avg_time_steps: avg_time_steps = avg_time_steps
    """
    avg_time_steps argument of statistics_controls.
    """
