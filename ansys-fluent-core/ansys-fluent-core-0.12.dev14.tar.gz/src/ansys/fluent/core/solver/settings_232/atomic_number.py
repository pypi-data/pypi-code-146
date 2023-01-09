#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class atomic_number(Group):
    """
    'atomic_number' child.
    """

    fluent_name = "atomic-number"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of atomic_number.
    """
    value: value = value
    """
    value child of atomic_number.
    """
