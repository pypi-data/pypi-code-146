#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .pre_exponential_factor import pre_exponential_factor
from .activation_energy import activation_energy
class film_thermolysis_rate(Group):
    """
    'film_thermolysis_rate' child.
    """

    fluent_name = "film-thermolysis-rate"

    child_names = \
        ['pre_exponential_factor', 'activation_energy']

    pre_exponential_factor: pre_exponential_factor = pre_exponential_factor
    """
    pre_exponential_factor child of film_thermolysis_rate.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of film_thermolysis_rate.
    """
