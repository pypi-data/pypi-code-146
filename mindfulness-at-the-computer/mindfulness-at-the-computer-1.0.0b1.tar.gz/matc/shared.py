import enum
import logging
import os
import shutil
import sys
import tempfile
import urllib.request
from string import Template

from PySide6 import QtCore

import matc.constants

"""
This file contains
* enums
* global functions, for example:
  * relating to file names/paths (some using QtCore)
  * relating to font (some using QtGui)
"""

APPLICATION_ICON_FILE_NAME = "icon.png"
APPLICATION_ICON_WITH_DOT_FILE_NAME = "icon-b.png"

USER_FILES_DIR = "user_files"
IMAGES_DIR = "images"
ICONS_DIR = "icons"
AUDIO_DIR = "audio"
RES_DIR = "res"

LIGHT_GREEN_COLOR = "#bfef7f"
DARK_GREEN_COLOR = "#7fcc19"
DARKER_GREEN_COLOR = "#548811"
WHITE_COLOR = "#ffffff"
BLACK_COLOR = "#1C1C1C"


class BrVis(enum.Enum):
    bar = 0
    circle = 1
    line = 2
    columns = 3


class Platform(enum.Enum):
    gnu_linux = enum.auto()
    windows = enum.auto()
    macos = enum.auto()
    other = enum.auto()


def get_platform() -> Platform:
    kernel_type: str = QtCore.QSysInfo.kernelType()
    if kernel_type == "linux":
        return Platform.gnu_linux
    if kernel_type == "darwin":
        return Platform.macos
    if kernel_type == "windows":
        return Platform.windows
    return Platform.other


def do_extra_setup():
    """
    Called from two different places: 1. setup.py 2. When first starting the application
    :return:
    """
    platform = get_platform()
    if platform == Platform.gnu_linux:
        do_extra_setup_gnu_linux()
    elif platform == Platform.windows:
        do_extra_setup_windows()
    elif platform == Platform.macos:
        do_extra_setup_macos()
    else:
        pass


def do_extra_setup_windows():
    """
    Two approaches:
    * Option A: Creating a windows shortcut file (.lnk file) and adding it to the startup dir and
    start menu.
      This is complicated to do since .lnk files are designed to be difficult to create. They are
      (at least look like)
      binary files. It is possible though if we install (using pip) pywin32 and winshell. But at
      the time of writing i don't think it's worth it since it would add two new depenedencies
      and increase the size of the pyinstaller package
    * Option B: Adding a registry entry for the application
      This requires admin priveliges

    Workaround: During the first startup of the application, we can ask the user to add the
    application to autostart
    and add a shortcut
    """
    logging.debug("Extra setup is not supported on Windows")


def do_extra_setup_macos():
    # TODO: Looking into this (need to talk to someone with a Mac computer)
    logging.debug("Extra setup is not supported on MacOS")


