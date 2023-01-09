# Copyright 2022 Karlsruhe Institute of Technology
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
import warnings
from collections import OrderedDict

from flask import current_app

from kadi.plugins.core import run_hook


def get_plugin_preferences_configs():
    """Get all plugin preferences configurations.

    Uses the :func:`kadi.plugins.spec.kadi_get_preferences_config` plugin hook to
    collect all potential configurations.

    :return: An ordered (by title) dictionary of plugin preferences configurations,
        mapping the name of each plugin (as specificed in the plugin forms) to a
        dictionary in the form as expected by
        :func:`kadi.plugins.spec.kadi_get_preferences_config`.
    """
    preferences_configs = run_hook("kadi_get_preferences_config")
    preferences_configs.sort(key=lambda config: config["title"])

    results = OrderedDict()

    for config in preferences_configs:
        if not isinstance(config, dict) or "form" not in config:
            current_app.logger.error("Invalid preferences configuration format.")
            continue

        form = config["form"]
        plugin_name = form.plugin_name

        if plugin_name in results:
            warnings.warn(f"Duplicate preferences configuration for '{plugin_name}'.")
            continue

        results[plugin_name] = {
            "form": form,
            "title": config.get("title", plugin_name),
            "get_template": config.get("get_template", lambda: ""),
        }

    return results
