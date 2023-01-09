#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .display_1 import display
from .copy_3 import copy
from .add_to_graphics import add_to_graphics
from .clear_history import clear_history
from .mesh_child_1 import mesh_child

class mesh(NamedObject[mesh_child], _CreatableNamedObjectMixin[mesh_child]):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of mesh.
    """
    copy: copy = copy
    """
    copy command of mesh.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of mesh.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of mesh.
    """
    child_object_type: mesh_child = mesh_child
    """
    child_object_type of mesh.
    """
