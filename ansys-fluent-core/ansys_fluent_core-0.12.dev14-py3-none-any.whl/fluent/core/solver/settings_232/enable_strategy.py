#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable import enable
class enable_strategy(Command):
    """
    Specify whether automatic initialization and case modification should be enabled.
    
    Parameters
    ----------
        enable : bool
            'enable' child.
    
    """

    fluent_name = "enable-strategy?"

    argument_names = \
        ['enable']

    enable: enable = enable
    """
    enable argument of enable_strategy.
    """
