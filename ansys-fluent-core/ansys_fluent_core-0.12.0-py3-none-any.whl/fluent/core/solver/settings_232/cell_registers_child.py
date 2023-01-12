#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .python_name import python_name
from .type_2 import type
from .display_options import display_options
class cell_registers_child(Group):
    """
    'child_object_type' of cell_registers.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'python_name', 'type', 'display_options']

    name: name = name
    """
    name child of cell_registers_child.
    """
    python_name: python_name = python_name
    """
    python_name child of cell_registers_child.
    """
    type: type = type
    """
    type child of cell_registers_child.
    """
    display_options: display_options = display_options
    """
    display_options child of cell_registers_child.
    """
