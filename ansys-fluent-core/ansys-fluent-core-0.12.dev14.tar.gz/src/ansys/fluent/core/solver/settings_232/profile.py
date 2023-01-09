#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_1 import enable
from .disable import disable
from .print import print
from .clear import clear
class profile(Group):
    """
    Enter the adaption profile menu.
    """

    fluent_name = "profile"

    command_names = \
        ['enable', 'disable', 'print', 'clear']

    enable: enable = enable
    """
    enable command of profile.
    """
    disable: disable = disable
    """
    disable command of profile.
    """
    print: print = print
    """
    print command of profile.
    """
    clear: clear = clear
    """
    clear command of profile.
    """
