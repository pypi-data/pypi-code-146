#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .ap_face_zone import ap_face_zone
from .beam_length import beam_length
from .ray_points_count import ray_points_count
from .beam_vector import beam_vector
class beams_child(Group):
    """
    'child_object_type' of beams.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['ap_face_zone', 'beam_length', 'ray_points_count', 'beam_vector']

    ap_face_zone: ap_face_zone = ap_face_zone
    """
    ap_face_zone child of beams_child.
    """
    beam_length: beam_length = beam_length
    """
    beam_length child of beams_child.
    """
    ray_points_count: ray_points_count = ray_points_count
    """
    ray_points_count child of beams_child.
    """
    beam_vector: beam_vector = beam_vector
    """
    beam_vector child of beams_child.
    """
