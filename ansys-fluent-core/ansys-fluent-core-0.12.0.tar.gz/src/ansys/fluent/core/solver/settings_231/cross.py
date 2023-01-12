#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .zero_shear_viscosity import zero_shear_viscosity
from .power_law_index import power_law_index
from .time_constant import time_constant
from .reference_temperature import reference_temperature
from .activation_energy import activation_energy
class cross(Group):
    """
    'cross' child.
    """

    fluent_name = "cross"

    child_names = \
        ['option', 'zero_shear_viscosity', 'power_law_index', 'time_constant',
         'reference_temperature', 'activation_energy']

    option: option = option
    """
    option child of cross.
    """
    zero_shear_viscosity: zero_shear_viscosity = zero_shear_viscosity
    """
    zero_shear_viscosity child of cross.
    """
    power_law_index: power_law_index = power_law_index
    """
    power_law_index child of cross.
    """
    time_constant: time_constant = time_constant
    """
    time_constant child of cross.
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of cross.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of cross.
    """
