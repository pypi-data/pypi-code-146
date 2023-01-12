#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .viscous_scale import viscous_scale
from .gravity_scale import gravity_scale
from .surface_tension_scale import surface_tension_scale
from .acoustic_scale import acoustic_scale
class time_scale_options(Group):
    """
    'time_scale_options' child.
    """

    fluent_name = "time-scale-options"

    child_names = \
        ['viscous_scale', 'gravity_scale', 'surface_tension_scale',
         'acoustic_scale']

    viscous_scale: viscous_scale = viscous_scale
    """
    viscous_scale child of time_scale_options.
    """
    gravity_scale: gravity_scale = gravity_scale
    """
    gravity_scale child of time_scale_options.
    """
    surface_tension_scale: surface_tension_scale = surface_tension_scale
    """
    surface_tension_scale child of time_scale_options.
    """
    acoustic_scale: acoustic_scale = acoustic_scale
    """
    acoustic_scale child of time_scale_options.
    """
