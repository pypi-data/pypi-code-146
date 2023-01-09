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
class u(Group):
    """
    'u' child.
    """

    fluent_name = "u"

    child_names = \
        ['x', 'y', 'z']

    x: x = x
    """
    x child of u.
    """
    y: y = y
    """
    y child of u.
    """
    z: z = z
    """
    z child of u.
    """
