#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .execute_commands import execute_commands
from .solution_animations import solution_animations
from .poor_mesh_numerics import poor_mesh_numerics
from .enable_strategy import enable_strategy
from .copy_modification import copy_modification
from .delete_modification import delete_modification
from .enable_modification import enable_modification
from .disable_modification import disable_modification
from .import_modifications import import_modifications
from .export_modifications import export_modifications
from .continue_strategy_execution import continue_strategy_execution
class calculation_activity(Group):
    """
    'calculation_activity' child.
    """

    fluent_name = "calculation-activity"

    child_names = \
        ['execute_commands', 'solution_animations', 'poor_mesh_numerics']

    execute_commands: execute_commands = execute_commands
    """
    execute_commands child of calculation_activity.
    """
    solution_animations: solution_animations = solution_animations
    """
    solution_animations child of calculation_activity.
    """
    poor_mesh_numerics: poor_mesh_numerics = poor_mesh_numerics
    """
    poor_mesh_numerics child of calculation_activity.
    """
    command_names = \
        ['enable_strategy', 'copy_modification', 'delete_modification',
         'enable_modification', 'disable_modification',
         'import_modifications', 'export_modifications',
         'continue_strategy_execution']

    enable_strategy: enable_strategy = enable_strategy
    """
    enable_strategy command of calculation_activity.
    """
    copy_modification: copy_modification = copy_modification
    """
    copy_modification command of calculation_activity.
    """
    delete_modification: delete_modification = delete_modification
    """
    delete_modification command of calculation_activity.
    """
    enable_modification: enable_modification = enable_modification
    """
    enable_modification command of calculation_activity.
    """
    disable_modification: disable_modification = disable_modification
    """
    disable_modification command of calculation_activity.
    """
    import_modifications: import_modifications = import_modifications
    """
    import_modifications command of calculation_activity.
    """
    export_modifications: export_modifications = export_modifications
    """
    export_modifications command of calculation_activity.
    """
    continue_strategy_execution: continue_strategy_execution = continue_strategy_execution
    """
    continue_strategy_execution command of calculation_activity.
    """
