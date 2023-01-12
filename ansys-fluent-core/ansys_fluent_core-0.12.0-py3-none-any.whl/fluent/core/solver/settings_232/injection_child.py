#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_type import report_type
from .user_specified_origin_and_axis import user_specified_origin_and_axis
from .origin_1 import origin
from .axis_1 import axis
from .mass_criterion import mass_criterion
from .physics import physics
from .boundary_zones_names import boundary_zones_names
from .boundary_zones_1 import boundary_zones
from .retain_instantaneous_values import retain_instantaneous_values
from .inj_mass_rate_last_tstp import inj_mass_rate_last_tstp
from .inj_mass_rate_last_flow import inj_mass_rate_last_flow
from .inj_mass_rate_prev_mass import inj_mass_rate_prev_mass
from .inj_mass_rate_prev_time import inj_mass_rate_prev_time
from .show_unsteady_rate import show_unsteady_rate
from .old_props import old_props
from .average_over import average_over
from .per_injection import per_injection
from .injection_list import injection_list
class injection_child(Group):
    """
    'child_object_type' of injection.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['report_type', 'user_specified_origin_and_axis', 'origin', 'axis',
         'mass_criterion', 'physics', 'boundary_zones_names',
         'boundary_zones', 'retain_instantaneous_values',
         'inj_mass_rate_last_tstp', 'inj_mass_rate_last_flow',
         'inj_mass_rate_prev_mass', 'inj_mass_rate_prev_time',
         'show_unsteady_rate', 'old_props', 'average_over', 'per_injection',
         'injection_list']

    report_type: report_type = report_type
    """
    report_type child of injection_child.
    """
    user_specified_origin_and_axis: user_specified_origin_and_axis = user_specified_origin_and_axis
    """
    user_specified_origin_and_axis child of injection_child.
    """
    origin: origin = origin
    """
    origin child of injection_child.
    """
    axis: axis = axis
    """
    axis child of injection_child.
    """
    mass_criterion: mass_criterion = mass_criterion
    """
    mass_criterion child of injection_child.
    """
    physics: physics = physics
    """
    physics child of injection_child.
    """
    boundary_zones_names: boundary_zones_names = boundary_zones_names
    """
    boundary_zones_names child of injection_child.
    """
    boundary_zones: boundary_zones = boundary_zones
    """
    boundary_zones child of injection_child.
    """
    retain_instantaneous_values: retain_instantaneous_values = retain_instantaneous_values
    """
    retain_instantaneous_values child of injection_child.
    """
    inj_mass_rate_last_tstp: inj_mass_rate_last_tstp = inj_mass_rate_last_tstp
    """
    inj_mass_rate_last_tstp child of injection_child.
    """
    inj_mass_rate_last_flow: inj_mass_rate_last_flow = inj_mass_rate_last_flow
    """
    inj_mass_rate_last_flow child of injection_child.
    """
    inj_mass_rate_prev_mass: inj_mass_rate_prev_mass = inj_mass_rate_prev_mass
    """
    inj_mass_rate_prev_mass child of injection_child.
    """
    inj_mass_rate_prev_time: inj_mass_rate_prev_time = inj_mass_rate_prev_time
    """
    inj_mass_rate_prev_time child of injection_child.
    """
    show_unsteady_rate: show_unsteady_rate = show_unsteady_rate
    """
    show_unsteady_rate child of injection_child.
    """
    old_props: old_props = old_props
    """
    old_props child of injection_child.
    """
    average_over: average_over = average_over
    """
    average_over child of injection_child.
    """
    per_injection: per_injection = per_injection
    """
    per_injection child of injection_child.
    """
    injection_list: injection_list = injection_list
    """
    injection_list child of injection_child.
    """
