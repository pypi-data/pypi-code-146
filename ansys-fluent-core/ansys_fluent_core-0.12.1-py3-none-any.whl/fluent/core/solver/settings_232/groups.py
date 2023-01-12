#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .faces_child import faces_child

class groups(NamedObject[faces_child], _CreatableNamedObjectMixin[faces_child]):
    """
    'groups' child.
    """

    fluent_name = "groups"

    child_object_type: faces_child = faces_child
    """
    child_object_type of groups.
    """
