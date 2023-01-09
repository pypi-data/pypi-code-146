#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .relative_permeability import relative_permeability
from .capillary_pressure_as_diffusion import capillary_pressure_as_diffusion
class porous_media(Group):
    """
    Multiphase miscellaneous porous media numerics menu.
    """

    fluent_name = "porous-media"

    child_names = \
        ['relative_permeability', 'capillary_pressure_as_diffusion']

    relative_permeability: relative_permeability = relative_permeability
    """
    relative_permeability child of porous_media.
    """
    capillary_pressure_as_diffusion: capillary_pressure_as_diffusion = capillary_pressure_as_diffusion
    """
    capillary_pressure_as_diffusion child of porous_media.
    """
