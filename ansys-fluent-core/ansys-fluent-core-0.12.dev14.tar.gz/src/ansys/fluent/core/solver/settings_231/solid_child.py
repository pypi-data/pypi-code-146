#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .density_1 import density
from .specific_heat_1 import specific_heat
from .thermal_conductivity_1 import thermal_conductivity
from .atomic_number import atomic_number
from .absorption_coefficient import absorption_coefficient
from .scattering_coefficient_1 import scattering_coefficient
from .scattering_phase_function import scattering_phase_function
from .refractive_index import refractive_index
from .uds_diffusivity_1 import uds_diffusivity
from .electric_conductivity import electric_conductivity
from .dual_electric_conductivity import dual_electric_conductivity
from .lithium_diffusivity import lithium_diffusivity
from .magnetic_permeability import magnetic_permeability
from .struct_youngs_modulus import struct_youngs_modulus
from .struct_poisson_ratio import struct_poisson_ratio
from .struct_start_temperature import struct_start_temperature
from .struct_thermal_expansion import struct_thermal_expansion
from .struct_damping_alpha import struct_damping_alpha
from .struct_damping_beta import struct_damping_beta
class solid_child(Group):
    """
    'child_object_type' of solid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'specific_heat', 'thermal_conductivity', 'atomic_number',
         'absorption_coefficient', 'scattering_coefficient',
         'scattering_phase_function', 'refractive_index', 'uds_diffusivity',
         'electric_conductivity', 'dual_electric_conductivity',
         'lithium_diffusivity', 'magnetic_permeability',
         'struct_youngs_modulus', 'struct_poisson_ratio',
         'struct_start_temperature', 'struct_thermal_expansion',
         'struct_damping_alpha', 'struct_damping_beta']

    density: density = density
    """
    density child of solid_child.
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat child of solid_child.
    """
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    """
    thermal_conductivity child of solid_child.
    """
    atomic_number: atomic_number = atomic_number
    """
    atomic_number child of solid_child.
    """
    absorption_coefficient: absorption_coefficient = absorption_coefficient
    """
    absorption_coefficient child of solid_child.
    """
    scattering_coefficient: scattering_coefficient = scattering_coefficient
    """
    scattering_coefficient child of solid_child.
    """
    scattering_phase_function: scattering_phase_function = scattering_phase_function
    """
    scattering_phase_function child of solid_child.
    """
    refractive_index: refractive_index = refractive_index
    """
    refractive_index child of solid_child.
    """
    uds_diffusivity: uds_diffusivity = uds_diffusivity
    """
    uds_diffusivity child of solid_child.
    """
    electric_conductivity: electric_conductivity = electric_conductivity
    """
    electric_conductivity child of solid_child.
    """
    dual_electric_conductivity: dual_electric_conductivity = dual_electric_conductivity
    """
    dual_electric_conductivity child of solid_child.
    """
    lithium_diffusivity: lithium_diffusivity = lithium_diffusivity
    """
    lithium_diffusivity child of solid_child.
    """
    magnetic_permeability: magnetic_permeability = magnetic_permeability
    """
    magnetic_permeability child of solid_child.
    """
    struct_youngs_modulus: struct_youngs_modulus = struct_youngs_modulus
    """
    struct_youngs_modulus child of solid_child.
    """
    struct_poisson_ratio: struct_poisson_ratio = struct_poisson_ratio
    """
    struct_poisson_ratio child of solid_child.
    """
    struct_start_temperature: struct_start_temperature = struct_start_temperature
    """
    struct_start_temperature child of solid_child.
    """
    struct_thermal_expansion: struct_thermal_expansion = struct_thermal_expansion
    """
    struct_thermal_expansion child of solid_child.
    """
    struct_damping_alpha: struct_damping_alpha = struct_damping_alpha
    """
    struct_damping_alpha child of solid_child.
    """
    struct_damping_beta: struct_damping_beta = struct_damping_beta
    """
    struct_damping_beta child of solid_child.
    """
