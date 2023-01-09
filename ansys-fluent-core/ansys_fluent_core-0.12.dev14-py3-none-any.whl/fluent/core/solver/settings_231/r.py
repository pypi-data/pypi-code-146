#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .x import x
from .y import y
from .z import z
class r(Group):
    """
    'r' child.
    """

    fluent_name = "r"

    child_names = \
        ['x', 'y', 'z']

    x: x = x
    """
    x child of r.
    """
    y: y = y
    """
    y child of r.
    """
    z: z = z
    """
    z child of r.
    """
