#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .default import default
from .reverse import reverse
class curve_length(Group):
    """
    'curve_length' child.
    """

    fluent_name = "curve-length"

    child_names = \
        ['option', 'default', 'reverse']

    option: option = option
    """
    option child of curve_length.
    """
    default: default = default
    """
    default child of curve_length.
    """
    reverse: reverse = reverse
    """
    reverse child of curve_length.
    """
