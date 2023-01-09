#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_9 import enable
from .disable_1 import disable
from .copy_2 import copy
from .delete_1 import delete
from .export_1 import export
from .import__1 import import_
class execute_commands(Group):
    """
    'execute_commands' child.
    """

    fluent_name = "execute-commands"

    command_names = \
        ['enable', 'disable', 'copy', 'delete', 'export', 'import_']

    enable: enable = enable
    """
    enable command of execute_commands.
    """
    disable: disable = disable
    """
    disable command of execute_commands.
    """
    copy: copy = copy
    """
    copy command of execute_commands.
    """
    delete: delete = delete
    """
    delete command of execute_commands.
    """
    export: export = export
    """
    export command of execute_commands.
    """
    import_: import_ = import_
    """
    import_ command of execute_commands.
    """
