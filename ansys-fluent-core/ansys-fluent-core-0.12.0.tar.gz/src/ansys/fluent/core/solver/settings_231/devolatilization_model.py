#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .single_rate import single_rate
from .two_competing_rates import two_competing_rates
from .cpd_model import cpd_model
class devolatilization_model(Group):
    """
    'devolatilization_model' child.
    """

    fluent_name = "devolatilization-model"

    child_names = \
        ['option', 'value', 'single_rate', 'two_competing_rates', 'cpd_model']

    option: option = option
    """
    option child of devolatilization_model.
    """
    value: value = value
    """
    value child of devolatilization_model.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of devolatilization_model.
    """
    two_competing_rates: two_competing_rates = two_competing_rates
    """
    two_competing_rates child of devolatilization_model.
    """
    cpd_model: cpd_model = cpd_model
    """
    cpd_model child of devolatilization_model.
    """
