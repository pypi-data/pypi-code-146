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
from .contour_child import contour_child

class contour(NamedObject[contour_child], _CreatableNamedObjectMixin[contour_child]):
    """
    'contour' child.
    """

    fluent_name = "contour"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of contour.
    """
    copy: copy = copy
    """
    copy command of contour.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of contour.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of contour.
    """
    child_object_type: contour_child = contour_child
    """
    child_object_type of contour.
    """
