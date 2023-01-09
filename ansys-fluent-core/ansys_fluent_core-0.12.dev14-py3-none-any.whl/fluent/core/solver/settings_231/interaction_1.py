#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .continuous_phase import continuous_phase
from .enable_rough_wall_treatment import enable_rough_wall_treatment
from .volume_displacement import volume_displacement
class interaction(Group):
    """
    'interaction' child.
    """

    fluent_name = "interaction"

    child_names = \
        ['continuous_phase', 'enable_rough_wall_treatment',
         'volume_displacement']

    continuous_phase: continuous_phase = continuous_phase
    """
    continuous_phase child of interaction.
    """
    enable_rough_wall_treatment: enable_rough_wall_treatment = enable_rough_wall_treatment
    """
    enable_rough_wall_treatment child of interaction.
    """
    volume_displacement: volume_displacement = volume_displacement
    """
    volume_displacement child of interaction.
    """
