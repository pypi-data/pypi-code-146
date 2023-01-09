#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .re_randomize_every_iteration import re_randomize_every_iteration
from .re_randomize_every_timestep import re_randomize_every_timestep
from .tracking_statistics_format import tracking_statistics_format
from .verbosity_1 import verbosity
class expert_options(Group):
    """
    Menu containing not frequently used (expert level) settings.
    """

    fluent_name = "expert-options"

    child_names = \
        ['re_randomize_every_iteration', 're_randomize_every_timestep',
         'tracking_statistics_format', 'verbosity']

    re_randomize_every_iteration: re_randomize_every_iteration = re_randomize_every_iteration
    """
    re_randomize_every_iteration child of expert_options.
    """
    re_randomize_every_timestep: re_randomize_every_timestep = re_randomize_every_timestep
    """
    re_randomize_every_timestep child of expert_options.
    """
    tracking_statistics_format: tracking_statistics_format = tracking_statistics_format
    """
    tracking_statistics_format child of expert_options.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of expert_options.
    """
