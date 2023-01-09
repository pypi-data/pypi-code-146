#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .pressure_inlet_child import pressure_inlet_child

class pressure_inlet(NamedObject[pressure_inlet_child], _NonCreatableNamedObjectMixin[pressure_inlet_child]):
    """
    'pressure_inlet' child.
    """

    fluent_name = "pressure-inlet"

    child_object_type: pressure_inlet_child = pressure_inlet_child
    """
    child_object_type of pressure_inlet.
    """
