#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .child_object_type_child_1 import child_object_type_child

class mass_flow_multiplier(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'mass_flow_multiplier' child.
    """

    fluent_name = "mass-flow-multiplier"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of mass_flow_multiplier.
    """
