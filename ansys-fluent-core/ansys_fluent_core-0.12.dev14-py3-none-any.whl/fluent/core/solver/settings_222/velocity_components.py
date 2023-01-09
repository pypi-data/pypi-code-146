#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .child_object_type_child import child_object_type_child

class velocity_components(ListObject[child_object_type_child]):
    """
    'velocity_components' child.
    """

    fluent_name = "velocity-components"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of velocity_components.
    """
