#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axis_begin import axis_begin
from .axis_end import axis_end
from .radius import radius
from .inside import inside
from .create_volume_surface import create_volume_surface
class cylinder(Group):
    """
    'cylinder' child.
    """

    fluent_name = "cylinder"

    child_names = \
        ['axis_begin', 'axis_end', 'radius', 'inside',
         'create_volume_surface']

    axis_begin: axis_begin = axis_begin
    """
    axis_begin child of cylinder.
    """
    axis_end: axis_end = axis_end
    """
    axis_end child of cylinder.
    """
    radius: radius = radius
    """
    radius child of cylinder.
    """
    inside: inside = inside
    """
    inside child of cylinder.
    """
    create_volume_surface: create_volume_surface = create_volume_surface
    """
    create_volume_surface child of cylinder.
    """
