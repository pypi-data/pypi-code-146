#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .const_htc import const_htc
from .const_nu import const_nu
class heat_transfer(Group):
    """
    'heat_transfer' child.
    """

    fluent_name = "heat-transfer"

    child_names = \
        ['option', 'const_htc', 'const_nu']

    option: option = option
    """
    option child of heat_transfer.
    """
    const_htc: const_htc = const_htc
    """
    const_htc child of heat_transfer.
    """
    const_nu: const_nu = const_nu
    """
    const_nu child of heat_transfer.
    """
