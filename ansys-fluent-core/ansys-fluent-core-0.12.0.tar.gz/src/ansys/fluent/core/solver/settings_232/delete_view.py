#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .view_name import view_name
class delete_view(Command):
    """
    Remove a view from the list.
    
    Parameters
    ----------
        view_name : str
            'view_name' child.
    
    """

    fluent_name = "delete-view"

    argument_names = \
        ['view_name']

    view_name: view_name = view_name
    """
    view_name argument of delete_view.
    """
