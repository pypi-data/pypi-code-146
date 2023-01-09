#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .formulation import formulation
from .relaxation_method_1 import relaxation_method
from .convergence_acceleration_for_stretched_meshes_1 import convergence_acceleration_for_stretched_meshes
from .relaxation_bounds import relaxation_bounds
class pseudo_time_method(Group):
    """
    Enter the pseudo time method menu.
    """

    fluent_name = "pseudo-time-method"

    child_names = \
        ['formulation', 'relaxation_method',
         'convergence_acceleration_for_stretched_meshes']

    formulation: formulation = formulation
    """
    formulation child of pseudo_time_method.
    """
    relaxation_method: relaxation_method = relaxation_method
    """
    relaxation_method child of pseudo_time_method.
    """
    convergence_acceleration_for_stretched_meshes: convergence_acceleration_for_stretched_meshes = convergence_acceleration_for_stretched_meshes
    """
    convergence_acceleration_for_stretched_meshes child of pseudo_time_method.
    """
    command_names = \
        ['relaxation_bounds']

    relaxation_bounds: relaxation_bounds = relaxation_bounds
    """
    relaxation_bounds command of pseudo_time_method.
    """
