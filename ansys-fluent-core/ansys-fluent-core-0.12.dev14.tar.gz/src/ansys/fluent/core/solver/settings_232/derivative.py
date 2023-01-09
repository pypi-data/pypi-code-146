#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .none_1 import none
from .gradient_1 import gradient
from .curvature import curvature
from .hessian import hessian
class derivative(Group):
    """
    'derivative' child.
    """

    fluent_name = "derivative"

    child_names = \
        ['option', 'none', 'gradient', 'curvature', 'hessian']

    option: option = option
    """
    option child of derivative.
    """
    none: none = none
    """
    none child of derivative.
    """
    gradient: gradient = gradient
    """
    gradient child of derivative.
    """
    curvature: curvature = curvature
    """
    curvature child of derivative.
    """
    hessian: hessian = hessian
    """
    hessian child of derivative.
    """
