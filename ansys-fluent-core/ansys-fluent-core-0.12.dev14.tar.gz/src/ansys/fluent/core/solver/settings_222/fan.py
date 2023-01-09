#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .change_type import change_type
from .fan_child import fan_child

class fan(NamedObject[fan_child], _CreatableNamedObjectMixin[fan_child]):
    """
    'fan' child.
    """

    fluent_name = "fan"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of fan.
    """
    child_object_type: fan_child = fan_child
    """
    child_object_type of fan.
    """
