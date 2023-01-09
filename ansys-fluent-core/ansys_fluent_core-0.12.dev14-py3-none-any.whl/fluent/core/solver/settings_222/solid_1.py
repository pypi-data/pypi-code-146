#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .change_type import change_type
from .solid_child import solid_child

class solid(NamedObject[solid_child], _CreatableNamedObjectMixin[solid_child]):
    """
    'solid' child.
    """

    fluent_name = "solid"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of solid.
    """
    child_object_type: solid_child = solid_child
    """
    child_object_type of solid.
    """
