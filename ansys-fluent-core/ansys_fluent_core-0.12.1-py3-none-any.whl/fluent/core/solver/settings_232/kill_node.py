#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .compute_node import compute_node
from .invalidate_case import invalidate_case
class kill_node(Command):
    """
    'kill_node' command.
    
    Parameters
    ----------
        compute_node : int
            'compute_node' child.
        invalidate_case : bool
            'invalidate_case' child.
    
    """

    fluent_name = "kill-node"

    argument_names = \
        ['compute_node', 'invalidate_case']

    compute_node: compute_node = compute_node
    """
    compute_node argument of kill_node.
    """
    invalidate_case: invalidate_case = invalidate_case
    """
    invalidate_case argument of kill_node.
    """
