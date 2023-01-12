#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .variable_lewis_number import variable_lewis_number
from .use_vapor_species_heat_capacity import use_vapor_species_heat_capacity
class convection_diffusion_controlled(Group):
    """
    'convection_diffusion_controlled' child.
    """

    fluent_name = "convection-diffusion-controlled"

    child_names = \
        ['variable_lewis_number', 'use_vapor_species_heat_capacity']

    variable_lewis_number: variable_lewis_number = variable_lewis_number
    """
    variable_lewis_number child of convection_diffusion_controlled.
    """
    use_vapor_species_heat_capacity: use_vapor_species_heat_capacity = use_vapor_species_heat_capacity
    """
    use_vapor_species_heat_capacity child of convection_diffusion_controlled.
    """
