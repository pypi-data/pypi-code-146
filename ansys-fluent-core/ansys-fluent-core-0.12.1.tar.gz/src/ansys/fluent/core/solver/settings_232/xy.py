#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .border_4 import border
from .bottom_4 import bottom
from .left_4 import left
from .right_5 import right
from .top_4 import top
from .visible_5 import visible
class xy(Group):
    """
    Enter the X-Y plot window options menu.
    """

    fluent_name = "xy"

    child_names = \
        ['border', 'bottom', 'left', 'right', 'top', 'visible']

    border: border = border
    """
    border child of xy.
    """
    bottom: bottom = bottom
    """
    bottom child of xy.
    """
    left: left = left
    """
    left child of xy.
    """
    right: right = right
    """
    right child of xy.
    """
    top: top = top
    """
    top child of xy.
    """
    visible: visible = visible
    """
    visible child of xy.
    """
