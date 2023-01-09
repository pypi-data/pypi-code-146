#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .lines import lines
from .markers import markers
class curves(Group):
    """
    'curves' child.
    """

    fluent_name = "curves"

    child_names = \
        ['lines', 'markers']

    lines: lines = lines
    """
    lines child of curves.
    """
    markers: markers = markers
    """
    markers child of curves.
    """
