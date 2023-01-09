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
class direction_2_x(Group):
    """
    'direction_2_x' child.
    """

    fluent_name = "direction-2-x"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of direction_2_x.
    """
    value: value = value
    """
    value child of direction_2_x.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of direction_2_x.
    """
    field_name: field_name = field_name
    """
    field_name child of direction_2_x.
    """
    udf: udf = udf
    """
    udf child of direction_2_x.
    """
