#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .register_name import register_name
class list_properties(Command):
    """
    List the properties of a definition for automatic poor mesh numerics.
    
    Parameters
    ----------
        register_name : str
            'register_name' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['register_name']

    register_name: register_name = register_name
    """
    register_name argument of list_properties.
    """
