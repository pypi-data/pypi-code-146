#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fluid_child_1 import fluid_child

class fluid(NamedObject[fluid_child], _NonCreatableNamedObjectMixin[fluid_child]):
    """
    'fluid' child.
    """

    fluent_name = "fluid"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of fluid.
    """
