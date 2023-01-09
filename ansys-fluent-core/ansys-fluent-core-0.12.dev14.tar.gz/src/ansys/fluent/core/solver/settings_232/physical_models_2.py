#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use_multi_physics import use_multi_physics
from .threshold import threshold
from .interval import interval
class physical_models(Group):
    """
    Use physical-models load balancing?.
    """

    fluent_name = "physical-models"

    child_names = \
        ['use_multi_physics', 'threshold', 'interval']

    use_multi_physics: use_multi_physics = use_multi_physics
    """
    use_multi_physics child of physical_models.
    """
    threshold: threshold = threshold
    """
    threshold child of physical_models.
    """
    interval: interval = interval
    """
    interval child of physical_models.
    """
