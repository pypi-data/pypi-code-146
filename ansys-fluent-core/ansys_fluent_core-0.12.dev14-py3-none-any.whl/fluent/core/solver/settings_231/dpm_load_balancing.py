#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .load_balancing import load_balancing
from .threshold import threshold
from .interval import interval
class dpm_load_balancing(Group):
    """
    Enable automatic load balancing for DPM.
    """

    fluent_name = "dpm-load-balancing"

    child_names = \
        ['load_balancing', 'threshold', 'interval']

    load_balancing: load_balancing = load_balancing
    """
    load_balancing child of dpm_load_balancing.
    """
    threshold: threshold = threshold
    """
    threshold child of dpm_load_balancing.
    """
    interval: interval = interval
    """
    interval child of dpm_load_balancing.
    """
