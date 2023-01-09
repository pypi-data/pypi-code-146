#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .symbol import symbol
from .size_1 import size
from .color import color
class markers_child(Group):
    """
    'child_object_type' of markers.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['symbol', 'size', 'color']

    symbol: symbol = symbol
    """
    symbol child of markers_child.
    """
    size: size = size
    """
    size child of markers_child.
    """
    color: color = color
    """
    color child of markers_child.
    """
