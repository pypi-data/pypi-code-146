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
from .scene_child import scene_child

class scene(NamedObject[scene_child], _CreatableNamedObjectMixin[scene_child]):
    """
    'scene' child.
    """

    fluent_name = "scene"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of scene.
    """
    copy: copy = copy
    """
    copy command of scene.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of scene.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of scene.
    """
    child_object_type: scene_child = scene_child
    """
    child_object_type of scene.
    """
