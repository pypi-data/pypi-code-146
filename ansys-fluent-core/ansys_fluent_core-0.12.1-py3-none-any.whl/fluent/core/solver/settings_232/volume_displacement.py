#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .ddpm_phase import ddpm_phase
class volume_displacement(Group):
    """
    'volume_displacement' child.
    """

    fluent_name = "volume-displacement"

    child_names = \
        ['option', 'ddpm_phase']

    option: option = option
    """
    option child of volume_displacement.
    """
    ddpm_phase: ddpm_phase = ddpm_phase
    """
    ddpm_phase child of volume_displacement.
    """
