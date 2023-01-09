#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class reference_temperature(Group):
    """
    'reference_temperature' child.
    """

    fluent_name = "reference-temperature"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of reference_temperature.
    """
    value: value = value
    """
    value child of reference_temperature.
    """
