#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .scheme import scheme
from .low_order_scheme import low_order_scheme
from .high_order_scheme import high_order_scheme
from .accuracy_control import accuracy_control
class tracking(Group):
    """
    'tracking' child.
    """

    fluent_name = "tracking"

    child_names = \
        ['scheme', 'low_order_scheme', 'high_order_scheme',
         'accuracy_control']

    scheme: scheme = scheme
    """
    scheme child of tracking.
    """
    low_order_scheme: low_order_scheme = low_order_scheme
    """
    low_order_scheme child of tracking.
    """
    high_order_scheme: high_order_scheme = high_order_scheme
    """
    high_order_scheme child of tracking.
    """
    accuracy_control: accuracy_control = accuracy_control
    """
    accuracy_control child of tracking.
    """
