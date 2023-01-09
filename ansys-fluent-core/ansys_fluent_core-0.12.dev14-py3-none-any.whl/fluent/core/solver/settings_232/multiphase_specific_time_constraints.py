#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .moving_mesh_cfl_constraint import moving_mesh_cfl_constraint
from .physics_based_constraint import physics_based_constraint
from .time_scale_options import time_scale_options
from .verbosity_7 import verbosity
class multiphase_specific_time_constraints(Group):
    """
    'multiphase_specific_time_constraints' child.
    """

    fluent_name = "multiphase-specific-time-constraints"

    child_names = \
        ['moving_mesh_cfl_constraint', 'physics_based_constraint',
         'time_scale_options', 'verbosity']

    moving_mesh_cfl_constraint: moving_mesh_cfl_constraint = moving_mesh_cfl_constraint
    """
    moving_mesh_cfl_constraint child of multiphase_specific_time_constraints.
    """
    physics_based_constraint: physics_based_constraint = physics_based_constraint
    """
    physics_based_constraint child of multiphase_specific_time_constraints.
    """
    time_scale_options: time_scale_options = time_scale_options
    """
    time_scale_options child of multiphase_specific_time_constraints.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of multiphase_specific_time_constraints.
    """
