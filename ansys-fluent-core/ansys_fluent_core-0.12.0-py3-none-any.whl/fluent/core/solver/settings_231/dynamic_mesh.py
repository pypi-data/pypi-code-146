#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use import use
from .auto_1 import auto
from .threshold import threshold
from .interval import interval
class dynamic_mesh(Group):
    """
    Use load balancing for dynamic mesh?.
    """

    fluent_name = "dynamic-mesh"

    child_names = \
        ['use', 'auto', 'threshold', 'interval']

    use: use = use
    """
    use child of dynamic_mesh.
    """
    auto: auto = auto
    """
    auto child of dynamic_mesh.
    """
    threshold: threshold = threshold
    """
    threshold child of dynamic_mesh.
    """
    interval: interval = interval
    """
    interval child of dynamic_mesh.
    """
