#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axis_direction_child import axis_direction_child

class phase_based_vof_discretization(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    'phase_based_vof_discretization' child.
    """

    fluent_name = "phase-based-vof-discretization"

    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of phase_based_vof_discretization.
    """
