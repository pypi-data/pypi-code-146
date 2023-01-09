#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .reference_frame import reference_frame
from .point import point
from .snap_method import snap_method
class point_surface_child(Group):
    """
    'child_object_type' of point_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['reference_frame', 'point', 'snap_method']

    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of point_surface_child.
    """
    point: point = point
    """
    point child of point_surface_child.
    """
    snap_method: snap_method = snap_method
    """
    snap_method child of point_surface_child.
    """
