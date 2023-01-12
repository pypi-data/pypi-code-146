#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .first_rate import first_rate
from .second_rate import second_rate
class two_competing_rates(Group):
    """
    'two_competing_rates' child.
    """

    fluent_name = "two-competing-rates"

    child_names = \
        ['first_rate', 'second_rate']

    first_rate: first_rate = first_rate
    """
    first_rate child of two_competing_rates.
    """
    second_rate: second_rate = second_rate
    """
    second_rate child of two_competing_rates.
    """
