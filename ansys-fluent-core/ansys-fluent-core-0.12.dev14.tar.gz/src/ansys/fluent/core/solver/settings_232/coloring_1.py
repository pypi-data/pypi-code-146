#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .automatic import automatic
from .manual import manual
class coloring(Group):
    """
    'coloring' child.
    """

    fluent_name = "coloring"

    child_names = \
        ['option', 'automatic', 'manual']

    option: option = option
    """
    option child of coloring.
    """
    automatic: automatic = automatic
    """
    automatic child of coloring.
    """
    manual: manual = manual
    """
    manual child of coloring.
    """
