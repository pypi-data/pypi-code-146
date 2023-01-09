#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sc_def_file_settings import sc_def_file_settings
from .settings import settings
from .abaqus import abaqus
from .mechanical_apdl import mechanical_apdl
from .mechanical_apdl_input import mechanical_apdl_input
from .custom_heat_flux import custom_heat_flux
from .icemcfd_for_icepak import icemcfd_for_icepak
from .fast_mesh import fast_mesh
from .fast_solution import fast_solution
from .fast_velocity import fast_velocity
from .taitherm import taitherm
class export(Group):
    """
    'export' child.
    """

    fluent_name = "export"

    child_names = \
        ['sc_def_file_settings', 'settings']

    sc_def_file_settings: sc_def_file_settings = sc_def_file_settings
    """
    sc_def_file_settings child of export.
    """
    settings: settings = settings
    """
    settings child of export.
    """
    command_names = \
        ['abaqus', 'mechanical_apdl', 'mechanical_apdl_input',
         'custom_heat_flux', 'icemcfd_for_icepak', 'fast_mesh',
         'fast_solution', 'fast_velocity', 'taitherm']

    abaqus: abaqus = abaqus
    """
    abaqus command of export.
    """
    mechanical_apdl: mechanical_apdl = mechanical_apdl
    """
    mechanical_apdl command of export.
    """
    mechanical_apdl_input: mechanical_apdl_input = mechanical_apdl_input
    """
    mechanical_apdl_input command of export.
    """
    custom_heat_flux: custom_heat_flux = custom_heat_flux
    """
    custom_heat_flux command of export.
    """
    icemcfd_for_icepak: icemcfd_for_icepak = icemcfd_for_icepak
    """
    icemcfd_for_icepak command of export.
    """
    fast_mesh: fast_mesh = fast_mesh
    """
    fast_mesh command of export.
    """
    fast_solution: fast_solution = fast_solution
    """
    fast_solution command of export.
    """
    fast_velocity: fast_velocity = fast_velocity
    """
    fast_velocity command of export.
    """
    taitherm: taitherm = taitherm
    """
    taitherm command of export.
    """
