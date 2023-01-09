#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axis_child import axis_child

class degassing(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'degassing' child.
    """

    fluent_name = "degassing"

    child_object_type: axis_child = axis_child
    """
    child_object_type of degassing.
    """
