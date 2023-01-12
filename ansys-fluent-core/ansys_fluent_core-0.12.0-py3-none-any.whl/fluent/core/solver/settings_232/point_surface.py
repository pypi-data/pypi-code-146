#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .point_surface_child import point_surface_child

class point_surface(NamedObject[point_surface_child], _CreatableNamedObjectMixin[point_surface_child]):
    """
    'point_surface' child.
    """

    fluent_name = "point-surface"

    child_object_type: point_surface_child = point_surface_child
    """
    child_object_type of point_surface.
    """
