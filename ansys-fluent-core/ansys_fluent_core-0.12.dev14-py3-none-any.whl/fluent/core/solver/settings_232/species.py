#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .volumetric_species import volumetric_species
from .last_species import last_species
class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['volumetric_species', 'last_species']

    volumetric_species: volumetric_species = volumetric_species
    """
    volumetric_species child of species.
    """
    last_species: last_species = last_species
    """
    last_species child of species.
    """
