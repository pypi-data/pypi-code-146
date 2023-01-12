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
class kinetics_diffusion_limited(Group):
    """
    'kinetics_diffusion_limited' child.
    """

    fluent_name = "kinetics-diffusion-limited"

    child_names = \
        ['diffusion_rate_constant', 'pre_exponential_factor',
         'activation_energy']

    diffusion_rate_constant: diffusion_rate_constant = diffusion_rate_constant
    """
    diffusion_rate_constant child of kinetics_diffusion_limited.
    """
    pre_exponential_factor: pre_exponential_factor = pre_exponential_factor
    """
    pre_exponential_factor child of kinetics_diffusion_limited.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of kinetics_diffusion_limited.
    """
