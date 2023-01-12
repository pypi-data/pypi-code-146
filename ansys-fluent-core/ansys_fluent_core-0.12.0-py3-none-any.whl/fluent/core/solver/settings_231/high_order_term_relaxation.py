#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_5 import enable
from .options_3 import options
class high_order_term_relaxation(Group):
    """
    Enter High Order Relaxation Menu.
    """

    fluent_name = "high-order-term-relaxation"

    child_names = \
        ['enable', 'options']

    enable: enable = enable
    """
    enable child of high_order_term_relaxation.
    """
    options: options = options
    """
    options child of high_order_term_relaxation.
    """
