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
from .lic_child import lic_child

class lic(NamedObject[lic_child], _CreatableNamedObjectMixin[lic_child]):
    """
    'lic' child.
    """

    fluent_name = "lic"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of lic.
    """
    copy: copy = copy
    """
    copy command of lic.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of lic.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of lic.
    """
    child_object_type: lic_child = lic_child
    """
    child_object_type of lic.
    """
