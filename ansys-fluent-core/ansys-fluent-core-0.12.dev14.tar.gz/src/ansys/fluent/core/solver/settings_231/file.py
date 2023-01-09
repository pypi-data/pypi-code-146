#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .single_precision_coordinates import single_precision_coordinates
from .binary_legacy_files import binary_legacy_files
from .cff_files import cff_files
from .async_optimize import async_optimize
from .write_pdat import write_pdat
from .confirm_overwrite import confirm_overwrite
from .export import export
from .import_ import import_
from .parametric_project import parametric_project
from .auto_save import auto_save
from .define_macro import define_macro
from .read_1 import read
from .read_case import read_case
from .read_case_data import read_case_data
from .read_case_setting import read_case_setting
from .read_data import read_data
from .read_mesh import read_mesh
from .read_journal import read_journal
from .start_journal import start_journal
from .stop_journal import stop_journal
from .replace_mesh import replace_mesh
from .write import write
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    child_names = \
        ['single_precision_coordinates', 'binary_legacy_files', 'cff_files',
         'async_optimize', 'write_pdat', 'confirm_overwrite', 'export',
         'import_', 'parametric_project']

    single_precision_coordinates: single_precision_coordinates = single_precision_coordinates
    """
    single_precision_coordinates child of file.
    """
    binary_legacy_files: binary_legacy_files = binary_legacy_files
    """
    binary_legacy_files child of file.
    """
    cff_files: cff_files = cff_files
    """
    cff_files child of file.
    """
    async_optimize: async_optimize = async_optimize
    """
    async_optimize child of file.
    """
    write_pdat: write_pdat = write_pdat
    """
    write_pdat child of file.
    """
    confirm_overwrite: confirm_overwrite = confirm_overwrite
    """
    confirm_overwrite child of file.
    """
    export: export = export
    """
    export child of file.
    """
    import_: import_ = import_
    """
    import_ child of file.
    """
    parametric_project: parametric_project = parametric_project
    """
    parametric_project child of file.
    """
    command_names = \
        ['auto_save', 'define_macro', 'read', 'read_case', 'read_case_data',
         'read_case_setting', 'read_data', 'read_mesh', 'read_journal',
         'start_journal', 'stop_journal', 'replace_mesh', 'write']

    auto_save: auto_save = auto_save
    """
    auto_save command of file.
    """
    define_macro: define_macro = define_macro
    """
    define_macro command of file.
    """
    read: read = read
    """
    read command of file.
    """
    read_case: read_case = read_case
    """
    read_case command of file.
    """
    read_case_data: read_case_data = read_case_data
    """
    read_case_data command of file.
    """
    read_case_setting: read_case_setting = read_case_setting
    """
    read_case_setting command of file.
    """
    read_data: read_data = read_data
    """
    read_data command of file.
    """
    read_mesh: read_mesh = read_mesh
    """
    read_mesh command of file.
    """
    read_journal: read_journal = read_journal
    """
    read_journal command of file.
    """
    start_journal: start_journal = start_journal
    """
    start_journal command of file.
    """
    stop_journal: stop_journal = stop_journal
    """
    stop_journal command of file.
    """
    replace_mesh: replace_mesh = replace_mesh
    """
    replace_mesh command of file.
    """
    write: write = write
    """
    write command of file.
    """
