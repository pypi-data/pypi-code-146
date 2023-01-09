#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .trim_option import trim_option
from .update_frequency import update_frequency
from .damping_factor import damping_factor
from .thrust_coefficient import thrust_coefficient
from .x_moment_coefficient import x_moment_coefficient
from .y_moment_coefficient import y_moment_coefficient
class trimming(Group):
    """
    Menu to define rotor trimming set-up.
    
     - trim-option       : to define collective and cyclic pitches to trim, 
     - update-frequency  : the number of solver iterations that pitch angle will be updated each time, 
     - damping-factor    : relaxation factor for pitch angles, 
     - thrust-coef       : desired thrust coefficient to set pitch for
     - moment-coef-x     : desired x-moment coefficient to set pitch for, 
     - moment-coef-y     : desired y-moment coefficient to set pitch for, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "trimming"

    child_names = \
        ['trim_option', 'update_frequency', 'damping_factor',
         'thrust_coefficient', 'x_moment_coefficient',
         'y_moment_coefficient']

    trim_option: trim_option = trim_option
    """
    trim_option child of trimming.
    """
    update_frequency: update_frequency = update_frequency
    """
    update_frequency child of trimming.
    """
    damping_factor: damping_factor = damping_factor
    """
    damping_factor child of trimming.
    """
    thrust_coefficient: thrust_coefficient = thrust_coefficient
    """
    thrust_coefficient child of trimming.
    """
    x_moment_coefficient: x_moment_coefficient = x_moment_coefficient
    """
    x_moment_coefficient child of trimming.
    """
    y_moment_coefficient: y_moment_coefficient = y_moment_coefficient
    """
    y_moment_coefficient child of trimming.
    """
