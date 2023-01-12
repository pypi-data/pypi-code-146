#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

import inspect
import os
import shutil
import sys

from .utils import document_folder, root_folder, spyder_folder

HERE = os.path.dirname(os.path.abspath(__file__))


def patch_config_folder():

    import spyder.config.base

    def get_conf_subfolder():
        return str(spyder_folder)

    def get_home_dir():
        return str(root_folder)

    def get_conf_path(filename=None):
        """Return absolute path to the config file with the specified filename."""
        conf_dir = os.path.join(get_home_dir(), get_conf_subfolder())

        if not os.path.isdir(conf_dir):
            os.makedirs(conf_dir)

        if filename is None:
            return conf_dir
        else:
            return os.path.join(conf_dir, filename)

    def get_module_path(name, _orig=spyder.config.base.get_module_path):
        # during restart spyder determines its own home folder and then calls
        # restart.py:main in its app sub folder.  we catch this case and inject our
        # current folder HERE such that spyder calls HERE/app/restart.py:main instead
        # we only patch this situation as get_module_path is called in different
        # settings.

        upper_frame = inspect.getouterframes(inspect.currentframe())[1]
        if upper_frame.function != "restart":
            return _orig(name)

        return HERE

    spyder.config.base.get_home_dir = get_home_dir
    spyder.config.base.get_conf_subfolder = get_conf_subfolder
    spyder.config.base.get_conf_path = get_conf_path
    spyder.config.base.get_module_path = get_module_path

    # this var was already set during import:
    spyder.config.base.LANG_FILE = get_conf_path("langconfig")


def patch_splash_screen():

    import spyder.config.base

    def get_image_path(
        name, default="not_found.png", _original=spyder.config.base.get_image_path
    ):
        if name == "splash.svg":
            return os.path.join(HERE, "assets", "splash.png")
        return _original(name, default=default)

    spyder.config.base.get_image_path = get_image_path


def set_spyder_theme():

    import spyder.config.appearance

    if sys.platform == "win32":
        return

    spyder.config.appearance.APPEARANCE["selected"] = "spyder"
    spyder.config.appearance.APPEARANCE["font/size"] = 14
    spyder.config.appearance.APPEARANCE["rich_font/size"] = 14


def disable_kite_startup_dialog():

    import spyder.config.main

    dd = dict(spyder.config.main.DEFAULTS)
    dd["kite"]["enable"] = False
    dd["kite"]["show_installation_dialog"] = False
    dd["kite"]["show_onboarding"] = False
    spyder.config.main.DEFAULTS = list(dd.items())


def disable_update_checks():
    import spyder.config.main

    dd = dict(spyder.config.main.DEFAULTS)
    dd["main"]["check_updates_on_startup"] = False


def silence_umr():
    import spyder.config.main

    dd = dict(spyder.config.main.DEFAULTS)
    dd["main_interpreter"]["umr/verbose"] = False
    spyder.config.main.DEFAULTS = list(dd.items())


def set_scripts_home_folder():
    import configparser

    from spyder.config.manager import CONF

    scripts_home_folder = document_folder / "emzed3_examples"

    if not scripts_home_folder.exists():
        shutil.copytree(os.path.join(HERE, "emzed3_examples"), scripts_home_folder)

    try:
        CONF._user_config.get("workingdir", "startup/fixed_directory")
    except configparser.NoSectionError:
        # first start
        CONF._user_config.set(
            "workingdir", "startup/fixed_directory", str(scripts_home_folder)
        )
        CONF._user_config.set("workingdir", "startup/use_fixed_directory", True)
        CONF._user_config.set(
            "workingdir", "startup/use_project_or_home_directory", False
        )
        CONF._user_config.set(
            "editor", "recent_files", [str(scripts_home_folder / "README.txt")]
        )
        CONF._user_config.set(
            "editor", "filenames", [str(scripts_home_folder / "README.txt")]
        )
    return


def set_remote_python_interpreter(path_executable):
    from spyder.config.manager import CONF

    executable = str(path_executable)

    CONF.set("main_interpreter", "custom", True)
    CONF.set("main_interpreter", "default", False)
    CONF.set("main_interpreter", "custom_interpreters_list", [executable])
    CONF.set("main_interpreter", "custom_interpreter", executable)
    CONF.set("main_interpreter", "executable", executable)


def set_remote_interpreter_startup_file():
    import spyder.config.main

    path = os.path.join(HERE, "remote_interpreter_startup.py")

    dd = dict(spyder.config.main.DEFAULTS)
    dd["ipython_console"]["startup/use_run_file"] = True
    dd["ipython_console"]["startup/run_file"] = path
    dd["ipython_console"]["startup/run_lines"] = f"__file__ = r'{path}'"

    # always override pylab backend to Qt, needed for non-modal inspect:
    from spyder.config.manager import CONF

    CONF.set("ipython_console", "pylab/backend", 2)

    spyder.config.main.DEFAULTS = list(dd.items())
