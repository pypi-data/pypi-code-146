#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .porous_jump_child import porous_jump_child

class porous_jump(NamedObject[porous_jump_child], _NonCreatableNamedObjectMixin[porous_jump_child]):
    """
    'porous_jump' child.
    """

    fluent_name = "porous-jump"

    child_object_type: porous_jump_child = porous_jump_child
    """
    child_object_type of porous_jump.
    """
