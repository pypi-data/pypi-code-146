#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .application import application
from .border_3 import border
from .bottom_3 import bottom
from .clear_3 import clear
from .company import company
from .date import date
from .left_3 import left
from .right_4 import right
from .top_3 import top
from .visible_4 import visible
from .alignment import alignment
class text(Group):
    """
    Enter the text window options menu.
    """

    fluent_name = "text"

    child_names = \
        ['application', 'border', 'bottom', 'clear', 'company', 'date',
         'left', 'right', 'top', 'visible', 'alignment']

    application: application = application
    """
    application child of text.
    """
    border: border = border
    """
    border child of text.
    """
    bottom: bottom = bottom
    """
    bottom child of text.
    """
    clear: clear = clear
    """
    clear child of text.
    """
    company: company = company
    """
    company child of text.
    """
    date: date = date
    """
    date child of text.
    """
    left: left = left
    """
    left child of text.
    """
    right: right = right
    """
    right child of text.
    """
    top: top = top
    """
    top child of text.
    """
    visible: visible = visible
    """
    visible child of text.
    """
    alignment: alignment = alignment
    """
    alignment child of text.
    """
