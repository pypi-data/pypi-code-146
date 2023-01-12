#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_2 import list_properties
class faces_child(Group):
    """
    'child_object_type' of faces.
    """

    fluent_name = "child-object-type"

    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of faces_child.
    """
