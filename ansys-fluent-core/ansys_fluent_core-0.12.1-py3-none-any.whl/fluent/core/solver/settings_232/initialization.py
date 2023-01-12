#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fmg_initialize import fmg_initialize
from .localized_turb_init import localized_turb_init
from .reference_frame_1 import reference_frame
from .fmg_options import fmg_options
from .hybrid_init_options import hybrid_init_options
from .patch import patch
from .set_defaults import set_defaults
from .open_channel_auto_init import open_channel_auto_init
from .fmg_initialization import fmg_initialization
from .initialization_type import initialization_type
from .standard_initialize import standard_initialize
from .hybrid_initialize import hybrid_initialize
from .initialize import initialize
from .dpm_reset import dpm_reset
from .lwf_reset import lwf_reset
from .init_flow_statistics import init_flow_statistics
from .init_acoustics_options import init_acoustics_options
from .list_defaults import list_defaults
from .init_turb_vel_fluctuations import init_turb_vel_fluctuations
from .show_iterations_sampled import show_iterations_sampled
from .show_time_sampled import show_time_sampled
from .levelset_auto_init import levelset_auto_init
class initialization(Group):
    """
    'initialization' child.
    """

    fluent_name = "initialization"

    child_names = \
        ['fmg_initialize', 'localized_turb_init', 'reference_frame',
         'fmg_options', 'hybrid_init_options', 'patch', 'set_defaults',
         'open_channel_auto_init', 'fmg_initialization',
         'initialization_type']

    fmg_initialize: fmg_initialize = fmg_initialize
    """
    fmg_initialize child of initialization.
    """
    localized_turb_init: localized_turb_init = localized_turb_init
    """
    localized_turb_init child of initialization.
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of initialization.
    """
    fmg_options: fmg_options = fmg_options
    """
    fmg_options child of initialization.
    """
    hybrid_init_options: hybrid_init_options = hybrid_init_options
    """
    hybrid_init_options child of initialization.
    """
    patch: patch = patch
    """
    patch child of initialization.
    """
    set_defaults: set_defaults = set_defaults
    """
    set_defaults child of initialization.
    """
    open_channel_auto_init: open_channel_auto_init = open_channel_auto_init
    """
    open_channel_auto_init child of initialization.
    """
    fmg_initialization: fmg_initialization = fmg_initialization
    """
    fmg_initialization child of initialization.
    """
    initialization_type: initialization_type = initialization_type
    """
    initialization_type child of initialization.
    """
    command_names = \
        ['standard_initialize', 'hybrid_initialize', 'initialize',
         'dpm_reset', 'lwf_reset', 'init_flow_statistics',
         'init_acoustics_options', 'list_defaults',
         'init_turb_vel_fluctuations', 'show_iterations_sampled',
         'show_time_sampled', 'levelset_auto_init']

    standard_initialize: standard_initialize = standard_initialize
    """
    standard_initialize command of initialization.
    """
    hybrid_initialize: hybrid_initialize = hybrid_initialize
    """
    hybrid_initialize command of initialization.
    """
    initialize: initialize = initialize
    """
    initialize command of initialization.
    """
    dpm_reset: dpm_reset = dpm_reset
    """
    dpm_reset command of initialization.
    """
    lwf_reset: lwf_reset = lwf_reset
    """
    lwf_reset command of initialization.
    """
    init_flow_statistics: init_flow_statistics = init_flow_statistics
    """
    init_flow_statistics command of initialization.
    """
    init_acoustics_options: init_acoustics_options = init_acoustics_options
    """
    init_acoustics_options command of initialization.
    """
    list_defaults: list_defaults = list_defaults
    """
    list_defaults command of initialization.
    """
    init_turb_vel_fluctuations: init_turb_vel_fluctuations = init_turb_vel_fluctuations
    """
    init_turb_vel_fluctuations command of initialization.
    """
    show_iterations_sampled: show_iterations_sampled = show_iterations_sampled
    """
    show_iterations_sampled command of initialization.
    """
    show_time_sampled: show_time_sampled = show_time_sampled
    """
    show_time_sampled command of initialization.
    """
    levelset_auto_init: levelset_auto_init = levelset_auto_init
    """
    levelset_auto_init command of initialization.
    """
