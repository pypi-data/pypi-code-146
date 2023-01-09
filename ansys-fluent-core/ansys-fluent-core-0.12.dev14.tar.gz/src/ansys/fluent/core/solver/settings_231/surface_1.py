#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .surface_child import surface_child

class surface(NamedObject[surface_child], _CreatableNamedObjectMixin[surface_child]):
    """
    'surface' child.
    """

    fluent_name = "surface"

    child_object_type: surface_child = surface_child
    """
    child_object_type of surface.
    """
