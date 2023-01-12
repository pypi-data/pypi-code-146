#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .control_by import control_by
from .max_number_of_steps import max_number_of_steps
from .length_scale import length_scale
from .step_length_factor import step_length_factor
class tracking_parameters(Group):
    """
    Main menu to control the time integration of the particle trajectory equations:
    
     - the maximum number of steps; the trajectory calculation is stopped and the particle aborted when the particle reaches this limit.
     - the length scale/step length factor; this factor is used to set the time step size for integration within a cell.
    
    """

    fluent_name = "tracking-parameters"

    child_names = \
        ['control_by', 'max_number_of_steps', 'length_scale',
         'step_length_factor']

    control_by: control_by = control_by
    """
    control_by child of tracking_parameters.
    """
    max_number_of_steps: max_number_of_steps = max_number_of_steps
    """
    max_number_of_steps child of tracking_parameters.
    """
    length_scale: length_scale = length_scale
    """
    length_scale child of tracking_parameters.
    """
    step_length_factor: step_length_factor = step_length_factor
    """
    step_length_factor child of tracking_parameters.
    """
