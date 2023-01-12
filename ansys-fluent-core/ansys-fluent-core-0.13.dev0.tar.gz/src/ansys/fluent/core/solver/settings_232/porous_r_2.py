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
class porous_r_2(Group):
    """
    'porous_r_2' child.
    """

    fluent_name = "porous-r-2"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of porous_r_2.
    """
    value: value = value
    """
    value child of porous_r_2.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of porous_r_2.
    """
    field_name: field_name = field_name
    """
    field_name child of porous_r_2.
    """
    udf: udf = udf
    """
    udf child of porous_r_2.
    """
