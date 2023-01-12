#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable import enable
class dynamic_adaption(Command):
    """
    Adapt the mesh during solution.
    
    Parameters
    ----------
        enable : bool
            'enable' child.
    
    """

    fluent_name = "dynamic-adaption?"

    argument_names = \
        ['enable']

    enable: enable = enable
    """
    enable argument of dynamic_adaption.
    """
