#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .outlet_vent_child import outlet_vent_child

class outlet_vent(NamedObject[outlet_vent_child], _NonCreatableNamedObjectMixin[outlet_vent_child]):
    """
    'outlet_vent' child.
    """

    fluent_name = "outlet-vent"

    child_object_type: outlet_vent_child = outlet_vent_child
    """
    child_object_type of outlet_vent.
    """
