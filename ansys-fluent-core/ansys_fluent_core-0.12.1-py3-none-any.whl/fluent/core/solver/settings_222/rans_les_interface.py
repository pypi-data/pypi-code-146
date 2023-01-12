#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .change_type import change_type
from .rans_les_interface_child import rans_les_interface_child

class rans_les_interface(NamedObject[rans_les_interface_child], _CreatableNamedObjectMixin[rans_les_interface_child]):
    """
    'rans_les_interface' child.
    """

    fluent_name = "rans-les-interface"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of rans_les_interface.
    """
    child_object_type: rans_les_interface_child = rans_les_interface_child
    """
    child_object_type of rans_les_interface.
    """
