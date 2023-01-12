#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .child_object_type_child import child_object_type_child

class component_of_radiation_direction(ListObject[child_object_type_child]):
    """
    'component_of_radiation_direction' child.
    """

    fluent_name = "component-of-radiation-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of component_of_radiation_direction.
    """
