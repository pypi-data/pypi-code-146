#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axis_direction_child import axis_direction_child

class input_parameters(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    Input Parameter Values of Design Point.
    """

    fluent_name = "input-parameters"

    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of input_parameters.
    """
