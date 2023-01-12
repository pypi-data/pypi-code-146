#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .state_name import state_name
class restore_state(Command):
    """
    Apply a display state to the active window.
    
    Parameters
    ----------
        state_name : str
            'state_name' child.
    
    """

    fluent_name = "restore-state"

    argument_names = \
        ['state_name']

    state_name: state_name = state_name
    """
    state_name argument of restore_state.
    """
