"""
Allows setting environment variables and the path.
"""

# pylint: disable=missing-function-docstring,import-outside-toplevel,invalid-name,unused-argument,protected-access,c-extension-no-member

import sys
import os
from pathlib import Path


def broadcast_env_change():
    if sys.platform == "win32":
        import win32con  # type: ignore
        import win32gui  # type: ignore

        SendMessageTimeout = win32gui.SendMessageTimeout  # type: ignore
        SendMessageTimeout(
            win32con.HWND_BROADCAST,
            win32con.WM_SETTINGCHANGE,
            0,
            "Environment",
            win32con.SMTO_ABORTIFHUNG,
            5000,
        )
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")


def add_system_path(new_path: Path):
    if sys.platform == "win32":
        import windowspathadder.windowspathadder  # type: ignore

        print(f"Adding {new_path} to Windows PATH")

        def null_print(*args, **kwargs):
            pass

        windowspathadder.windowspathadder._print = null_print
        windowspathadder.add_windows_path(str(new_path))
        os.environ["PATH"] += os.pathsep + str(new_path)
        broadcast_env_change()
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")


def set_env_var(var_name, var_value):
    assert var_name.lower() != "path", "Use add_system_path instead"
    var_name = str(var_name)
    var_value = str(var_value)
    if sys.platform == "win32":
        import winreg

        print(f"Setting {var_name} to {var_value}")
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS
        )
        winreg.SetValueEx(key, var_name, 0, winreg.REG_SZ, var_value)
        winreg.CloseKey(key)
        broadcast_env_change()
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")
