#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .general_settings_1 import general_settings
from .turbulent_setting import turbulent_setting
from .species_setting import species_setting
class hybrid_init_options(Group):
    """
    Enter the settings for hybrid initialization method.
    """

    fluent_name = "hybrid-init-options"

    child_names = \
        ['general_settings', 'turbulent_setting', 'species_setting']

    general_settings: general_settings = general_settings
    """
    general_settings child of hybrid_init_options.
    """
    turbulent_setting: turbulent_setting = turbulent_setting
    """
    turbulent_setting child of hybrid_init_options.
    """
    species_setting: species_setting = species_setting
    """
    species_setting child of hybrid_init_options.
    """
