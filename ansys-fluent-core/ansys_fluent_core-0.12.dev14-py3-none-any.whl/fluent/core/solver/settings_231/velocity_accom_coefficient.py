#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class velocity_accom_coefficient(Group):
    """
    'velocity_accom_coefficient' child.
    """

    fluent_name = "velocity-accom-coefficient"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of velocity_accom_coefficient.
    """
    value: value = value
    """
    value child of velocity_accom_coefficient.
    """
