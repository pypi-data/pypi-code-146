#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .child_object_type_child import child_object_type_child

class mf(NamedObject[child_object_type_child], _CreatableNamedObjectMixin[child_object_type_child]):
    """
    'mf' child.
    """

    fluent_name = "mf"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of mf.
    """
