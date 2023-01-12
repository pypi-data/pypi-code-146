#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .pressure_outlet_child import pressure_outlet_child

class pressure_outlet(NamedObject[pressure_outlet_child], _NonCreatableNamedObjectMixin[pressure_outlet_child]):
    """
    'pressure_outlet' child.
    """

    fluent_name = "pressure-outlet"

    child_object_type: pressure_outlet_child = pressure_outlet_child
    """
    child_object_type of pressure_outlet.
    """
