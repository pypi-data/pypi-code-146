#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .lines_child import lines_child

class lines(ListObject[lines_child]):
    """
    'lines' child.
    """

    fluent_name = "lines"

    child_object_type: lines_child = lines_child
    """
    child_object_type of lines.
    """
