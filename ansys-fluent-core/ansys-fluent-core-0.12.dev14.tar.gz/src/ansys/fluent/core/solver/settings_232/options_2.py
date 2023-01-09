#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .thermal_effects_1 import thermal_effects
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['thermal_effects']

    thermal_effects: thermal_effects = thermal_effects
    """
    thermal_effects child of options.
    """
