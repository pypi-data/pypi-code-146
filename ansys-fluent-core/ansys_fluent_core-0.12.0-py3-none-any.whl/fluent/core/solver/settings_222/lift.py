#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .lift_child import lift_child

class lift(NamedObject[lift_child], _CreatableNamedObjectMixin[lift_child]):
    """
    'lift' child.
    """

    fluent_name = "lift"

    child_object_type: lift_child = lift_child
    """
    child_object_type of lift.
    """
