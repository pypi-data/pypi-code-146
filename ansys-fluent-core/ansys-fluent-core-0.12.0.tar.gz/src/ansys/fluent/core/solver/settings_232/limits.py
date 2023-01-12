#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .min_pressure import min_pressure
from .max_pressure import max_pressure
from .min_temperature import min_temperature
from .max_temperature import max_temperature
from .min_tke import min_tke
from .min_lam_tke import min_lam_tke
from .min_des_tke import min_des_tke
from .min_epsilon import min_epsilon
from .min_des_epsilon import min_des_epsilon
from .min_v2f_tke import min_v2f_tke
from .min_v2f_epsilon import min_v2f_epsilon
from .min_vel_var_scale import min_vel_var_scale
from .min_elliptic_relax_func import min_elliptic_relax_func
from .min_omega import min_omega
from .min_des_omega import min_des_omega
from .max_turb_visc_ratio import max_turb_visc_ratio
from .positivity_rate import positivity_rate
from .min_vol_frac_for_matrix_sol import min_vol_frac_for_matrix_sol
class limits(Group):
    """
    'limits' child.
    """

    fluent_name = "limits"

    child_names = \
        ['min_pressure', 'max_pressure', 'min_temperature', 'max_temperature',
         'min_tke', 'min_lam_tke', 'min_des_tke', 'min_epsilon',
         'min_des_epsilon', 'min_v2f_tke', 'min_v2f_epsilon',
         'min_vel_var_scale', 'min_elliptic_relax_func', 'min_omega',
         'min_des_omega', 'max_turb_visc_ratio', 'positivity_rate',
         'min_vol_frac_for_matrix_sol']

    min_pressure: min_pressure = min_pressure
    """
    min_pressure child of limits.
    """
    max_pressure: max_pressure = max_pressure
    """
    max_pressure child of limits.
    """
    min_temperature: min_temperature = min_temperature
    """
    min_temperature child of limits.
    """
    max_temperature: max_temperature = max_temperature
    """
    max_temperature child of limits.
    """
    min_tke: min_tke = min_tke
    """
    min_tke child of limits.
    """
    min_lam_tke: min_lam_tke = min_lam_tke
    """
    min_lam_tke child of limits.
    """
    min_des_tke: min_des_tke = min_des_tke
    """
    min_des_tke child of limits.
    """
    min_epsilon: min_epsilon = min_epsilon
    """
    min_epsilon child of limits.
    """
    min_des_epsilon: min_des_epsilon = min_des_epsilon
    """
    min_des_epsilon child of limits.
    """
    min_v2f_tke: min_v2f_tke = min_v2f_tke
    """
    min_v2f_tke child of limits.
    """
    min_v2f_epsilon: min_v2f_epsilon = min_v2f_epsilon
    """
    min_v2f_epsilon child of limits.
    """
    min_vel_var_scale: min_vel_var_scale = min_vel_var_scale
    """
    min_vel_var_scale child of limits.
    """
    min_elliptic_relax_func: min_elliptic_relax_func = min_elliptic_relax_func
    """
    min_elliptic_relax_func child of limits.
    """
    min_omega: min_omega = min_omega
    """
    min_omega child of limits.
    """
    min_des_omega: min_des_omega = min_des_omega
    """
    min_des_omega child of limits.
    """
    max_turb_visc_ratio: max_turb_visc_ratio = max_turb_visc_ratio
    """
    max_turb_visc_ratio child of limits.
    """
    positivity_rate: positivity_rate = positivity_rate
    """
    positivity_rate child of limits.
    """
    min_vol_frac_for_matrix_sol: min_vol_frac_for_matrix_sol = min_vol_frac_for_matrix_sol
    """
    min_vol_frac_for_matrix_sol child of limits.
    """
