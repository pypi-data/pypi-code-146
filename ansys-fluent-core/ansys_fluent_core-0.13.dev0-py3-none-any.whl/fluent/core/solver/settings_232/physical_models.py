#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .particle_drag import particle_drag
from .particle_rotation import particle_rotation
from .heat_transfer import heat_transfer
from .custom_laws import custom_laws
from .turbulent_dispersion import turbulent_dispersion
from .droplet_breakup import droplet_breakup
class physical_models(Group):
    """
    'physical_models' child.
    """

    fluent_name = "physical-models"

    child_names = \
        ['particle_drag', 'particle_rotation', 'heat_transfer', 'custom_laws',
         'turbulent_dispersion', 'droplet_breakup']

    particle_drag: particle_drag = particle_drag
    """
    particle_drag child of physical_models.
    """
    particle_rotation: particle_rotation = particle_rotation
    """
    particle_rotation child of physical_models.
    """
    heat_transfer: heat_transfer = heat_transfer
    """
    heat_transfer child of physical_models.
    """
    custom_laws: custom_laws = custom_laws
    """
    custom_laws child of physical_models.
    """
    turbulent_dispersion: turbulent_dispersion = turbulent_dispersion
    """
    turbulent_dispersion child of physical_models.
    """
    droplet_breakup: droplet_breakup = droplet_breakup
    """
    droplet_breakup child of physical_models.
    """
