#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .end_of_timestep import end_of_timestep
class interrupt(Command):
    """
    Interrupt the iterations.
    
    Parameters
    ----------
        end_of_timestep : bool
            'end_of_timestep' child.
    
    """

    fluent_name = "interrupt"

    argument_names = \
        ['end_of_timestep']

    end_of_timestep: end_of_timestep = end_of_timestep
    """
    end_of_timestep argument of interrupt.
    """
