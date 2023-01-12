#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .parts import parts
from .list_topology import list_topology
class geometry(Group):
    """
    'geometry' child.
    """

    fluent_name = "geometry"

    child_names = \
        ['parts']

    parts: parts = parts
    """
    parts child of geometry.
    """
    command_names = \
        ['list_topology']

    list_topology: list_topology = list_topology
    """
    list_topology command of geometry.
    """
