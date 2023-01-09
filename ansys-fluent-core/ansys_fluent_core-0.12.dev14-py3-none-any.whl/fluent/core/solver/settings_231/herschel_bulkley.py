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
from .yield_stress_threshold import yield_stress_threshold
from .critical_shear_rate import critical_shear_rate
from .reference_temperature import reference_temperature
from .activation_energy import activation_energy
class herschel_bulkley(Group):
    """
    'herschel_bulkley' child.
    """

    fluent_name = "herschel-bulkley"

    child_names = \
        ['option', 'consistency_index', 'power_law_index',
         'yield_stress_threshold', 'critical_shear_rate',
         'reference_temperature', 'activation_energy']

    option: option = option
    """
    option child of herschel_bulkley.
    """
    consistency_index: consistency_index = consistency_index
    """
    consistency_index child of herschel_bulkley.
    """
    power_law_index: power_law_index = power_law_index
    """
    power_law_index child of herschel_bulkley.
    """
    yield_stress_threshold: yield_stress_threshold = yield_stress_threshold
    """
    yield_stress_threshold child of herschel_bulkley.
    """
    critical_shear_rate: critical_shear_rate = critical_shear_rate
    """
    critical_shear_rate child of herschel_bulkley.
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of herschel_bulkley.
    """
    activation_energy: activation_energy = activation_energy
    """
    activation_energy child of herschel_bulkley.
    """
