#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

import os
import re
import subprocess
import sys
from datetime import datetime

from .utils import (
    active_python_exe,
    emzed_projects,
    get_active_project,
    is_valid_project,
    python_executable_in,
    update_active_project,
)


def set_emzed_spyder_kernels():
    import spyder.plugins.ipythonconsole.utils.kernelspec as kernelspec

    class PatchedKernelSpec(kernelspec.SpyderKernelSpec):
        def __init__(self, is_cython=False, is_pylab=False, is_sympy=False, **kwargs):

            kernelspec.KernelSpec.__init__(self, **kwargs)
            self.is_cython = is_cython
            self.is_pylab = is_pylab
            self.is_sympy = is_sympy

            self.display_name = "Python 3 (emzed.spyder)"
            self.language = "python3"
            self.resource_dir = ""

        @property
        def argv(self):
            result = super().argv

            update_active_project()
            active_project = get_active_project()
            if active_project and is_valid_project(active_project):
                python_exe = python_executable_in(
                    emzed_projects / active_project / ".venv"
                )
                if (
                    python_exe is not None
                    and python_exe.exists()
                    and os.access(python_exe, os.X_OK)
                ):
                    result[0] = str(python_exe)
            result[2] = "emzed_spyder_kernels"
            print(result, file=sys.__stderr__)
            return result

    kernelspec.SpyderKernelSpec = PatchedKernelSpec


ITALICS = "\033[0;3m"
RESET = "\033[0;0m"
BLUE_FG = "\033[0;34m"
RED_FG = "\033[0;31m"

LIGHT_GREEN_FG = "\033[1;32m"
WHITE_FG = "\033[1;37m"

WELCOME = r"""{FG_LOGO}                                 _
                                | |
     _____ ____  _____ _____  __| |
    | ___ |    \(___  ) ___ |/ _  |
    | ____| | | |/ __/| ____( (_| |
    |_____)_|_|_(_____)_____)\____|
{FG_TEXT}
{ITALICS}
      Copyright (c) 2020 ETH Zurich
             Scientific IT Services
              https://emzed.ethz.ch
{RESET}
run {ITALICS}emzed_help(){RESET} for an overview of
available functions.
"""

latest_version_check = None


def set_banner(remote_interpreter):
    from spyder.plugins.ipythonconsole.widgets.shell import (
        ShellWidget,
        create_qss_style,
    )

    def _banner_default(self, _orig=ShellWidget._banner_default):
        _, dark_fg = create_qss_style(self.syntax_style)
        if dark_fg:
            FG_LOGO = RED_FG
            FG_TEXT = BLUE_FG
        else:
            FG_LOGO = LIGHT_GREEN_FG
            FG_TEXT = WHITE_FG

        global latest_version_check

        active_project_exe = active_python_exe()
        if active_project_exe is not None:
            remote_interpreter = active_project_exe

        # only check versions at startup or at max once per day when one opens a new
        # console:
        if (
            latest_version_check is None
            or (datetime.now() - latest_version_check).days >= 1
        ):
            try:
                extra = "\n".join(update_message(remote_interpreter, FG_LOGO, FG_TEXT))
            except Exception:
                import traceback

                extra = traceback.format_exc()
            latest_version_check = datetime.now()
        else:
            extra = ""

        return (
            WELCOME.format(
                FG_LOGO=FG_LOGO, FG_TEXT=FG_TEXT, ITALICS=ITALICS, RESET=RESET
            )
            + extra
        )

    ShellWidget._banner_default = _banner_default


def update_message(remote_interpreter, color_logo, color_fg):
    lines = []
    found_new = False
    for (package, latest_version, local_version, error) in check_updates(
        remote_interpreter
    ):
        if error is not None:
            lines.append(
                color_logo + f"error when checking updates for {package}" f": {error}"
            )
        else:
            latest_str = ".".join(map(str, latest_version))
            if local_version < latest_version:
                line = color_fg + f"{package:10s}: new version {latest_str} available."
                found_new = True
                lines.append(line)

    if found_new:
        lines.append("")
        lines.append(f"please run {color_logo}emzed_update(){color_fg}")

    latest_emzed_spyder, current_emzed_spyder, msg = _check_emzed_spyder_update()
    if msg:
        lines.append("")
        lines.append(color_logo + msg)
    if (
        latest_emzed_spyder is not None
        and current_emzed_spyder is not None
        and latest_emzed_spyder > current_emzed_spyder
    ):
        lines.append(
            color_fg + f"emzed-spyder: new version {latest_emzed_spyder} available."
        )
        lines.append(
            color_logo
            + "you must close emzed.spyder first and then use pip to upgrade."
        )

    return lines


def check_updates(remote_interpreter):
    for package in ("emzed3", "emzed3_gui"):
        yield _check_update(remote_interpreter, package)


def _check_update(remote_interpreter, package):

    latest = _latest_version(remote_interpreter, package)
    if latest is None:
        return (package, None, None, f"could not determine latest version of {package}")

    local_version = _local_version(remote_interpreter, package)
    if isinstance(local_version, str):
        local_version = tuple(map(int, local_version.split(".")))
        local_version = (local_version + (0, 0))[:3]
    if not isinstance(local_version, tuple):
        return (package, latest, None, "could not determine local version")

    return package, latest, local_version, None


def _check_emzed_spyder_update():
    latest_version = _latest_version(sys.executable, "emzed_spyder")
    if latest_version is None:
        return None, None, "could not determine latest version of emzed_spyder"
    from . import __version__ as current_version_str

    current_version = tuple(map(int, current_version_str.split(".")))
    return latest_version, current_version, None


def _latest_version(remote_interpreter, package):

    output = ""
    try:
        # will fail as version 'x' is not available, will print available versions
        # to stderr then:
        binary_only = "--only-binary :all:" if sys.platform == "win32" else ""
        line = (
            f"{remote_interpreter} -m pip install -v {binary_only}"
            f" {package}==x"
        )
        subprocess.check_output(line.split(), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = str(e.output, "utf-8")

    versions = []
    for line in output.split("\n"):
        if "Found link" in line:
            match = re.search(rf"/{package}-(\d+\.\d+\.\d+)", line)
            if match is not None:
                versions.append(match.group(1))

    if versions:
        latest = max(tuple(map(int, version.split("."))) for version in versions)
        return latest
    return None


def _local_version(remote_interpreter, package_local):

    try:  # will fail as version is not specified, will print available versions
        # to stderr then:
        line = f"{remote_interpreter} -m pip show {package_local}"
        output = subprocess.check_output(line.split(), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return None

    for line in str(output, "utf-8").split("\n"):
        if line.startswith("Version:"):
            version = re.findall(r"\d+\.\d+\.\d+", line)[0]
            return version
