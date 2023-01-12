#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axis_direction_child import axis_direction_child

class film_velocity(ListObject[axis_direction_child]):
    """
    'film_velocity' child.
    """

    fluent_name = "film-velocity"

    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of film_velocity.
    """
