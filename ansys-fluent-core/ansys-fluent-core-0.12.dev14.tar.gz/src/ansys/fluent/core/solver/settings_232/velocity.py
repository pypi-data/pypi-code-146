#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .x_velocity import x_velocity
from .x_velocity_2 import x_velocity_2
from .y_velocity import y_velocity
from .y_velocity_2 import y_velocity_2
from .z_velocity import z_velocity
from .z_velocity_2 import z_velocity_2
from .magnitude import magnitude
from .swirl_fraction import swirl_fraction
from .use_face_normal_direction import use_face_normal_direction
class velocity(Group):
    """
    'velocity' child.
    """

    fluent_name = "velocity"

    child_names = \
        ['x_velocity', 'x_velocity_2', 'y_velocity', 'y_velocity_2',
         'z_velocity', 'z_velocity_2', 'magnitude', 'swirl_fraction',
         'use_face_normal_direction']

    x_velocity: x_velocity = x_velocity
    """
    x_velocity child of velocity.
    """
    x_velocity_2: x_velocity_2 = x_velocity_2
    """
    x_velocity_2 child of velocity.
    """
    y_velocity: y_velocity = y_velocity
    """
    y_velocity child of velocity.
    """
    y_velocity_2: y_velocity_2 = y_velocity_2
    """
    y_velocity_2 child of velocity.
    """
    z_velocity: z_velocity = z_velocity
    """
    z_velocity child of velocity.
    """
    z_velocity_2: z_velocity_2 = z_velocity_2
    """
    z_velocity_2 child of velocity.
    """
    magnitude: magnitude = magnitude
    """
    magnitude child of velocity.
    """
    swirl_fraction: swirl_fraction = swirl_fraction
    """
    swirl_fraction child of velocity.
    """
    use_face_normal_direction: use_face_normal_direction = use_face_normal_direction
    """
    use_face_normal_direction child of velocity.
    """
