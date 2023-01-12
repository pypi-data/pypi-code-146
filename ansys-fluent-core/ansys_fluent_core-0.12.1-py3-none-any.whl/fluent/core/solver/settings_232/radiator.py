#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .radiator_child import radiator_child

class radiator(NamedObject[radiator_child], _NonCreatableNamedObjectMixin[radiator_child]):
    """
    'radiator' child.
    """

    fluent_name = "radiator"

    child_object_type: radiator_child = radiator_child
    """
    child_object_type of radiator.
    """
