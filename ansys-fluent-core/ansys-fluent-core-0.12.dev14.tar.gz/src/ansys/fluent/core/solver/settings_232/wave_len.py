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
class wave_len(Group):
    """
    'wave_len' child.
    """

    fluent_name = "wave-len"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of wave_len.
    """
    value: value = value
    """
    value child of wave_len.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of wave_len.
    """
    field_name: field_name = field_name
    """
    field_name child of wave_len.
    """
    udf: udf = udf
    """
    udf child of wave_len.
    """
