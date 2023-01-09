#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .low_re_ke import low_re_ke
from .low_re_ke_index import low_re_ke_index
from .kato_launder_model import kato_launder_model
from .production_limiter import production_limiter
from .kw_vorticity_based_production import kw_vorticity_based_production
from .kw_add_sas import kw_add_sas
from .kw_add_des import kw_add_des
from .turb_add_sbes_sdes import turb_add_sbes_sdes
from .sbes_sdes_hybrid_model import sbes_sdes_hybrid_model
from .sbes_update_interval_k_omega import sbes_update_interval_k_omega
from .sbes_sgs_option import sbes_sgs_option
from .sbes_les_subgrid_dynamic_fvar import sbes_les_subgrid_dynamic_fvar
from .turbulence_damping import turbulence_damping
from .rke_cmu_rotation_term import rke_cmu_rotation_term
from .turb_non_newtonian import turb_non_newtonian
from .non_newtonian_modification import non_newtonian_modification
from .turb_pk_compressible import turb_pk_compressible
from .thermal_p_function import thermal_p_function
from .restore_sst_v61 import restore_sst_v61
class turbulence_expert(Group):
    """
    'turbulence_expert' child.
    """

    fluent_name = "turbulence-expert"

    child_names = \
        ['low_re_ke', 'low_re_ke_index', 'kato_launder_model',
         'production_limiter', 'kw_vorticity_based_production', 'kw_add_sas',
         'kw_add_des', 'turb_add_sbes_sdes', 'sbes_sdes_hybrid_model',
         'sbes_update_interval_k_omega', 'sbes_sgs_option',
         'sbes_les_subgrid_dynamic_fvar', 'turbulence_damping',
         'rke_cmu_rotation_term', 'turb_non_newtonian',
         'non_newtonian_modification', 'turb_pk_compressible',
         'thermal_p_function', 'restore_sst_v61']

    low_re_ke: low_re_ke = low_re_ke
    """
    low_re_ke child of turbulence_expert.
    """
    low_re_ke_index: low_re_ke_index = low_re_ke_index
    """
    low_re_ke_index child of turbulence_expert.
    """
    kato_launder_model: kato_launder_model = kato_launder_model
    """
    kato_launder_model child of turbulence_expert.
    """
    production_limiter: production_limiter = production_limiter
    """
    production_limiter child of turbulence_expert.
    """
    kw_vorticity_based_production: kw_vorticity_based_production = kw_vorticity_based_production
    """
    kw_vorticity_based_production child of turbulence_expert.
    """
    kw_add_sas: kw_add_sas = kw_add_sas
    """
    kw_add_sas child of turbulence_expert.
    """
    kw_add_des: kw_add_des = kw_add_des
    """
    kw_add_des child of turbulence_expert.
    """
    turb_add_sbes_sdes: turb_add_sbes_sdes = turb_add_sbes_sdes
    """
    turb_add_sbes_sdes child of turbulence_expert.
    """
    sbes_sdes_hybrid_model: sbes_sdes_hybrid_model = sbes_sdes_hybrid_model
    """
    sbes_sdes_hybrid_model child of turbulence_expert.
    """
    sbes_update_interval_k_omega: sbes_update_interval_k_omega = sbes_update_interval_k_omega
    """
    sbes_update_interval_k_omega child of turbulence_expert.
    """
    sbes_sgs_option: sbes_sgs_option = sbes_sgs_option
    """
    sbes_sgs_option child of turbulence_expert.
    """
    sbes_les_subgrid_dynamic_fvar: sbes_les_subgrid_dynamic_fvar = sbes_les_subgrid_dynamic_fvar
    """
    sbes_les_subgrid_dynamic_fvar child of turbulence_expert.
    """
    turbulence_damping: turbulence_damping = turbulence_damping
    """
    turbulence_damping child of turbulence_expert.
    """
    rke_cmu_rotation_term: rke_cmu_rotation_term = rke_cmu_rotation_term
    """
    rke_cmu_rotation_term child of turbulence_expert.
    """
    turb_non_newtonian: turb_non_newtonian = turb_non_newtonian
    """
    turb_non_newtonian child of turbulence_expert.
    """
    non_newtonian_modification: non_newtonian_modification = non_newtonian_modification
    """
    non_newtonian_modification child of turbulence_expert.
    """
    turb_pk_compressible: turb_pk_compressible = turb_pk_compressible
    """
    turb_pk_compressible child of turbulence_expert.
    """
    thermal_p_function: thermal_p_function = thermal_p_function
    """
    thermal_p_function child of turbulence_expert.
    """
    restore_sst_v61: restore_sst_v61 = restore_sst_v61
    """
    restore_sst_v61 child of turbulence_expert.
    """
