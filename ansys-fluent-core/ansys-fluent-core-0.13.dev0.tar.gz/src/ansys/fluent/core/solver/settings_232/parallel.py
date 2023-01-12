#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_4 import option
from .expert_options import expert_options
from .hybrid_options import hybrid_options
class parallel(Group):
    """
    Main menu to allow users to set options controlling the parallel scheme used when tracking particles. 
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "parallel"

    child_names = \
        ['option', 'expert_options', 'hybrid_options']

    option: option = option
    """
    option child of parallel.
    """
    expert_options: expert_options = expert_options
    """
    expert_options child of parallel.
    """
    hybrid_options: hybrid_options = hybrid_options
    """
    hybrid_options child of parallel.
    """
