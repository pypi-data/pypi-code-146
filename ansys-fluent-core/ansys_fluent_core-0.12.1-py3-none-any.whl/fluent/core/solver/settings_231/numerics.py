#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .averaging import averaging
from .source_terms import source_terms
from .tracking import tracking
class numerics(Group):
    """
    Main menu to allow users to set options controlling the solution of ordinary differential equations describing 
    the underlying physics of the Discrete Phase Model.
    For more details consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "numerics"

    child_names = \
        ['averaging', 'source_terms', 'tracking']

    averaging: averaging = averaging
    """
    averaging child of numerics.
    """
    source_terms: source_terms = source_terms
    """
    source_terms child of numerics.
    """
    tracking: tracking = tracking
    """
    tracking child of numerics.
    """
