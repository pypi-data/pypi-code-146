#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .convergence_acceleration_type import convergence_acceleration_type
from .casm_cutoff_multiplier_1 import casm_cutoff_multiplier
class convergence_acceleration_for_stretched_meshes(Group):
    """
    Enable convergence acceleration for stretched meshes to improve the convergence of the implicit pressure based solver on meshes with high cell stretching.
    """

    fluent_name = "convergence-acceleration-for-stretched-meshes"

    child_names = \
        ['convergence_acceleration_type', 'casm_cutoff_multiplier']

    convergence_acceleration_type: convergence_acceleration_type = convergence_acceleration_type
    """
    convergence_acceleration_type child of convergence_acceleration_for_stretched_meshes.
    """
    casm_cutoff_multiplier: casm_cutoff_multiplier = casm_cutoff_multiplier
    """
    casm_cutoff_multiplier child of convergence_acceleration_for_stretched_meshes.
    """
