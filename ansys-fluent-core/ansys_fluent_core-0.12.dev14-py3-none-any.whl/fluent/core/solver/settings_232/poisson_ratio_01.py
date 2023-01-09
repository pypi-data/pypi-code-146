#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class poisson_ratio_01(Group):
    """
    'poisson_ratio_01' child.
    """

    fluent_name = "poisson-ratio-01"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of poisson_ratio_01.
    """
    value: value = value
    """
    value child of poisson_ratio_01.
    """
