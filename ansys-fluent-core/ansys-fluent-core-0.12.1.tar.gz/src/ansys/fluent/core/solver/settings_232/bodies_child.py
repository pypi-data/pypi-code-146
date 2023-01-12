#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .faces import faces
from .list_properties_2 import list_properties
class bodies_child(Group):
    """
    'child_object_type' of bodies.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['faces']

    faces: faces = faces
    """
    faces child of bodies_child.
    """
    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of bodies_child.
    """
