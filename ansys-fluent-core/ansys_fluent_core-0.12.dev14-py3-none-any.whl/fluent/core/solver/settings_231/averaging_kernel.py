#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .kernel import kernel
from .gaussian_factor import gaussian_factor
class averaging_kernel(Group):
    """
    'averaging_kernel' child.
    """

    fluent_name = "averaging-kernel"

    child_names = \
        ['kernel', 'gaussian_factor']

    kernel: kernel = kernel
    """
    kernel child of averaging_kernel.
    """
    gaussian_factor: gaussian_factor = gaussian_factor
    """
    gaussian_factor child of averaging_kernel.
    """