def do_extra_setup_gnu_linux():
    """
    This function is called automatically during pip install. It creates a .desktop file and
    copies it to these dirs:
    * The user applications dir - so that the user can see the application shortcut in the menu
    system used by the
    desktop environment she is using
    * The autostart dir - so that the application is automatically launched on startup

    ### Menu .desktop files
    On Linux-based systems menu .desktop files are locally stored in
    ~/.local/share/applications (globally in /usr/share/applications)

    ### Autostart dir
    > $XDG_CONFIG_HOME defines the base directory relative to which user-specific configuration
    files should be stored.
    > If $XDG_CONFIG_HOME is either not set or empty, a default equal to $HOME/.config should be
    used.

    Based on the info above this is the default location: .desktop file in ~/.config/autostart

    Please note:
    * Only gnu/linux systems can run this extra setup file at the moment
    * Printouts are not written to the terminal unless the user has added the verbose flag at the
    end:
      `pip3 install -e . -v`

    There is no way to call a file at uninstall, but we could - in this script - create a text
    file with a list of the
    files that we have installed and therefore want to remove. And then have a simple script file
    which removes these
    files. One way to do this is described here: https://gist.github.com/myusuf3/933625 (I don't
    think we need to use
    sudo though)

    References:
    * Freedesktop spec:
      * https://www.freedesktop.org/wiki/Specifications/autostart-spec/
      * https://specifications.freedesktop.org/autostart-spec/autostart-spec-latest.html
    * https://doc.qt.io/qt-5/qstandardpaths.html#StandardLocation-enum
    """

    if matc.shared.get_platform() != matc.shared.Platform.gnu_linux:
        logging.debug("Only gnu/linux systems can run this extra setup at the moment")
        return

    # from PySide6 import QtCore

    print("====Running extra setup python script extra_setup.py====")
    user_home_dir = QtCore.QStandardPaths.standardLocations(
        QtCore.QStandardPaths.HomeLocation)[0]
    user_config_dir = QtCore.QStandardPaths.standardLocations(
        QtCore.QStandardPaths.ConfigLocation)[0]
    user_applications_dir = QtCore.QStandardPaths.standardLocations(
        QtCore.QStandardPaths.ApplicationsLocation)[0]
    os.makedirs(user_applications_dir, exist_ok=True)
    user_desktop_dir = QtCore.QStandardPaths.standardLocations(
        QtCore.QStandardPaths.DesktopLocation)[0]
    os.makedirs(user_desktop_dir, exist_ok=True)
    user_autostart_dir = os.path.join(user_config_dir, "autostart")
    os.makedirs(user_autostart_dir, exist_ok=True)

    read_icon_path = get_app_icon_path()
    write_icon_path = matc.shared.get_config_path(APPLICATION_ICON_FILE_NAME)
    print(f"Copying {read_icon_path} to {write_icon_path}")
    shutil.copy(read_icon_path, write_icon_path)

    template_desktop_file_path: str = get_res_path("mindfulness-at-the-computer[template].desktop")
    with open(template_desktop_file_path, "r") as f:
        template_content_str = f.read()
    template = Template(template_content_str)
    exec_path = os.path.join(user_home_dir, ".local", "bin", matc.constants.APPLICATION_NAME)
    output_desktop_file_contents: str = template.substitute(exec=exec_path, icon=write_icon_path)
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        print(f"{tmp_dir_path=}")
        output_desktop_file_name: str = "mindfulness-at-the-computer.desktop"
        output_desktop_file_path = os.path.join(tmp_dir_path, output_desktop_file_name)

        with open(output_desktop_file_path, "w+") as output_file:
            output_file.write(output_desktop_file_contents)

        os.chmod(output_desktop_file_path, 0o744)
        print(f"Copying {output_desktop_file_path} to {user_applications_dir}")
        shutil.copy2(output_desktop_file_path, user_applications_dir)
        print(f"Copying {output_desktop_file_path} to {user_autostart_dir}")
        shutil.copy2(output_desktop_file_path, user_autostart_dir)
        print(f"Copying {output_desktop_file_path} to {user_desktop_dir}")
        shutil.copy2(output_desktop_file_path, user_desktop_dir)


def get_system_info() -> dict:
    sys_info_telist = {}
    sys_info_telist["Application name"] = matc.constants.APPLICATION_NAME
    sys_info_telist["Application version"] = get_version()
    sys_info_telist["Config path"] = get_config_path()
    sys_info_telist["Module path"] = get_module_path()
    sys_info_telist["Python version"] = sys.version
    sys_info_telist["Qt version"] = QtCore.qVersion()
    plugins_path: str = QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.PluginsPath)
    sys_info_telist["Plugins path"] = plugins_path
    qt_sys_info = QtCore.QSysInfo()
    sys_info_telist["OS name and version"] = qt_sys_info.prettyProductName()
    kernel_type_and_version = qt_sys_info.kernelType() + " " + qt_sys_info.kernelVersion()
    sys_info_telist["Kernel type and version"] = kernel_type_and_version
    sys_info_telist["buildCpuArchitecture"] = qt_sys_info.buildCpuArchitecture()
    sys_info_telist["currentCpuArchitecture"] = qt_sys_info.currentCpuArchitecture()
    system_locale = QtCore.QLocale.system().name()
    """
    Other things we may want to add:
    self.tray_icon.isSystemTrayAvailable():
    self.tray_icon.supportsMessages():
    desktop_widget = matc_qapplication.desktop()
    desktop_widget.isVirtualDesktop()
    desktop_widget.screenCount()
    desktop_widget.primaryScreen()
    sys_info_telist.append(("Pyside version"))
    """
    sys_info_telist["System Localization"] = system_locale

    return sys_info_telist


