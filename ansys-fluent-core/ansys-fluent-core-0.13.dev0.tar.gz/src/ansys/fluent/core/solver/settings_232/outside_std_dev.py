#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .lower import lower
from .upper import upper
class outside_std_dev(Group):
    """
    'outside_std_dev' child.
    """

    fluent_name = "outside-std-dev"

    child_names = \
        ['lower', 'upper']

    lower: lower = lower
    """
    lower child of outside_std_dev.
    """
    upper: upper = upper
    """
    upper child of outside_std_dev.
    """
