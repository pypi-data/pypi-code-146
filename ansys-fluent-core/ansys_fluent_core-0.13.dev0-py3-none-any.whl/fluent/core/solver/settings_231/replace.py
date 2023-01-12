#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name import name
from .zones import zones
class replace(Command):
    """
    Replace mesh and interpolate data.
    
    Parameters
    ----------
        name : str
            'name' child.
        zones : bool
            'zones' child.
    
    """

    fluent_name = "replace"

    argument_names = \
        ['name', 'zones']

    name: name = name
    """
    name argument of replace.
    """
    zones: zones = zones
    """
    zones argument of replace.
    """
