#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .bodies_child import bodies_child

class bodies(NamedObject[bodies_child], _CreatableNamedObjectMixin[bodies_child]):
    """
    'bodies' child.
    """

    fluent_name = "bodies"

    child_object_type: bodies_child = bodies_child
    """
    child_object_type of bodies.
    """
