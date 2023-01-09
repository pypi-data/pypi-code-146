#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .chemical_formula import chemical_formula
from .density_5 import density
from .specific_heat_4 import specific_heat
from .species_1 import species
from .vp_equilib import vp_equilib
from .thermal_conductivity_3 import thermal_conductivity
from .viscosity_2 import viscosity
from .dpm_surften import dpm_surften
from .emissivity_2 import emissivity
from .scattering_factor_2 import scattering_factor
from .vaporization_model import vaporization_model
from .averaging_coefficient_t import averaging_coefficient_t
from .averaging_coefficient_y import averaging_coefficient_y
from .thermophoretic_co import thermophoretic_co
from .reaction_model import reaction_model
class particle_mixture_child(Group):
    """
    'child_object_type' of particle_mixture.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['chemical_formula', 'density', 'specific_heat', 'species',
         'vp_equilib', 'thermal_conductivity', 'viscosity', 'dpm_surften',
         'emissivity', 'scattering_factor', 'vaporization_model',
         'averaging_coefficient_t', 'averaging_coefficient_y',
         'thermophoretic_co', 'reaction_model']

    chemical_formula: chemical_formula = chemical_formula
    """
    chemical_formula child of particle_mixture_child.
    """
    density: density = density
    """
    density child of particle_mixture_child.
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat child of particle_mixture_child.
    """
    species: species = species
    """
    species child of particle_mixture_child.
    """
    vp_equilib: vp_equilib = vp_equilib
    """
    vp_equilib child of particle_mixture_child.
    """
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    """
    thermal_conductivity child of particle_mixture_child.
    """
    viscosity: viscosity = viscosity
    """
    viscosity child of particle_mixture_child.
    """
    dpm_surften: dpm_surften = dpm_surften
    """
    dpm_surften child of particle_mixture_child.
    """
    emissivity: emissivity = emissivity
    """
    emissivity child of particle_mixture_child.
    """
    scattering_factor: scattering_factor = scattering_factor
    """
    scattering_factor child of particle_mixture_child.
    """
    vaporization_model: vaporization_model = vaporization_model
    """
    vaporization_model child of particle_mixture_child.
    """
    averaging_coefficient_t: averaging_coefficient_t = averaging_coefficient_t
    """
    averaging_coefficient_t child of particle_mixture_child.
    """
    averaging_coefficient_y: averaging_coefficient_y = averaging_coefficient_y
    """
    averaging_coefficient_y child of particle_mixture_child.
    """
    thermophoretic_co: thermophoretic_co = thermophoretic_co
    """
    thermophoretic_co child of particle_mixture_child.
    """
    reaction_model: reaction_model = reaction_model
    """
    reaction_model child of particle_mixture_child.
    """
