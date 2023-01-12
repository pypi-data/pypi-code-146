#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .r import r
from .u import u
class matrix(Group):
    """
    'matrix' child.
    """

    fluent_name = "matrix"

    child_names = \
        ['r', 'u']

    r: r = r
    """
    r child of matrix.
    """
    u: u = u
    """
    u child of matrix.
    """
