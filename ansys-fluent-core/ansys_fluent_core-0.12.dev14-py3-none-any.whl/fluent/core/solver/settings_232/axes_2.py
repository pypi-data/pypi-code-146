#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .border import border
from .bottom import bottom
from .clear_1 import clear
from .left import left
from .right_1 import right
from .top import top
from .visible_1 import visible
class axes(Group):
    """
    Enter the axes window options menu.
    """

    fluent_name = "axes"

    child_names = \
        ['border', 'bottom', 'clear', 'left', 'right', 'top', 'visible']

    border: border = border
    """
    border child of axes.
    """
    bottom: bottom = bottom
    """
    bottom child of axes.
    """
    clear: clear = clear
    """
    clear child of axes.
    """
    left: left = left
    """
    left child of axes.
    """
    right: right = right
    """
    right child of axes.
    """
    top: top = top
    """
    top child of axes.
    """
    visible: visible = visible
    """
    visible child of axes.
    """
