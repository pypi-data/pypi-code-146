import os
import sys

from .patch_config import (
    disable_kite_startup_dialog,
    disable_update_checks,
    patch_config_folder,
    patch_splash_screen,
    set_remote_interpreter_startup_file,
    set_remote_python_interpreter,
    set_scripts_home_folder,
    set_spyder_theme,
    silence_umr,
)
from .patch_gui import (
    activate_file_browser,
    patch_console_startup,
    patch_double_click_variable_explorer,
    patch_editor_code_completion,
    patch_in_prompt,
)
from .patch_remote_kernel_startup import set_banner, set_emzed_spyder_kernels
from .utils import setup_venv_for_remote_interpreter

remote_executable = setup_venv_for_remote_interpreter()

if os.environ.get("SPYDER_PYTEST") is not None:
    sys.exit(0)

# order matters, if we'd run set_remote_python_interpreter eariler, patching the configs
# would not work!

# reason: patching only works for data which is not imported into spyder already


def step_1():
    patch_config_folder()
    patch_splash_screen()
    set_spyder_theme()
    disable_kite_startup_dialog()
    disable_update_checks()
    silence_umr()
    set_remote_interpreter_startup_file()


def step_2():
    set_remote_python_interpreter(remote_executable)


def step_3():
    patch_double_click_variable_explorer()
    patch_editor_code_completion()
    set_scripts_home_folder()
    activate_file_browser()
    set_emzed_spyder_kernels()
    patch_console_startup()
    set_banner(remote_executable)
    patch_in_prompt()


step_1()
step_2()
step_3()

# SHELL can cause issues with restart on windows
if "SHELL" in os.environ and sys.platform == "win32":
    del os.environ["SHELL"]
