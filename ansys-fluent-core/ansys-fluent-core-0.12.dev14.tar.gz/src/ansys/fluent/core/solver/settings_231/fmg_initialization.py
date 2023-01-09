#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fmg_courant_number import fmg_courant_number
from .enable_fmg_verbose import enable_fmg_verbose
from .customize_fmg_initialization import customize_fmg_initialization
class fmg_initialization(Group):
    """
    Enter the set full-multigrid for initialization menu.
    """

    fluent_name = "fmg-initialization"

    child_names = \
        ['fmg_courant_number', 'enable_fmg_verbose']

    fmg_courant_number: fmg_courant_number = fmg_courant_number
    """
    fmg_courant_number child of fmg_initialization.
    """
    enable_fmg_verbose: enable_fmg_verbose = enable_fmg_verbose
    """
    enable_fmg_verbose child of fmg_initialization.
    """
    command_names = \
        ['customize_fmg_initialization']

    customize_fmg_initialization: customize_fmg_initialization = customize_fmg_initialization
    """
    customize_fmg_initialization command of fmg_initialization.
    """
