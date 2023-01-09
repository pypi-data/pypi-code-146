#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
class list_properties(Command):
    """
    List the properties of a locally-stored material.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['name']

    name: name = name
    """
    name argument of list_properties.
    """
