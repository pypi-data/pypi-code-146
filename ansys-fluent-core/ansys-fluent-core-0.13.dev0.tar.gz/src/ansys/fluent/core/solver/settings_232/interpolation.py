#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .interpolate_flow_cp import interpolate_flow_cp
from .interpolate_flow_density import interpolate_flow_density
from .interpolate_flow_solution_gradients import interpolate_flow_solution_gradients
from .interpolate_flow_viscosity import interpolate_flow_viscosity
from .interpolate_temperature import interpolate_temperature
from .zero_nodal_velocities_on_walls import zero_nodal_velocities_on_walls
class interpolation(Group):
    """
    Main menu holding options to enable/disable interpolation of flow data to the particle position.
    """

    fluent_name = "interpolation"

    child_names = \
        ['interpolate_flow_cp', 'interpolate_flow_density',
         'interpolate_flow_solution_gradients', 'interpolate_flow_viscosity',
         'interpolate_temperature', 'zero_nodal_velocities_on_walls']

    interpolate_flow_cp: interpolate_flow_cp = interpolate_flow_cp
    """
    interpolate_flow_cp child of interpolation.
    """
    interpolate_flow_density: interpolate_flow_density = interpolate_flow_density
    """
    interpolate_flow_density child of interpolation.
    """
    interpolate_flow_solution_gradients: interpolate_flow_solution_gradients = interpolate_flow_solution_gradients
    """
    interpolate_flow_solution_gradients child of interpolation.
    """
    interpolate_flow_viscosity: interpolate_flow_viscosity = interpolate_flow_viscosity
    """
    interpolate_flow_viscosity child of interpolation.
    """
    interpolate_temperature: interpolate_temperature = interpolate_temperature
    """
    interpolate_temperature child of interpolation.
    """
    zero_nodal_velocities_on_walls: zero_nodal_velocities_on_walls = zero_nodal_velocities_on_walls
    """
    zero_nodal_velocities_on_walls child of interpolation.
    """
