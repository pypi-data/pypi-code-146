#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .cell_registers_child import cell_registers_child

class cell_registers(NamedObject[cell_registers_child], _CreatableNamedObjectMixin[cell_registers_child]):
    """
    'cell_registers' child.
    """

    fluent_name = "cell-registers"

    child_object_type: cell_registers_child = cell_registers_child
    """
    child_object_type of cell_registers.
    """
