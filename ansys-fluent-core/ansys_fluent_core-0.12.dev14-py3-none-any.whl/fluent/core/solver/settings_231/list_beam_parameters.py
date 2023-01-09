#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .beam_name_1 import beam_name
class list_beam_parameters(Command):
    """
    List parameters of optical beam grid.
    
    Parameters
    ----------
        beam_name : str
            Choose the name for the optical beam to be listed.
    
    """

    fluent_name = "list-beam-parameters"

    argument_names = \
        ['beam_name']

    beam_name: beam_name = beam_name
    """
    beam_name argument of list_beam_parameters.
    """
