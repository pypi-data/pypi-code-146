#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .pattern import pattern
from .weight import weight
from .color import color
class lines_child(Group):
    """
    'child_object_type' of lines.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pattern', 'weight', 'color']

    pattern: pattern = pattern
    """
    pattern child of lines_child.
    """
    weight: weight = weight
    """
    weight child of lines_child.
    """
    color: color = color
    """
    color child of lines_child.
    """
