#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .mod_name import mod_name
class delete_modification(Command):
    """
    Delete a single case modification.
    
    Parameters
    ----------
        mod_name : str
            'mod_name' child.
    
    """

    fluent_name = "delete-modification"

    argument_names = \
        ['mod_name']

    mod_name: mod_name = mod_name
    """
    mod_name argument of delete_modification.
    """
