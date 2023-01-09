#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .cbk import cbk
from .kinetics_diffusion_limited import kinetics_diffusion_limited
from .intrinsic_model import intrinsic_model
from .multiple_surface_reactions import multiple_surface_reactions
class combustion_model(Group):
    """
    'combustion_model' child.
    """

    fluent_name = "combustion-model"

    child_names = \
        ['option', 'cbk', 'kinetics_diffusion_limited', 'intrinsic_model',
         'multiple_surface_reactions']

    option: option = option
    """
    option child of combustion_model.
    """
    cbk: cbk = cbk
    """
    cbk child of combustion_model.
    """
    kinetics_diffusion_limited: kinetics_diffusion_limited = kinetics_diffusion_limited
    """
    kinetics_diffusion_limited child of combustion_model.
    """
    intrinsic_model: intrinsic_model = intrinsic_model
    """
    intrinsic_model child of combustion_model.
    """
    multiple_surface_reactions: multiple_surface_reactions = multiple_surface_reactions
    """
    multiple_surface_reactions child of combustion_model.
    """
