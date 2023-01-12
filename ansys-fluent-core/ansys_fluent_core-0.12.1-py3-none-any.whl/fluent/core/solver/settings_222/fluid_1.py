#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .change_type import change_type
from .fluid_child_1 import fluid_child

class fluid(NamedObject[fluid_child], _CreatableNamedObjectMixin[fluid_child]):
    """
    'fluid' child.
    """

    fluent_name = "fluid"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of fluid.
    """
    child_object_type: fluid_child = fluid_child
    """
    child_object_type of fluid.
    """
