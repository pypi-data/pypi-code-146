#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .subgrid_scale_turb_visc import subgrid_scale_turb_visc
from .turb_visc_func_mf import turb_visc_func_mf
from .turb_visc_func import turb_visc_func
from .tke_prandtl import tke_prandtl
from .tdr_prandtl import tdr_prandtl
from .sdr_prandtl import sdr_prandtl
from .energy_prandtl import energy_prandtl
from .wall_prandtl import wall_prandtl
from .turbulent_schmidt import turbulent_schmidt
class user_defined(Group):
    """
    'user_defined' child.
    """

    fluent_name = "user-defined"

    child_names = \
        ['subgrid_scale_turb_visc', 'turb_visc_func_mf', 'turb_visc_func',
         'tke_prandtl', 'tdr_prandtl', 'sdr_prandtl', 'energy_prandtl',
         'wall_prandtl', 'turbulent_schmidt']

    subgrid_scale_turb_visc: subgrid_scale_turb_visc = subgrid_scale_turb_visc
    """
    subgrid_scale_turb_visc child of user_defined.
    """
    turb_visc_func_mf: turb_visc_func_mf = turb_visc_func_mf
    """
    turb_visc_func_mf child of user_defined.
    """
    turb_visc_func: turb_visc_func = turb_visc_func
    """
    turb_visc_func child of user_defined.
    """
    tke_prandtl: tke_prandtl = tke_prandtl
    """
    tke_prandtl child of user_defined.
    """
    tdr_prandtl: tdr_prandtl = tdr_prandtl
    """
    tdr_prandtl child of user_defined.
    """
    sdr_prandtl: sdr_prandtl = sdr_prandtl
    """
    sdr_prandtl child of user_defined.
    """
    energy_prandtl: energy_prandtl = energy_prandtl
    """
    energy_prandtl child of user_defined.
    """
    wall_prandtl: wall_prandtl = wall_prandtl
    """
    wall_prandtl child of user_defined.
    """
    turbulent_schmidt: turbulent_schmidt = turbulent_schmidt
    """
    turbulent_schmidt child of user_defined.
    """
