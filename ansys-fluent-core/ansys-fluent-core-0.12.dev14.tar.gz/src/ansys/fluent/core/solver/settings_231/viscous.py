#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .model import model
from .options_1 import options
from .spalart_allmaras_production import spalart_allmaras_production
from .k_epsilon_model import k_epsilon_model
from .k_omega_model import k_omega_model
from .k_omega_options import k_omega_options
from .rng_options import rng_options
from .near_wall_treatment import near_wall_treatment
from .reynolds_stress_model import reynolds_stress_model
from .subgrid_scale_model import subgrid_scale_model
from .les_model_options import les_model_options
from .reynolds_stress_options import reynolds_stress_options
from .rans_model import rans_model
from .des_options import des_options
from .transition_module import transition_module
from .user_defined_transition import user_defined_transition
from .multiphase_turbulence import multiphase_turbulence
from .turbulence_expert import turbulence_expert
from .geko_options import geko_options
from .transition_model_options import transition_model_options
from .transition_sst_option import transition_sst_option
from .user_defined import user_defined
from .sa_enhanced_wall_treatment import sa_enhanced_wall_treatment
from .sa_damping import sa_damping
class viscous(Group):
    """
    'viscous' child.
    """

    fluent_name = "viscous"

    child_names = \
        ['model', 'options', 'spalart_allmaras_production', 'k_epsilon_model',
         'k_omega_model', 'k_omega_options', 'rng_options',
         'near_wall_treatment', 'reynolds_stress_model',
         'subgrid_scale_model', 'les_model_options',
         'reynolds_stress_options', 'rans_model', 'des_options',
         'transition_module', 'user_defined_transition',
         'multiphase_turbulence', 'turbulence_expert', 'geko_options',
         'transition_model_options', 'transition_sst_option', 'user_defined',
         'sa_enhanced_wall_treatment', 'sa_damping']

    model: model = model
    """
    model child of viscous.
    """
    options: options = options
    """
    options child of viscous.
    """
    spalart_allmaras_production: spalart_allmaras_production = spalart_allmaras_production
    """
    spalart_allmaras_production child of viscous.
    """
    k_epsilon_model: k_epsilon_model = k_epsilon_model
    """
    k_epsilon_model child of viscous.
    """
    k_omega_model: k_omega_model = k_omega_model
    """
    k_omega_model child of viscous.
    """
    k_omega_options: k_omega_options = k_omega_options
    """
    k_omega_options child of viscous.
    """
    rng_options: rng_options = rng_options
    """
    rng_options child of viscous.
    """
    near_wall_treatment: near_wall_treatment = near_wall_treatment
    """
    near_wall_treatment child of viscous.
    """
    reynolds_stress_model: reynolds_stress_model = reynolds_stress_model
    """
    reynolds_stress_model child of viscous.
    """
    subgrid_scale_model: subgrid_scale_model = subgrid_scale_model
    """
    subgrid_scale_model child of viscous.
    """
    les_model_options: les_model_options = les_model_options
    """
    les_model_options child of viscous.
    """
    reynolds_stress_options: reynolds_stress_options = reynolds_stress_options
    """
    reynolds_stress_options child of viscous.
    """
    rans_model: rans_model = rans_model
    """
    rans_model child of viscous.
    """
    des_options: des_options = des_options
    """
    des_options child of viscous.
    """
    transition_module: transition_module = transition_module
    """
    transition_module child of viscous.
    """
    user_defined_transition: user_defined_transition = user_defined_transition
    """
    user_defined_transition child of viscous.
    """
    multiphase_turbulence: multiphase_turbulence = multiphase_turbulence
    """
    multiphase_turbulence child of viscous.
    """
    turbulence_expert: turbulence_expert = turbulence_expert
    """
    turbulence_expert child of viscous.
    """
    geko_options: geko_options = geko_options
    """
    geko_options child of viscous.
    """
    transition_model_options: transition_model_options = transition_model_options
    """
    transition_model_options child of viscous.
    """
    transition_sst_option: transition_sst_option = transition_sst_option
    """
    transition_sst_option child of viscous.
    """
    user_defined: user_defined = user_defined
    """
    user_defined child of viscous.
    """
    sa_enhanced_wall_treatment: sa_enhanced_wall_treatment = sa_enhanced_wall_treatment
    """
    sa_enhanced_wall_treatment child of viscous.
    """
    sa_damping: sa_damping = sa_damping
    """
    sa_damping child of viscous.
    """
