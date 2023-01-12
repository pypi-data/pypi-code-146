#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option import option
from .update_sources_every_flow_iteration import update_sources_every_flow_iteration
from .iteration_interval import iteration_interval
class interaction(Group):
    """
    'interaction' child.
    """

    fluent_name = "interaction"

    child_names = \
        ['option', 'update_sources_every_flow_iteration',
         'iteration_interval']

    option: option = option
    """
    option child of interaction.
    """
    update_sources_every_flow_iteration: update_sources_every_flow_iteration = update_sources_every_flow_iteration
    """
    update_sources_every_flow_iteration child of interaction.
    """
    iteration_interval: iteration_interval = iteration_interval
    """
    iteration_interval child of interaction.
    """
