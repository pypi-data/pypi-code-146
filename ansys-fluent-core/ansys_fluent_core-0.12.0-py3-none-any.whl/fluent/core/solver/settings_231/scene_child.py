#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .title import title
from .temporary import temporary
from .graphics_objects import graphics_objects
from .display_state_name import display_state_name
from .display_2 import display
class scene_child(Group):
    """
    'child_object_type' of scene.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'title', 'temporary', 'graphics_objects',
         'display_state_name']

    name: name = name
    """
    name child of scene_child.
    """
    title: title = title
    """
    title child of scene_child.
    """
    temporary: temporary = temporary
    """
    temporary child of scene_child.
    """
    graphics_objects: graphics_objects = graphics_objects
    """
    graphics_objects child of scene_child.
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of scene_child.
    """
    command_names = \
        ['display']

    display: display = display
    """
    display command of scene_child.
    """
