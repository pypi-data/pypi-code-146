#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .iterate_1 import iterate
from .dual_time_iterate_1 import dual_time_iterate
class solve(Group):
    """
    'solve' child.
    """

    fluent_name = "solve"

    command_names = \
        ['iterate', 'dual_time_iterate']

    iterate: iterate = iterate
    """
    iterate command of solve.
    """
    dual_time_iterate: dual_time_iterate = dual_time_iterate
    """
    dual_time_iterate command of solve.
    """
