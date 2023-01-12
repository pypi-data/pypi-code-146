#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .center import center
from .radius import radius
from .inside import inside
from .create_volume_surface import create_volume_surface
class sphere(Group):
    """
    'sphere' child.
    """

    fluent_name = "sphere"

    child_names = \
        ['center', 'radius', 'inside', 'create_volume_surface']

    center: center = center
    """
    center child of sphere.
    """
    radius: radius = radius
    """
    radius child of sphere.
    """
    inside: inside = inside
    """
    inside child of sphere.
    """
    create_volume_surface: create_volume_surface = create_volume_surface
    """
    create_volume_surface child of sphere.
    """
