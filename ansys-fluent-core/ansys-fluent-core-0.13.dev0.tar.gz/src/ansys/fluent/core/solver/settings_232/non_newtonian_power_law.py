#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .consistency_index import consistency_index
from .power_law_index import power_law_index
from .minimum_viscosity import minimum_viscosity
from .maximum_viscosity import maximum_viscosity
from .reference_temperature import reference_temperature
from .activation_energy import activation_energy
class non_newtonian_power_law(Group):
    """
    'non_newtonian_power_law' child.
    """

    fluent_name = "non-newtonian-power-law"

    child_names = \
        ['option', 'consistency_index', 'power_law_index',
         'minimum_viscosity', 'maximum_viscosity', 'reference_temperature',
         'activation_energy']

    option: option = option
    """
    option child of non_newtonian_power_law.
    """
    consistency_index: consistency_index = consistency_index
    """
    consistency_index child of non_newtonian_power_law.
    """
    power_law_index: power_law_index = power_law_index
    """
    power_law_index child of non_newtonian_power_law.
    """
    minimum_viscosity: minimum_viscosity = minimum_viscosity
    """
    minimum_viscosity child of non_newtonian_power_law.
    """
    maximum_viscosity: maximum_viscosity = maximum_viscosity
    """
    maximum_viscosity child of non_newtonian_power_law.
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of non_newtonian_power_law.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of non_newtonian_power_law.
    """
