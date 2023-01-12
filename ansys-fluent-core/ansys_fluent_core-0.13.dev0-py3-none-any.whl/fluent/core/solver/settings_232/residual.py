#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .equation_for_residual import equation_for_residual
from .threshold import threshold
class residual(Group):
    """
    'residual' child.
    """

    fluent_name = "residual"

    child_names = \
        ['equation_for_residual', 'threshold']

    equation_for_residual: equation_for_residual = equation_for_residual
    """
    equation_for_residual child of residual.
    """
    threshold: threshold = threshold
    """
    threshold child of residual.
    """
