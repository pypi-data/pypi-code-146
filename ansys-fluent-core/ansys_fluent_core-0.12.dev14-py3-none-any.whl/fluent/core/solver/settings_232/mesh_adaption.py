#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use import use
from .threshold import threshold
class mesh_adaption(Group):
    """
    Use load balancing for mesh adaption?.
    """

    fluent_name = "mesh-adaption"

    child_names = \
        ['use', 'threshold']

    use: use = use
    """
    use child of mesh_adaption.
    """
    threshold: threshold = threshold
    """
    threshold child of mesh_adaption.
    """
