#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .chemical_formula import chemical_formula
from .density_2 import density
from .viscosity_1 import viscosity
from .specific_heat_2 import specific_heat
from .thermal_conductivity_2 import thermal_conductivity
from .premix_laminar_speed import premix_laminar_speed
from .premix_laminar_thickness import premix_laminar_thickness
from .premix_unburnt_temp_1 import premix_unburnt_temp
from .premix_unburnt_cp import premix_unburnt_cp
from .premix_unburnt_density_1 import premix_unburnt_density
from .premix_heat_trans_coeff_1 import premix_heat_trans_coeff
from .premix_critical_strain import premix_critical_strain
from .therm_exp_coeff import therm_exp_coeff
from .absorption_coefficient_1 import absorption_coefficient
from .scattering_coefficient import scattering_coefficient
from .scattering_phase_function import scattering_phase_function
from .refractive_index import refractive_index
from .mass_diffusivity import mass_diffusivity
from .species import species
from .reactions import reactions
from .reaction_mechs import reaction_mechs
from .uds_diffusivity import uds_diffusivity
from .thermal_diffusivity import thermal_diffusivity
from .tmelt import tmelt
from .melting_heat import melting_heat
from .eutectic_temp import eutectic_temp
from .speed_of_sound import speed_of_sound
from .critical_temperature import critical_temperature
from .critical_pressure import critical_pressure
from .critical_volume import critical_volume
from .acentric_factor import acentric_factor
from .electric_conductivity import electric_conductivity
from .dual_electric_conductivity import dual_electric_conductivity
from .lithium_diffusivity import lithium_diffusivity
from .collision_cross_section import collision_cross_section
class mixture_child(Group):
    """
    'child_object_type' of mixture.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['chemical_formula', 'density', 'viscosity', 'specific_heat',
         'thermal_conductivity', 'premix_laminar_speed',
         'premix_laminar_thickness', 'premix_unburnt_temp',
         'premix_unburnt_cp', 'premix_unburnt_density',
         'premix_heat_trans_coeff', 'premix_critical_strain',
         'therm_exp_coeff', 'absorption_coefficient',
         'scattering_coefficient', 'scattering_phase_function',
         'refractive_index', 'mass_diffusivity', 'species', 'reactions',
         'reaction_mechs', 'uds_diffusivity', 'thermal_diffusivity', 'tmelt',
         'melting_heat', 'eutectic_temp', 'speed_of_sound',
         'critical_temperature', 'critical_pressure', 'critical_volume',
         'acentric_factor', 'electric_conductivity',
         'dual_electric_conductivity', 'lithium_diffusivity',
         'collision_cross_section']

    chemical_formula: chemical_formula = chemical_formula
    """
    chemical_formula child of mixture_child.
    """
    density: density = density
    """
    density child of mixture_child.
    """
    viscosity: viscosity = viscosity
    """
    viscosity child of mixture_child.
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat child of mixture_child.
    """
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    """
    thermal_conductivity child of mixture_child.
    """
    premix_laminar_speed: premix_laminar_speed = premix_laminar_speed
    """
    premix_laminar_speed child of mixture_child.
    """
    premix_laminar_thickness: premix_laminar_thickness = premix_laminar_thickness
    """
    premix_laminar_thickness child of mixture_child.
    """
    premix_unburnt_temp: premix_unburnt_temp = premix_unburnt_temp
    """
    premix_unburnt_temp child of mixture_child.
    """
    premix_unburnt_cp: premix_unburnt_cp = premix_unburnt_cp
    """
    premix_unburnt_cp child of mixture_child.
    """
    premix_unburnt_density: premix_unburnt_density = premix_unburnt_density
    """
    premix_unburnt_density child of mixture_child.
    """
    premix_heat_trans_coeff: premix_heat_trans_coeff = premix_heat_trans_coeff
    """
    premix_heat_trans_coeff child of mixture_child.
    """
    premix_critical_strain: premix_critical_strain = premix_critical_strain
    """
    premix_critical_strain child of mixture_child.
    """
    therm_exp_coeff: therm_exp_coeff = therm_exp_coeff
    """
    therm_exp_coeff child of mixture_child.
    """
    absorption_coefficient: absorption_coefficient = absorption_coefficient
    """
    absorption_coefficient child of mixture_child.
    """
    scattering_coefficient: scattering_coefficient = scattering_coefficient
    """
    scattering_coefficient child of mixture_child.
    """
    scattering_phase_function: scattering_phase_function = scattering_phase_function
    """
    scattering_phase_function child of mixture_child.
    """
    refractive_index: refractive_index = refractive_index
    """
    refractive_index child of mixture_child.
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of mixture_child.
    """
    species: species = species
    """
    species child of mixture_child.
    """
    reactions: reactions = reactions
    """
    reactions child of mixture_child.
    """
    reaction_mechs: reaction_mechs = reaction_mechs
    """
    reaction_mechs child of mixture_child.
    """
    uds_diffusivity: uds_diffusivity = uds_diffusivity
    """
    uds_diffusivity child of mixture_child.
    """
    thermal_diffusivity: thermal_diffusivity = thermal_diffusivity
    """
    thermal_diffusivity child of mixture_child.
    """
    tmelt: tmelt = tmelt
    """
    tmelt child of mixture_child.
    """
    melting_heat: melting_heat = melting_heat
    """
    melting_heat child of mixture_child.
    """
    eutectic_temp: eutectic_temp = eutectic_temp
    """
    eutectic_temp child of mixture_child.
    """
    speed_of_sound: speed_of_sound = speed_of_sound
    """
    speed_of_sound child of mixture_child.
    """
    critical_temperature: critical_temperature = critical_temperature
    """
    critical_temperature child of mixture_child.
    """
    critical_pressure: critical_pressure = critical_pressure
    """
    critical_pressure child of mixture_child.
    """
    critical_volume: critical_volume = critical_volume
    """
    critical_volume child of mixture_child.
    """
    acentric_factor: acentric_factor = acentric_factor
    """
    acentric_factor child of mixture_child.
    """
    electric_conductivity: electric_conductivity = electric_conductivity
    """
    electric_conductivity child of mixture_child.
    """
    dual_electric_conductivity: dual_electric_conductivity = dual_electric_conductivity
    """
    dual_electric_conductivity child of mixture_child.
    """
    lithium_diffusivity: lithium_diffusivity = lithium_diffusivity
    """
    lithium_diffusivity child of mixture_child.
    """
    collision_cross_section: collision_cross_section = collision_cross_section
    """
    collision_cross_section child of mixture_child.
    """
