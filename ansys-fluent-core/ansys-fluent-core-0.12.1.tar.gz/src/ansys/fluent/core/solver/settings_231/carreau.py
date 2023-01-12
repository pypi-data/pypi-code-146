#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .time_constant import time_constant
from .power_law_index import power_law_index
from .zero_shear_viscosity import zero_shear_viscosity
from .infinite_shear_viscosity import infinite_shear_viscosity
from .reference_temperature import reference_temperature
from .activation_energy import activation_energy
class carreau(Group):
    """
    'carreau' child.
    """

    fluent_name = "carreau"

    child_names = \
        ['option', 'time_constant', 'power_law_index', 'zero_shear_viscosity',
         'infinite_shear_viscosity', 'reference_temperature',
         'activation_energy']

    option: option = option
    """
    option child of carreau.
    """
    time_constant: time_constant = time_constant
    """
    time_constant child of carreau.
    """
    power_law_index: power_law_index = power_law_index
    """
    power_law_index child of carreau.
    """
    zero_shear_viscosity: zero_shear_viscosity = zero_shear_viscosity
    """
    zero_shear_viscosity child of carreau.
    """
    infinite_shear_viscosity: infinite_shear_viscosity = infinite_shear_viscosity
    """
    infinite_shear_viscosity child of carreau.
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of carreau.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of carreau.
    """
