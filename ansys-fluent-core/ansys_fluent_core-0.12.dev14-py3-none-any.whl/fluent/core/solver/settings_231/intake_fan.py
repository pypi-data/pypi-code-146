#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .intake_fan_child import intake_fan_child

class intake_fan(NamedObject[intake_fan_child], _NonCreatableNamedObjectMixin[intake_fan_child]):
    """
    'intake_fan' child.
    """

    fluent_name = "intake-fan"

    child_object_type: intake_fan_child = intake_fan_child
    """
    child_object_type of intake_fan.
    """
