#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class magnetic_permeability(Group):
    """
    'magnetic_permeability' child.
    """

    fluent_name = "magnetic-permeability"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of magnetic_permeability.
    """
    value: value = value
    """
    value child of magnetic_permeability.
    """
