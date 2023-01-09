#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .vibrational_modes import vibrational_modes
from .value import value
class characteristic_vibrational_temperature(Group):
    """
    'characteristic_vibrational_temperature' child.
    """

    fluent_name = "characteristic-vibrational-temperature"

    child_names = \
        ['option', 'vibrational_modes', 'value']

    option: option = option
    """
    option child of characteristic_vibrational_temperature.
    """
    vibrational_modes: vibrational_modes = vibrational_modes
    """
    vibrational_modes child of characteristic_vibrational_temperature.
    """
    value: value = value
    """
    value child of characteristic_vibrational_temperature.
    """
