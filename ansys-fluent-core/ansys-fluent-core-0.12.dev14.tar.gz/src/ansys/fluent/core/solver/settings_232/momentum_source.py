#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .child_object_type_child_1 import child_object_type_child

class momentum_source(ListObject[child_object_type_child]):
    """
    'momentum_source' child.
    """

    fluent_name = "momentum-source"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of momentum_source.
    """
