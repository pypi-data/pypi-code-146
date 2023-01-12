#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fluid_child import fluid_child

class solid(NamedObject[fluid_child], _CreatableNamedObjectMixin[fluid_child]):
    """
    'solid' child.
    """

    fluent_name = "solid"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of solid.
    """
