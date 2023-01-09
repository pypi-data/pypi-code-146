#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .total_period_count import total_period_count
from .time_step_count_1 import time_step_count
from .total_time_step_count import total_time_step_count
from .total_time import total_time
from .incremental_time import incremental_time
from .max_iter_per_step import max_iter_per_step
from .postprocess import postprocess
from .post_iter_per_time_step_count import post_iter_per_time_step_count
class dual_time_iterate(Command):
    """
    Perform unsteady iterations.
    
    Parameters
    ----------
        total_period_count : int
            Set number of total periods.
        time_step_count : int
            Set inceremtal number of Time steps.
        total_time_step_count : int
            Set total number of Time steps.
        total_time : real
            Set Total Simulation Time.
        incremental_time : real
            Set Incremental Time.
        max_iter_per_step : int
            Set Maximum Number of iterations per time step.
        postprocess : bool
            Enable/Disable Postprocess pollutant solution?.
        post_iter_per_time_step_count : int
            Set Number of post-processing iterations per time step.
    
    """

    fluent_name = "dual-time-iterate"

    argument_names = \
        ['total_period_count', 'time_step_count', 'total_time_step_count',
         'total_time', 'incremental_time', 'max_iter_per_step', 'postprocess',
         'post_iter_per_time_step_count']

    total_period_count: total_period_count = total_period_count
    """
    total_period_count argument of dual_time_iterate.
    """
    time_step_count: time_step_count = time_step_count
    """
    time_step_count argument of dual_time_iterate.
    """
    total_time_step_count: total_time_step_count = total_time_step_count
    """
    total_time_step_count argument of dual_time_iterate.
    """
    total_time: total_time = total_time
    """
    total_time argument of dual_time_iterate.
    """
    incremental_time: incremental_time = incremental_time
    """
    incremental_time argument of dual_time_iterate.
    """
    max_iter_per_step: max_iter_per_step = max_iter_per_step
    """
    max_iter_per_step argument of dual_time_iterate.
    """
    postprocess: postprocess = postprocess
    """
    postprocess argument of dual_time_iterate.
    """
    post_iter_per_time_step_count: post_iter_per_time_step_count = post_iter_per_time_step_count
    """
    post_iter_per_time_step_count argument of dual_time_iterate.
    """
