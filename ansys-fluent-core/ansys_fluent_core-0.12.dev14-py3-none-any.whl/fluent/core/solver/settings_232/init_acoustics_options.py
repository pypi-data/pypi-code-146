#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_ramping_length import set_ramping_length
from .time_step_count import time_step_count
class init_acoustics_options(Command):
    """
    'init_acoustics_options' command.
    
    Parameters
    ----------
        set_ramping_length : bool
            Enable/Disable ramping length and initialize acoustics.
        time_step_count : int
            Set number of timesteps for ramping of sources.
    
    """

    fluent_name = "init-acoustics-options"

    argument_names = \
        ['set_ramping_length', 'time_step_count']

    set_ramping_length: set_ramping_length = set_ramping_length
    """
    set_ramping_length argument of init_acoustics_options.
    """
    time_step_count: time_step_count = time_step_count
    """
    time_step_count argument of init_acoustics_options.
    """
