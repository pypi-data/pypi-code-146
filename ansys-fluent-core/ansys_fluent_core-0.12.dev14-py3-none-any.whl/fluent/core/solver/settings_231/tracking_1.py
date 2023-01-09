#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_high_res_tracking import enable_high_res_tracking
from .expert_options_1 import expert_options
from .high_res_tracking_options import high_res_tracking_options
from .tracking_parameters import tracking_parameters
from .track_in_absolute_frame import track_in_absolute_frame
class tracking(Group):
    """
    Main menu to control the time integration of the particle trajectory equations.
    """

    fluent_name = "tracking"

    child_names = \
        ['enable_high_res_tracking', 'expert_options',
         'high_res_tracking_options', 'tracking_parameters',
         'track_in_absolute_frame']

    enable_high_res_tracking: enable_high_res_tracking = enable_high_res_tracking
    """
    enable_high_res_tracking child of tracking.
    """
    expert_options: expert_options = expert_options
    """
    expert_options child of tracking.
    """
    high_res_tracking_options: high_res_tracking_options = high_res_tracking_options
    """
    high_res_tracking_options child of tracking.
    """
    tracking_parameters: tracking_parameters = tracking_parameters
    """
    tracking_parameters child of tracking.
    """
    track_in_absolute_frame: track_in_absolute_frame = track_in_absolute_frame
    """
    track_in_absolute_frame child of tracking.
    """
