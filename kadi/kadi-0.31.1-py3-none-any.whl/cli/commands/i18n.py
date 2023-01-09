# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys

import click
from flask import current_app

import kadi.lib.constants as const
from kadi.cli.main import kadi
from kadi.cli.utils import echo_danger
from kadi.cli.utils import echo_success
from kadi.cli.utils import echo_warning
from kadi.cli.utils import run_command
from kadi.plugins.core import run_hook


@kadi.group()
def i18n():
    """Utility commands for managing translations."""


def _pybabel_extract(translations_path):
    cwd = os.getcwd()
    # Change the current working directory to the application root path for the
    # extraction process. All configured paths in "babel.cfg" need to be relative to
    # this path.
    os.chdir(current_app.root_path)

    babel_cfg = os.path.join(translations_path, "babel.cfg")
    pot_path = os.path.join(translations_path, "messages.pot")

    cmd = [
        "pybabel",
        "extract",
        "-F",
        babel_cfg,
        "-k",
        "lazy_gettext",
        "-k",
        "_l",
        "-o",
        pot_path,
        "--copyright-holder",
        "Karlsruhe Institute of Technology",
        "--project",
        "Kadi4Mat",
        "--no-location",
        "--sort-output",
        ".",
    ]
    run_command(cmd)

    os.chdir(cwd)


def _load_plugins():
    os.environ[const.VAR_API_BP] = "1"

    # Always load all plugins, even if not configured, since they might specify a custom
    # translations path.
    current_app.plugin_manager.load_setuptools_entrypoints(
        current_app.config["PLUGIN_ENTRYPOINT"]
    )


def _get_translations_path(plugin_name):
    if plugin_name is not None:
        plugin = current_app.plugin_manager.get_plugin(plugin_name)

        if plugin is not None:
            if hasattr(plugin, "kadi_get_translations_paths"):
                return plugin.kadi_get_translations_paths()

            echo_danger("The given plugin does not specify a translations path.")
        else:
            echo_danger("No plugin with that name could be found.")

        sys.exit(1)

    return current_app.config["BACKEND_TRANSLATIONS_PATH"]


@i18n.command()
@click.argument("lang")
@click.option("-p", "--plugin", help="The name of a plugin to use instead.")
@click.option("--i-am-sure", is_flag=True)
def init(lang, plugin, i_am_sure):
    """Add a new language to the backend translations."""
    if not i_am_sure:
        echo_warning(
            f"This might replace existing translations for language '{lang}'. If you"
            " are sure you want to do this, use the flag --i-am-sure."
        )
        sys.exit(1)

    _load_plugins()

    translations_path = _get_translations_path(plugin)
    pot_path = os.path.join(translations_path, "messages.pot")
    cmd = ["pybabel", "init", "-i", pot_path, "-d", translations_path, "-l", lang]

    _pybabel_extract(translations_path)
    run_command(cmd)

    echo_success("Initialization completed successfully.")


@i18n.command()
@click.option("-p", "--plugin", help="The name of a plugin to use instead.")
def update(plugin):
    """Update the existing backend translations."""
    _load_plugins()

    translations_path = _get_translations_path(plugin)
    pot_path = os.path.join(translations_path, "messages.pot")
    cmd = ["pybabel", "update", "-N", "-i", pot_path, "-d", translations_path]

    _pybabel_extract(translations_path)
    run_command(cmd)

    echo_success("Update completed successfully.")


@i18n.command()
def compile():
    """Compile the existing backend translations, including plugins."""
    _load_plugins()

    translations_paths = [current_app.config["BACKEND_TRANSLATIONS_PATH"]] + run_hook(
        "kadi_get_translations_paths"
    )

    for path in translations_paths:
        cmd = ["pybabel", "compile", "-d", path]
        run_command(cmd)

    echo_success("Compilation completed successfully.")
