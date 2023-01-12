#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .viscous_heating import viscous_heating
from .low_pressure_boundary_slip import low_pressure_boundary_slip
from .curvature_correction import curvature_correction
from .corner_flow_correction import corner_flow_correction
from .production_kato_launder import production_kato_launder
from .turb_buoyancy_effects import turb_buoyancy_effects
from .kw_buoyancy_effects import kw_buoyancy_effects
from .enable_geko import enable_geko
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['viscous_heating', 'low_pressure_boundary_slip',
         'curvature_correction', 'corner_flow_correction',
         'production_kato_launder', 'turb_buoyancy_effects',
         'kw_buoyancy_effects', 'enable_geko']

    viscous_heating: viscous_heating = viscous_heating
    """
    viscous_heating child of options.
    """
    low_pressure_boundary_slip: low_pressure_boundary_slip = low_pressure_boundary_slip
    """
    low_pressure_boundary_slip child of options.
    """
    curvature_correction: curvature_correction = curvature_correction
    """
    curvature_correction child of options.
    """
    corner_flow_correction: corner_flow_correction = corner_flow_correction
    """
    corner_flow_correction child of options.
    """
    production_kato_launder: production_kato_launder = production_kato_launder
    """
    production_kato_launder child of options.
    """
    turb_buoyancy_effects: turb_buoyancy_effects = turb_buoyancy_effects
    """
    turb_buoyancy_effects child of options.
    """
    kw_buoyancy_effects: kw_buoyancy_effects = kw_buoyancy_effects
    """
    kw_buoyancy_effects child of options.
    """
    enable_geko: enable_geko = enable_geko
    """
    enable_geko child of options.
    """
