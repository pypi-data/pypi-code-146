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
from .pathline_child import pathline_child

class pathline(NamedObject[pathline_child], _CreatableNamedObjectMixin[pathline_child]):
    """
    'pathline' child.
    """

    fluent_name = "pathline"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of pathline.
    """
    copy: copy = copy
    """
    copy command of pathline.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of pathline.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of pathline.
    """
    child_object_type: pathline_child = pathline_child
    """
    child_object_type of pathline.
    """
