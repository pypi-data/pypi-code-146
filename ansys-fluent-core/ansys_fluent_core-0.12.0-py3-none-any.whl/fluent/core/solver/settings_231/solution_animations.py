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
from .solution_animations_child import solution_animations_child

class solution_animations(NamedObject[solution_animations_child], _CreatableNamedObjectMixin[solution_animations_child]):
    """
    'solution_animations' child.
    """

    fluent_name = "solution-animations"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of solution_animations.
    """
    copy: copy = copy
    """
    copy command of solution_animations.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of solution_animations.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of solution_animations.
    """
    child_object_type: solution_animations_child = solution_animations_child
    """
    child_object_type of solution_animations.
    """
