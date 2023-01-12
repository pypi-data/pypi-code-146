#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .diffusion_collision_integral import diffusion_collision_integral
from .viscosity_collision_integral import viscosity_collision_integral
class neutral_involved_interaction(Group):
    """
    'neutral_involved_interaction' child.
    """

    fluent_name = "neutral-involved-interaction"

    child_names = \
        ['diffusion_collision_integral', 'viscosity_collision_integral']

    diffusion_collision_integral: diffusion_collision_integral = diffusion_collision_integral
    """
    diffusion_collision_integral child of neutral_involved_interaction.
    """
    viscosity_collision_integral: viscosity_collision_integral = viscosity_collision_integral
    """
    viscosity_collision_integral child of neutral_involved_interaction.
    """
