#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .display import display
from .pathlines_child import pathlines_child

class pathlines(NamedObject[pathlines_child], _CreatableNamedObjectMixin[pathlines_child]):
    """
    'pathlines' child.
    """

    fluent_name = "pathlines"

    command_names = \
        ['display']

    display: display = display
    """
    display command of pathlines.
    """
    child_object_type: pathlines_child = pathlines_child
    """
    child_object_type of pathlines.
    """
