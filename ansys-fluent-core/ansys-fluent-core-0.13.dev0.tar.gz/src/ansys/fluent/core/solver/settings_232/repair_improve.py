#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .allow_repair_at_boundaries import allow_repair_at_boundaries
from .include_local_polyhedra_conversion_in_repair import include_local_polyhedra_conversion_in_repair
from .repair_poor_elements import repair_poor_elements
from .improve_quality import improve_quality
from .repair import repair
from .repair_face_handedness import repair_face_handedness
from .repair_face_node_order import repair_face_node_order
from .repair_wall_distance import repair_wall_distance
class repair_improve(Group):
    """
    Enter the repair and improve quality menu.
    """

    fluent_name = "repair-improve"

    child_names = \
        ['allow_repair_at_boundaries',
         'include_local_polyhedra_conversion_in_repair']

    allow_repair_at_boundaries: allow_repair_at_boundaries = allow_repair_at_boundaries
    """
    allow_repair_at_boundaries child of repair_improve.
    """
    include_local_polyhedra_conversion_in_repair: include_local_polyhedra_conversion_in_repair = include_local_polyhedra_conversion_in_repair
    """
    include_local_polyhedra_conversion_in_repair child of repair_improve.
    """
    command_names = \
        ['repair_poor_elements', 'improve_quality', 'repair',
         'repair_face_handedness', 'repair_face_node_order',
         'repair_wall_distance']

    repair_poor_elements: repair_poor_elements = repair_poor_elements
    """
    repair_poor_elements command of repair_improve.
    """
    improve_quality: improve_quality = improve_quality
    """
    improve_quality command of repair_improve.
    """
    repair: repair = repair
    """
    repair command of repair_improve.
    """
    repair_face_handedness: repair_face_handedness = repair_face_handedness
    """
    repair_face_handedness command of repair_improve.
    """
    repair_face_node_order: repair_face_node_order = repair_face_node_order
    """
    repair_face_node_order command of repair_improve.
    """
    repair_wall_distance: repair_wall_distance = repair_wall_distance
    """
    repair_wall_distance command of repair_improve.
    """
