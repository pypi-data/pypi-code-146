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
from .vector_child import vector_child

class vector(NamedObject[vector_child], _CreatableNamedObjectMixin[vector_child]):
    """
    'vector' child.
    """

    fluent_name = "vector"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of vector.
    """
    copy: copy = copy
    """
    copy command of vector.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of vector.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of vector.
    """
    child_object_type: vector_child = vector_child
    """
    child_object_type of vector.
    """
