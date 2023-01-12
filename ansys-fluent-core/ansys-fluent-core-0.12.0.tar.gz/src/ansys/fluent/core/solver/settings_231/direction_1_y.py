#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .value import value
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class direction_1_y(Group):
    """
    'direction_1_y' child.
    """

    fluent_name = "direction-1-y"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of direction_1_y.
    """
    value: value = value
    """
    value child of direction_1_y.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of direction_1_y.
    """
    field_name: field_name = field_name
    """
    field_name child of direction_1_y.
    """
    udf: udf = udf
    """
    udf child of direction_1_y.
    """
