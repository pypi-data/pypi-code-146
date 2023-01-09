#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .point_surface import point_surface
from .plane_surface import plane_surface
class surfaces(Group):
    """
    'surfaces' child.
    """

    fluent_name = "surfaces"

    child_names = \
        ['point_surface', 'plane_surface']

    point_surface: point_surface = point_surface
    """
    point_surface child of surfaces.
    """
    plane_surface: plane_surface = plane_surface
    """
    plane_surface child of surfaces.
    """
