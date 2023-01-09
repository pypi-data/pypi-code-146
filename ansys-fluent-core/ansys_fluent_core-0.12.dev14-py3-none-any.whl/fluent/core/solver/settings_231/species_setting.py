#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_specified_species import user_specified_species
from .species_1 import species
class species_setting(Group):
    """
    Enter the species settings menu.
    """

    fluent_name = "species-setting"

    child_names = \
        ['user_specified_species', 'species']

    user_specified_species: user_specified_species = user_specified_species
    """
    user_specified_species child of species_setting.
    """
    species: species = species
    """
    species child of species_setting.
    """
