#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .reset_color import reset_color
class reset(Command):
    """
    To reset colors and/or materials to the defaults.
    
    Parameters
    ----------
        reset_color : bool
            'reset_color' child.
    
    """

    fluent_name = "reset?"

    argument_names = \
        ['reset_color']

    reset_color: reset_color = reset_color
    """
    reset_color argument of reset.
    """
