#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .filename import filename
class define_macro(Command):
    """
    Save input to a named macro.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "define-macro"

    argument_names = \
        ['filename']

    filename: filename = filename
    """
    filename argument of define_macro.
    """
