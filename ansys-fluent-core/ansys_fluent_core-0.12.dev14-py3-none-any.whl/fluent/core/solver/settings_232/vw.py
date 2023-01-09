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
class vw(Group):
    """
    'vw' child.
    """

    fluent_name = "vw"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of vw.
    """
    value: value = value
    """
    value child of vw.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of vw.
    """
    field_name: field_name = field_name
    """
    field_name child of vw.
    """
    udf: udf = udf
    """
    udf child of vw.
    """
