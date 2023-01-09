#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .moving_mesh_constraint import moving_mesh_constraint
from .mesh_courant_number import mesh_courant_number
class moving_mesh_cfl_constraint(Group):
    """
    'moving_mesh_cfl_constraint' child.
    """

    fluent_name = "moving-mesh-cfl-constraint"

    child_names = \
        ['moving_mesh_constraint', 'mesh_courant_number']

    moving_mesh_constraint: moving_mesh_constraint = moving_mesh_constraint
    """
    moving_mesh_constraint child of moving_mesh_cfl_constraint.
    """
    mesh_courant_number: mesh_courant_number = mesh_courant_number
    """
    mesh_courant_number child of moving_mesh_cfl_constraint.
    """
