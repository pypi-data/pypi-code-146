#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .density_3 import density
from .specific_heat_3 import specific_heat
from .thermal_conductivity_3 import thermal_conductivity
from .thermophoretic_co import thermophoretic_co
from .scattering_factor import scattering_factor
from .emissivity import emissivity
from .viscosity_2 import viscosity
from .dpm_surften import dpm_surften
from .electric_conductivity_1 import electric_conductivity
from .dual_electric_conductivity_1 import dual_electric_conductivity
from .magnetic_permeability import magnetic_permeability
from .charge_density import charge_density
class inert_particle_child(Group):
    """
    'child_object_type' of inert_particle.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'specific_heat', 'thermal_conductivity',
         'thermophoretic_co', 'scattering_factor', 'emissivity', 'viscosity',
         'dpm_surften', 'electric_conductivity', 'dual_electric_conductivity',
         'magnetic_permeability', 'charge_density']

    density: density = density
    """
    density child of inert_particle_child.
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat child of inert_particle_child.
    """
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    """
    thermal_conductivity child of inert_particle_child.
    """
    thermophoretic_co: thermophoretic_co = thermophoretic_co
    """
    thermophoretic_co child of inert_particle_child.
    """
    scattering_factor: scattering_factor = scattering_factor
    """
    scattering_factor child of inert_particle_child.
    """
    emissivity: emissivity = emissivity
    """
    emissivity child of inert_particle_child.
    """
    viscosity: viscosity = viscosity
    """
    viscosity child of inert_particle_child.
    """
    dpm_surften: dpm_surften = dpm_surften
    """
    dpm_surften child of inert_particle_child.
    """
    electric_conductivity: electric_conductivity = electric_conductivity
    """
    electric_conductivity child of inert_particle_child.
    """
    dual_electric_conductivity: dual_electric_conductivity = dual_electric_conductivity
    """
    dual_electric_conductivity child of inert_particle_child.
    """
    magnetic_permeability: magnetic_permeability = magnetic_permeability
    """
    magnetic_permeability child of inert_particle_child.
    """
    charge_density: charge_density = charge_density
    """
    charge_density child of inert_particle_child.
    """
