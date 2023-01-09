#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .density_4 import density
from .thermal_conductivity_3 import thermal_conductivity
from .latent_heat_1 import latent_heat
from .volatile_fraction import volatile_fraction
from .combustible_fraction import combustible_fraction
from .swelling_coefficient import swelling_coefficient
from .burn_stoichiometry import burn_stoichiometry
from .specific_heat_3 import specific_heat
from .binary_diffusivity import binary_diffusivity
from .diffusivity_reference_pressure import diffusivity_reference_pressure
from .vaporization_temperature import vaporization_temperature
from .thermophoretic_co import thermophoretic_co
from .burn_hreact import burn_hreact
from .burn_hreact_fraction import burn_hreact_fraction
from .devolatilization_model import devolatilization_model
from .combustion_model import combustion_model
from .scattering_factor_1 import scattering_factor
from .emissivity_1 import emissivity
class combusting_particle_child(Group):
    """
    'child_object_type' of combusting_particle.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'thermal_conductivity', 'latent_heat',
         'volatile_fraction', 'combustible_fraction', 'swelling_coefficient',
         'burn_stoichiometry', 'specific_heat', 'binary_diffusivity',
         'diffusivity_reference_pressure', 'vaporization_temperature',
         'thermophoretic_co', 'burn_hreact', 'burn_hreact_fraction',
         'devolatilization_model', 'combustion_model', 'scattering_factor',
         'emissivity']

    density: density = density
    """
    density child of combusting_particle_child.
    """
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    """
    thermal_conductivity child of combusting_particle_child.
    """
    latent_heat: latent_heat = latent_heat
    """
    latent_heat child of combusting_particle_child.
    """
    volatile_fraction: volatile_fraction = volatile_fraction
    """
    volatile_fraction child of combusting_particle_child.
    """
    combustible_fraction: combustible_fraction = combustible_fraction
    """
    combustible_fraction child of combusting_particle_child.
    """
    swelling_coefficient: swelling_coefficient = swelling_coefficient
    """
    swelling_coefficient child of combusting_particle_child.
    """
    burn_stoichiometry: burn_stoichiometry = burn_stoichiometry
    """
    burn_stoichiometry child of combusting_particle_child.
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat child of combusting_particle_child.
    """
    binary_diffusivity: binary_diffusivity = binary_diffusivity
    """
    binary_diffusivity child of combusting_particle_child.
    """
    diffusivity_reference_pressure: diffusivity_reference_pressure = diffusivity_reference_pressure
    """
    diffusivity_reference_pressure child of combusting_particle_child.
    """
    vaporization_temperature: vaporization_temperature = vaporization_temperature
    """
    vaporization_temperature child of combusting_particle_child.
    """
    thermophoretic_co: thermophoretic_co = thermophoretic_co
    """
    thermophoretic_co child of combusting_particle_child.
    """
    burn_hreact: burn_hreact = burn_hreact
    """
    burn_hreact child of combusting_particle_child.
    """
    burn_hreact_fraction: burn_hreact_fraction = burn_hreact_fraction
    """
    burn_hreact_fraction child of combusting_particle_child.
    """
    devolatilization_model: devolatilization_model = devolatilization_model
    """
    devolatilization_model child of combusting_particle_child.
    """
    combustion_model: combustion_model = combustion_model
    """
    combustion_model child of combusting_particle_child.
    """
    scattering_factor: scattering_factor = scattering_factor
    """
    scattering_factor child of combusting_particle_child.
    """
    emissivity: emissivity = emissivity
    """
    emissivity child of combusting_particle_child.
    """
