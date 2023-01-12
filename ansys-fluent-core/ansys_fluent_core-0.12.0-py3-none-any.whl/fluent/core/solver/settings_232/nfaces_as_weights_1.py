#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .nfaces_as_weights import nfaces_as_weights
from .user_defined_value import user_defined_value
from .value import value
class nfaces_as_weights(Group):
    """
    Use number of faces as weights.
    """

    fluent_name = "nfaces-as-weights"

    child_names = \
        ['nfaces_as_weights', 'user_defined_value', 'value']

    nfaces_as_weights: nfaces_as_weights = nfaces_as_weights
    """
    nfaces_as_weights child of nfaces_as_weights.
    """
    user_defined_value: user_defined_value = user_defined_value
    """
    user_defined_value child of nfaces_as_weights.
    """
    value: value = value
    """
    value child of nfaces_as_weights.
    """
