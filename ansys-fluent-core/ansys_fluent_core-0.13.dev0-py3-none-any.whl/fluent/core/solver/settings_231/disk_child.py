#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .general_1 import general
from .geometry_1 import geometry
from .trimming import trimming
class disk_child(Group):
    """
    'child_object_type' of disk.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['general', 'geometry', 'trimming']

    general: general = general
    """
    general child of disk_child.
    """
    geometry: geometry = geometry
    """
    geometry child of disk_child.
    """
    trimming: trimming = trimming
    """
    trimming child of disk_child.
    """
