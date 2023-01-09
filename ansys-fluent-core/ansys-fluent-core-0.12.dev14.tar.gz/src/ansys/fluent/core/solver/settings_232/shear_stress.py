#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .child_object_type_child_1 import child_object_type_child

class shear_stress(ListObject[child_object_type_child]):
    """
    'shear_stress' child.
    """

    fluent_name = "shear-stress"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of shear_stress.
    """
