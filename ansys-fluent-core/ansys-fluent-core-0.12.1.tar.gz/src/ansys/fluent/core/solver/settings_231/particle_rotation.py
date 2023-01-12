#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable import enable
from .drag_law import drag_law
from .lift_law import lift_law
class particle_rotation(Group):
    """
    'particle_rotation' child.
    """

    fluent_name = "particle-rotation"

    child_names = \
        ['enable', 'drag_law', 'lift_law']

    enable: enable = enable
    """
    enable child of particle_rotation.
    """
    drag_law: drag_law = drag_law
    """
    drag_law child of particle_rotation.
    """
    lift_law: lift_law = lift_law
    """
    lift_law child of particle_rotation.
    """
