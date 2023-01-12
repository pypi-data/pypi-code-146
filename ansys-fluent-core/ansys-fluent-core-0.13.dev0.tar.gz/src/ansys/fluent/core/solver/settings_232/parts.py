#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .parts_child import parts_child

class parts(NamedObject[parts_child], _CreatableNamedObjectMixin[parts_child]):
    """
    'parts' child.
    """

    fluent_name = "parts"

    child_object_type: parts_child = parts_child
    """
    child_object_type of parts.
    """
