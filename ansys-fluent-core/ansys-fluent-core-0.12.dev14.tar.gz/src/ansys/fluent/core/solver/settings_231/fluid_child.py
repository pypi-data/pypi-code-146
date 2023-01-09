#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .density import density
from .viscosity import viscosity
from .specific_heat import specific_heat
from .thermal_conductivity import thermal_conductivity
from .molecular_weight import molecular_weight
from .premix_laminar_speed import premix_laminar_speed
from .premix_critical_strain import premix_critical_strain
from .premix_unburnt_temp import premix_unburnt_temp
from .premix_unburnt_density import premix_unburnt_density
from .premix_heat_trans_coeff import premix_heat_trans_coeff
from .premix_heat_of_comb import premix_heat_of_comb
from .premix_unburnt_fuel_mf import premix_unburnt_fuel_mf
from .premix_adiabatic_temp import premix_adiabatic_temp
from .therm_exp_coeff import therm_exp_coeff
from .characteristic_vibrational_temperature import characteristic_vibrational_temperature
from .absorption_coefficient import absorption_coefficient
from .melting_heat import melting_heat
from .tsolidus import tsolidus
from .tliqidus import tliqidus
from .liquidus_slope import liquidus_slope
from .partition_coeff import partition_coeff
from .eutectic_mf import eutectic_mf
from .solid_diffusion import solid_diffusion
from .solut_exp_coeff import solut_exp_coeff
from .scattering_coefficient import scattering_coefficient
from .scattering_phase_function import scattering_phase_function
from .refractive_index import refractive_index
from .formation_entropy import formation_entropy
from .formation_enthalpy import formation_enthalpy
from .reference_temperature_1 import reference_temperature
from .lennard_jones_length import lennard_jones_length
from .lennard_jones_energy import lennard_jones_energy
from .thermal_accom_coefficient import thermal_accom_coefficient
from .velocity_accom_coefficient import velocity_accom_coefficient
from .degrees_of_freedom import degrees_of_freedom
from .uds_diffusivity import uds_diffusivity
from .electric_conductivity import electric_conductivity
from .dual_electric_conductivity import dual_electric_conductivity
from .lithium_diffusivity import lithium_diffusivity
from .magnetic_permeability import magnetic_permeability
from .speed_of_sound import speed_of_sound
from .critical_temperature import critical_temperature
from .critical_pressure import critical_pressure
from .critical_volume import critical_volume
from .acentric_factor import acentric_factor
from .latent_heat import latent_heat
from .saturation_pressure import saturation_pressure
from .vaporization_temperature import vaporization_temperature
from .charge import charge
class fluid_child(Group):
    """
    'child_object_type' of fluid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'viscosity', 'specific_heat', 'thermal_conductivity',
         'molecular_weight', 'premix_laminar_speed', 'premix_critical_strain',
         'premix_unburnt_temp', 'premix_unburnt_density',
         'premix_heat_trans_coeff', 'premix_heat_of_comb',
         'premix_unburnt_fuel_mf', 'premix_adiabatic_temp', 'therm_exp_coeff',
         'characteristic_vibrational_temperature', 'absorption_coefficient',
         'melting_heat', 'tsolidus', 'tliqidus', 'liquidus_slope',
         'partition_coeff', 'eutectic_mf', 'solid_diffusion',
         'solut_exp_coeff', 'scattering_coefficient',
         'scattering_phase_function', 'refractive_index', 'formation_entropy',
         'formation_enthalpy', 'reference_temperature',
         'lennard_jones_length', 'lennard_jones_energy',
         'thermal_accom_coefficient', 'velocity_accom_coefficient',
         'degrees_of_freedom', 'uds_diffusivity', 'electric_conductivity',
         'dual_electric_conductivity', 'lithium_diffusivity',
         'magnetic_permeability', 'speed_of_sound', 'critical_temperature',
         'critical_pressure', 'critical_volume', 'acentric_factor',
         'latent_heat', 'saturation_pressure', 'vaporization_temperature',
         'charge']

    density: density = density
    """
    density child of fluid_child.
    """
    viscosity: viscosity = viscosity
    """
    viscosity child of fluid_child.
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat child of fluid_child.
    """
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    """
    thermal_conductivity child of fluid_child.
    """
    molecular_weight: molecular_weight = molecular_weight
    """
    molecular_weight child of fluid_child.
    """
    premix_laminar_speed: premix_laminar_speed = premix_laminar_speed
    """
    premix_laminar_speed child of fluid_child.
    """
    premix_critical_strain: premix_critical_strain = premix_critical_strain
    """
    premix_critical_strain child of fluid_child.
    """
    premix_unburnt_temp: premix_unburnt_temp = premix_unburnt_temp
    """
    premix_unburnt_temp child of fluid_child.
    """
    premix_unburnt_density: premix_unburnt_density = premix_unburnt_density
    """
    premix_unburnt_density child of fluid_child.
    """
    premix_heat_trans_coeff: premix_heat_trans_coeff = premix_heat_trans_coeff
    """
    premix_heat_trans_coeff child of fluid_child.
    """
    premix_heat_of_comb: premix_heat_of_comb = premix_heat_of_comb
    """
    premix_heat_of_comb child of fluid_child.
    """
    premix_unburnt_fuel_mf: premix_unburnt_fuel_mf = premix_unburnt_fuel_mf
    """
    premix_unburnt_fuel_mf child of fluid_child.
    """
    premix_adiabatic_temp: premix_adiabatic_temp = premix_adiabatic_temp
    """
    premix_adiabatic_temp child of fluid_child.
    """
    therm_exp_coeff: therm_exp_coeff = therm_exp_coeff
    """
    therm_exp_coeff child of fluid_child.
    """
    characteristic_vibrational_temperature: characteristic_vibrational_temperature = characteristic_vibrational_temperature
    """
    characteristic_vibrational_temperature child of fluid_child.
    """
    absorption_coefficient: absorption_coefficient = absorption_coefficient
    """
    absorption_coefficient child of fluid_child.
    """
    melting_heat: melting_heat = melting_heat
    """
    melting_heat child of fluid_child.
    """
    tsolidus: tsolidus = tsolidus
    """
    tsolidus child of fluid_child.
    """
    tliqidus: tliqidus = tliqidus
    """
    tliqidus child of fluid_child.
    """
    liquidus_slope: liquidus_slope = liquidus_slope
    """
    liquidus_slope child of fluid_child.
    """
    partition_coeff: partition_coeff = partition_coeff
    """
    partition_coeff child of fluid_child.
    """
    eutectic_mf: eutectic_mf = eutectic_mf
    """
    eutectic_mf child of fluid_child.
    """
    solid_diffusion: solid_diffusion = solid_diffusion
    """
    solid_diffusion child of fluid_child.
    """
    solut_exp_coeff: solut_exp_coeff = solut_exp_coeff
    """
    solut_exp_coeff child of fluid_child.
    """
    scattering_coefficient: scattering_coefficient = scattering_coefficient
    """
    scattering_coefficient child of fluid_child.
    """
    scattering_phase_function: scattering_phase_function = scattering_phase_function
    """
    scattering_phase_function child of fluid_child.
    """
    refractive_index: refractive_index = refractive_index
    """
    refractive_index child of fluid_child.
    """
    formation_entropy: formation_entropy = formation_entropy
    """
    formation_entropy child of fluid_child.
    """
    formation_enthalpy: formation_enthalpy = formation_enthalpy
    """
    formation_enthalpy child of fluid_child.
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of fluid_child.
    """
    lennard_jones_length: lennard_jones_length = lennard_jones_length
    """
    lennard_jones_length child of fluid_child.
    """
    lennard_jones_energy: lennard_jones_energy = lennard_jones_energy
    """
    lennard_jones_energy child of fluid_child.
    """
    thermal_accom_coefficient: thermal_accom_coefficient = thermal_accom_coefficient
    """
    thermal_accom_coefficient child of fluid_child.
    """
    velocity_accom_coefficient: velocity_accom_coefficient = velocity_accom_coefficient
    """
    velocity_accom_coefficient child of fluid_child.
    """
    degrees_of_freedom: degrees_of_freedom = degrees_of_freedom
    """
    degrees_of_freedom child of fluid_child.
    """
    uds_diffusivity: uds_diffusivity = uds_diffusivity
    """
    uds_diffusivity child of fluid_child.
    """
    electric_conductivity: electric_conductivity = electric_conductivity
    """
    electric_conductivity child of fluid_child.
    """
    dual_electric_conductivity: dual_electric_conductivity = dual_electric_conductivity
    """
    dual_electric_conductivity child of fluid_child.
    """
    lithium_diffusivity: lithium_diffusivity = lithium_diffusivity
    """
    lithium_diffusivity child of fluid_child.
    """
    magnetic_permeability: magnetic_permeability = magnetic_permeability
    """
    magnetic_permeability child of fluid_child.
    """
    speed_of_sound: speed_of_sound = speed_of_sound
    """
    speed_of_sound child of fluid_child.
    """
    critical_temperature: critical_temperature = critical_temperature
    """
    critical_temperature child of fluid_child.
    """
    critical_pressure: critical_pressure = critical_pressure
    """
    critical_pressure child of fluid_child.
    """
    critical_volume: critical_volume = critical_volume
    """
    critical_volume child of fluid_child.
    """
    acentric_factor: acentric_factor = acentric_factor
    """
    acentric_factor child of fluid_child.
    """
    latent_heat: latent_heat = latent_heat
    """
    latent_heat child of fluid_child.
    """
    saturation_pressure: saturation_pressure = saturation_pressure
    """
    saturation_pressure child of fluid_child.
    """
    vaporization_temperature: vaporization_temperature = vaporization_temperature
    """
    vaporization_temperature child of fluid_child.
    """
    charge: charge = charge
    """
    charge child of fluid_child.
    """
