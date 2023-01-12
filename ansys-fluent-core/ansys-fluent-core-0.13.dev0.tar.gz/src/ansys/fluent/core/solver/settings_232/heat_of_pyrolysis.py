#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class heat_of_pyrolysis(Group):
    """
    'heat_of_pyrolysis' child.
    """

    fluent_name = "heat-of-pyrolysis"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of heat_of_pyrolysis.
    """
    value: value = value
    """
    value child of heat_of_pyrolysis.
    """
