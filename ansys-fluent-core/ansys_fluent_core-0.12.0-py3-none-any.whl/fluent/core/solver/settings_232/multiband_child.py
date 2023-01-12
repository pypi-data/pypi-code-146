#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .start_1 import start
from .end import end
class multiband_child(Group):
    """
    'child_object_type' of multiband.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['start', 'end']

    start: start = start
    """
    start child of multiband_child.
    """
    end: end = end
    """
    end child of multiband_child.
    """
