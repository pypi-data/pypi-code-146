#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .delete import delete
from .display import display
from .read_2 import read
class surface_mesh(Group):
    """
    Enter the surface mesh menu.
    """

    fluent_name = "surface-mesh"

    command_names = \
        ['delete', 'display', 'read']

    delete: delete = delete
    """
    delete command of surface_mesh.
    """
    display: display = display
    """
    display command of surface_mesh.
    """
    read: read = read
    """
    read command of surface_mesh.
    """
