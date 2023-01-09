#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .pre_exponential_factor import pre_exponential_factor
from .activation_energy import activation_energy
from .weighting_factor import weighting_factor
class first_rate(Group):
    """
    'first_rate' child.
    """

    fluent_name = "first-rate"

    child_names = \
        ['pre_exponential_factor', 'activation_energy', 'weighting_factor']

    pre_exponential_factor: pre_exponential_factor = pre_exponential_factor
    """
    pre_exponential_factor child of first_rate.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of first_rate.
    """
    weighting_factor: weighting_factor = weighting_factor
    """
    weighting_factor child of first_rate.
    """
