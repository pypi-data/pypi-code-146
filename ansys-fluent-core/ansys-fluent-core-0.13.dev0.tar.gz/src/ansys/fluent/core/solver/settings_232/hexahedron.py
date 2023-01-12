#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .min_point import min_point
from .max_point import max_point
from .inside import inside
from .create_volume_surface import create_volume_surface
class hexahedron(Group):
    """
    'hexahedron' child.
    """

    fluent_name = "hexahedron"

    child_names = \
        ['min_point', 'max_point', 'inside', 'create_volume_surface']

    min_point: min_point = min_point
    """
    min_point child of hexahedron.
    """
    max_point: max_point = max_point
    """
    max_point child of hexahedron.
    """
    inside: inside = inside
    """
    inside child of hexahedron.
    """
    create_volume_surface: create_volume_surface = create_volume_surface
    """
    create_volume_surface child of hexahedron.
    """
