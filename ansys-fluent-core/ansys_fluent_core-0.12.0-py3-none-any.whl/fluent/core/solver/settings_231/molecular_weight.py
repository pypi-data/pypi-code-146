#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .rgp_table import rgp_table
class molecular_weight(Group):
    """
    'molecular_weight' child.
    """

    fluent_name = "molecular-weight"

    child_names = \
        ['option', 'value', 'rgp_table']

    option: option = option
    """
    option child of molecular_weight.
    """
    value: value = value
    """
    value child of molecular_weight.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of molecular_weight.
    """
