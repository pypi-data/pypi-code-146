#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .diffusion_rate_constant import diffusion_rate_constant
from .pre_exponential_factor import pre_exponential_factor
from .activation_energy import activation_energy
from .char_porosity import char_porosity
from .mean_pore_radius import mean_pore_radius
from .specific_internal_surface_area import specific_internal_surface_area
from .tortuosity import tortuosity
from .burning_mode import burning_mode
class intrinsic_model(Group):
    """
    'intrinsic_model' child.
    """

    fluent_name = "intrinsic-model"

    child_names = \
        ['diffusion_rate_constant', 'pre_exponential_factor',
         'activation_energy', 'char_porosity', 'mean_pore_radius',
         'specific_internal_surface_area', 'tortuosity', 'burning_mode']

    diffusion_rate_constant: diffusion_rate_constant = diffusion_rate_constant
    """
    diffusion_rate_constant child of intrinsic_model.
    """
    pre_exponential_factor: pre_exponential_factor = pre_exponential_factor
    """
    pre_exponential_factor child of intrinsic_model.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of intrinsic_model.
    """
    char_porosity: char_porosity = char_porosity
    """
    char_porosity child of intrinsic_model.
    """
    mean_pore_radius: mean_pore_radius = mean_pore_radius
    """
    mean_pore_radius child of intrinsic_model.
    """
    specific_internal_surface_area: specific_internal_surface_area = specific_internal_surface_area
    """
    specific_internal_surface_area child of intrinsic_model.
    """
    tortuosity: tortuosity = tortuosity
    """
    tortuosity child of intrinsic_model.
    """
    burning_mode: burning_mode = burning_mode
    """
    burning_mode child of intrinsic_model.
    """
