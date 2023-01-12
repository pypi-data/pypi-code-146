#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .computed_heat_rejection import computed_heat_rejection
from .inlet_temperature import inlet_temperature
from .outlet_temperature import outlet_temperature
from .mass_flow_rate import mass_flow_rate
from .specific_heat_5 import specific_heat
class heat_exchange(Group):
    """
    'heat_exchange' child.
    """

    fluent_name = "heat-exchange"

    command_names = \
        ['computed_heat_rejection', 'inlet_temperature', 'outlet_temperature',
         'mass_flow_rate', 'specific_heat']

    computed_heat_rejection: computed_heat_rejection = computed_heat_rejection
    """
    computed_heat_rejection command of heat_exchange.
    """
    inlet_temperature: inlet_temperature = inlet_temperature
    """
    inlet_temperature command of heat_exchange.
    """
    outlet_temperature: outlet_temperature = outlet_temperature
    """
    outlet_temperature command of heat_exchange.
    """
    mass_flow_rate: mass_flow_rate = mass_flow_rate
    """
    mass_flow_rate command of heat_exchange.
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat command of heat_exchange.
    """
