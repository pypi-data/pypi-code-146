#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .lower import lower
from .upper import upper
class between_std_dev(Group):
    """
    'between_std_dev' child.
    """

    fluent_name = "between-std-dev"

    child_names = \
        ['lower', 'upper']

    lower: lower = lower
    """
    lower child of between_std_dev.
    """
    upper: upper = upper
    """
    upper child of between_std_dev.
    """
