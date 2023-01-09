#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class burn_hreact(Group):
    """
    'burn_hreact' child.
    """

    fluent_name = "burn-hreact"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of burn_hreact.
    """
    value: value = value
    """
    value child of burn_hreact.
    """
