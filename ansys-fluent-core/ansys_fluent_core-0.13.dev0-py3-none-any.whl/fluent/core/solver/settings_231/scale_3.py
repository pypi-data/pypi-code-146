#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .border_2 import border
from .bottom_2 import bottom
from .clear_2 import clear
from .format_1 import format
from .font_size_1 import font_size
from .left_2 import left
from .margin import margin
from .right_3 import right
from .top_2 import top
from .visible_3 import visible
class scale(Group):
    """
    Enter the color scale window options menu.
    """

    fluent_name = "scale"

    child_names = \
        ['border', 'bottom', 'clear', 'format', 'font_size', 'left', 'margin',
         'right', 'top', 'visible']

    border: border = border
    """
    border child of scale.
    """
    bottom: bottom = bottom
    """
    bottom child of scale.
    """
    clear: clear = clear
    """
    clear child of scale.
    """
    format: format = format
    """
    format child of scale.
    """
    font_size: font_size = font_size
    """
    font_size child of scale.
    """
    left: left = left
    """
    left child of scale.
    """
    margin: margin = margin
    """
    margin child of scale.
    """
    right: right = right
    """
    right child of scale.
    """
    top: top = top
    """
    top child of scale.
    """
    visible: visible = visible
    """
    visible child of scale.
    """
