#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .child_object_type_child import child_object_type_child

class flow_direction_component(ListObject[child_object_type_child]):
    """
    'flow_direction_component' child.
    """

    fluent_name = "flow-direction-component"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of flow_direction_component.
    """
