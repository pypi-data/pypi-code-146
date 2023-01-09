#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .change_type import change_type
from .interface_child import interface_child

class interface(NamedObject[interface_child], _CreatableNamedObjectMixin[interface_child]):
    """
    'interface' child.
    """

    fluent_name = "interface"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of interface.
    """
    child_object_type: interface_child = interface_child
    """
    child_object_type of interface.
    """
