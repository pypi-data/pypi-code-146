#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .phase_14 import phase
from .geom_disable import geom_disable
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_levels import geom_levels
from .geom_bgthread import geom_bgthread
from .angular import angular
from .p_jump import p_jump
from .ai import ai
from .aj import aj
from .ak import ak
from .x_origin import x_origin
from .y_origin import y_origin
from .z_origin import z_origin
from .shift_x import shift_x
from .shift_y import shift_y
from .shift_z import shift_z
from .per_angle import per_angle
class periodic_child(Group):
    """
    'child_object_type' of periodic.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'angular', 'p_jump',
         'ai', 'aj', 'ak', 'x_origin', 'y_origin', 'z_origin', 'shift_x',
         'shift_y', 'shift_z', 'per_angle']

    phase: phase = phase
    """
    phase child of periodic_child.
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of periodic_child.
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of periodic_child.
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of periodic_child.
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of periodic_child.
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of periodic_child.
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of periodic_child.
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of periodic_child.
    """
    angular: angular = angular
    """
    angular child of periodic_child.
    """
    p_jump: p_jump = p_jump
    """
    p_jump child of periodic_child.
    """
    ai: ai = ai
    """
    ai child of periodic_child.
    """
    aj: aj = aj
    """
    aj child of periodic_child.
    """
    ak: ak = ak
    """
    ak child of periodic_child.
    """
    x_origin: x_origin = x_origin
    """
    x_origin child of periodic_child.
    """
    y_origin: y_origin = y_origin
    """
    y_origin child of periodic_child.
    """
    z_origin: z_origin = z_origin
    """
    z_origin child of periodic_child.
    """
    shift_x: shift_x = shift_x
    """
    shift_x child of periodic_child.
    """
    shift_y: shift_y = shift_y
    """
    shift_y child of periodic_child.
    """
    shift_z: shift_z = shift_z
    """
    shift_z child of periodic_child.
    """
    per_angle: per_angle = per_angle
    """
    per_angle child of periodic_child.
    """
