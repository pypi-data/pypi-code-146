#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .filename import filename
class read_views(Command):
    """
    Read views from a view file.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "read-views"

    argument_names = \
        ['filename']

    filename: filename = filename
    """
    filename argument of read_views.
    """