def get_config_path(*args) -> str:
    # application_dir_str = os.path.dirname(os.path.dirname(__file__))
    config_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    # logging.debug("QStandardPaths.ConfigLocation = " + config_dir)

    # There is a bug in Qt: For Windows, the application name is included in
    # QStandardPaths.ConfigLocation (for Linux, it's not included)
    if matc.constants.APPLICATION_NAME not in config_dir:
        config_dir = os.path.join(config_dir, matc.constants.APPLICATION_NAME)
    full_path_str = config_dir
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    os.makedirs(os.path.dirname(full_path_str), exist_ok=True)
    return full_path_str


def get_module_path(i_file_name: str = "") -> str:
    ret_module_dir_str: str = os.path.dirname(os.path.abspath(__file__))
    # -__file__ is the file that was started
    # base_dir_str: str = os.path.dirname(ret_module_dir_str)
    # base_dir_str = os.getcwd()
    if i_file_name:
        ret_module_dir_str = os.path.join(ret_module_dir_str, i_file_name)

    return ret_module_dir_str


def get_res_path(i_file_name: str = "") -> str:
    ret_res_path_str = os.path.join(get_module_path(), RES_DIR)
    if i_file_name:
        ret_res_path_str = os.path.join(ret_res_path_str, i_file_name)
    return ret_res_path_str


def get_audio_path(i_file_name: str = "") -> str:
    ret_audio_path_str = os.path.join(get_res_path(), AUDIO_DIR)
    if i_file_name:
        ret_audio_path_str = os.path.join(ret_audio_path_str, i_file_name)
    return ret_audio_path_str


def get_icon_path(i_file_name: str) -> str:
    ret_icon_path_str = os.path.join(get_res_path(), ICONS_DIR, i_file_name)
    return ret_icon_path_str


def get_app_icon_path(i_notification_dot: bool = False) -> str:
    if i_notification_dot:
        file_name = APPLICATION_ICON_WITH_DOT_FILE_NAME
    else:
        file_name = APPLICATION_ICON_FILE_NAME
    ret_icon_path_str = get_icon_path(file_name)
    return ret_icon_path_str


def get_html(i_text: str, i_focus: bool = False, i_margin: int = 0) -> str:
    html_template_base = (
        '<p style="text-align:center;padding:0px;margin:${margin}px;font-size:18px;${bold};'
        'color:${color_hex};">${text}</p>')
    html_template = Template(html_template_base)
    bold_html = ""
    color_hex: str = DARKER_GREEN_COLOR
    if i_focus:
        bold_html = "font-weight:bold;"
        color_hex: str = LIGHT_GREEN_COLOR
    ret_html = html_template.substitute(margin=i_margin, bold=bold_html, text=i_text,
        color_hex=color_hex)
    return ret_html


def get_version() -> str:
    version_file_path = get_module_path("version.txt")
    with open(version_file_path) as file:
        contents = file.read()
    ret_version = contents.strip()
    return ret_version


FAILED_TO_READ_REMOTE_VERSION = "failed"


def get_remote_version() -> str:
    url = ("https://gitlab.com/mindfulness-at-the-computer/mindfulness-at-the-computer.gitlab.io"
           "/-/raw/master/application-version.txt")
    try:
        with urllib.request.urlopen(url) as latest_version_source:
            remote_version_contents = latest_version_source.read()
    except urllib.error.URLError:
        logging.warning(
            "Could not download remote version file. This may simply be because you are "
            "temporarily disconnected from the internet."
        )
        return FAILED_TO_READ_REMOTE_VERSION
    remote_version_contents = remote_version_contents.decode('utf-8')
    ret_remote_version = remote_version_contents.strip()
    return ret_remote_version


def is_update_available() -> bool:
    local_version = get_version()
    latest_version = get_remote_version()
    if latest_version == FAILED_TO_READ_REMOTE_VERSION:
        return False
    if local_version == latest_version:
        return False
    return True
