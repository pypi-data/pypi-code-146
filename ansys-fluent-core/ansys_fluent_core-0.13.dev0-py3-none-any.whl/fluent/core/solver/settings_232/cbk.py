#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .char_intrinsic_reactivity import char_intrinsic_reactivity
from .carbon_content_percentage import carbon_content_percentage
class cbk(Group):
    """
    'cbk' child.
    """

    fluent_name = "cbk"

    child_names = \
        ['option', 'char_intrinsic_reactivity', 'carbon_content_percentage']

    option: option = option
    """
    option child of cbk.
    """
    char_intrinsic_reactivity: char_intrinsic_reactivity = char_intrinsic_reactivity
    """
    char_intrinsic_reactivity child of cbk.
    """
    carbon_content_percentage: carbon_content_percentage = carbon_content_percentage
    """
    carbon_content_percentage child of cbk.
    """
