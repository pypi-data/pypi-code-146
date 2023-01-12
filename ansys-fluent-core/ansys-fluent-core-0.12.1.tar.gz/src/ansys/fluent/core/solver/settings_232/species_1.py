#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .particle_species import particle_species
from .last_species import last_species
class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['particle_species', 'last_species']

    particle_species: particle_species = particle_species
    """
    particle_species child of species.
    """
    last_species: last_species = last_species
    """
    last_species child of species.
    """
