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
class targeted_mf_pmax(Group):
    """
    'targeted_mf_pmax' child.
    """

    fluent_name = "targeted-mf-pmax"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of targeted_mf_pmax.
    """
    value: value = value
    """
    value child of targeted_mf_pmax.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of targeted_mf_pmax.
    """
    field_name: field_name = field_name
    """
    field_name child of targeted_mf_pmax.
    """
    udf: udf = udf
    """
    udf child of targeted_mf_pmax.
    """
