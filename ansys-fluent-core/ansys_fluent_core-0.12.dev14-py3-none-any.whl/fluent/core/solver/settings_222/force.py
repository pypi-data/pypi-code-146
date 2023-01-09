#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .force_child import force_child

class force(NamedObject[force_child], _CreatableNamedObjectMixin[force_child]):
    """
    'force' child.
    """

    fluent_name = "force"

    child_object_type: force_child = force_child
    """
    child_object_type of force.
    """
