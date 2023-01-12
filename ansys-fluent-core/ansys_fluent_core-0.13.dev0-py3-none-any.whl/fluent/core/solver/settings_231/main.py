#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .border_1 import border
from .bottom_1 import bottom
from .left_1 import left
from .right_2 import right
from .top_1 import top
from .visible_2 import visible
class main(Group):
    """
    Enter the main view window options menu.
    """

    fluent_name = "main"

    child_names = \
        ['border', 'bottom', 'left', 'right', 'top', 'visible']

    border: border = border
    """
    border child of main.
    """
    bottom: bottom = bottom
    """
    bottom child of main.
    """
    left: left = left
    """
    left child of main.
    """
    right: right = right
    """
    right child of main.
    """
    top: top = top
    """
    top child of main.
    """
    visible: visible = visible
    """
    visible child of main.
    """
