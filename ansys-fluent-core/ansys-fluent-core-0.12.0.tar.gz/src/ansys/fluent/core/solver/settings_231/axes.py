#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .numbers import numbers
from .rules import rules
from .log_scale_1 import log_scale
from .auto_scale_1 import auto_scale
from .labels import labels
class axes(Group):
    """
    'axes' child.
    """

    fluent_name = "axes"

    child_names = \
        ['numbers', 'rules', 'log_scale', 'auto_scale', 'labels']

    numbers: numbers = numbers
    """
    numbers child of axes.
    """
    rules: rules = rules
    """
    rules child of axes.
    """
    log_scale: log_scale = log_scale
    """
    log_scale child of axes.
    """
    auto_scale: auto_scale = auto_scale
    """
    auto_scale child of axes.
    """
    labels: labels = labels
    """
    labels child of axes.
    """
