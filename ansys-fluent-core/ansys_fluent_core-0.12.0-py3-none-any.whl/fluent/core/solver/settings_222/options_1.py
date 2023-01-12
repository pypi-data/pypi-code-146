#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .verbosity import verbosity
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['verbosity']

    verbosity: verbosity = verbosity
    """
    verbosity child of options.
    """
