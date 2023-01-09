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
from flask import current_app
from flask_login import current_user

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.utils import flatten_list
from kadi.plugins.core import run_hook


def signal_resource_change(resource, user=None, created=False):
    """Convenience function to signal the creation or change of a resource.

    Runs the :func:`kadi.plugins.spec.kadi_post_resource_change` plugin hook. Generally,
    it is supposed to be run after a resource was created or changed and the change
    triggered the creation of a new revision.

    Note that this function may issue a database rollback.

    :param resource: The resource that was created or changed.
    :param user: (optional) The user who triggered the creation or change. Defaults to
        the current user.
    :param created: (optional) Flag indicating if the resource was newly created.
    """
    user = user if user is not None else current_user

    try:
        run_hook(
            "kadi_post_resource_change", resource=resource, user=user, created=created
        )
    except Exception as e:
        current_app.logger.exception(e)
        db.session.rollback()


def get_plugin_scripts():
    """Convenience function to retrieve all script URLs provided by plugins.

    Uses the :func:`kadi.plugins.spec.kadi_get_scripts` plugin hook to collect the
    script URLs.

    :return: A flattened list of all script URLs or an empty list if something went
        wrong while collecting the scripts.
    """
    try:
        urls = flatten_list(run_hook("kadi_get_scripts"))
    except Exception as e:
        current_app.logger.exception(e)
        return []

    return urls


def get_plugin_frontend_translations():
    """Convenience function to collect all frontend translations provided by plugins.

    Uses the :func:`kadi_get_translations_bundles` plugin hook to collect and merge the
    translation bundles.

    :return: A dictionary mapping each possible locale of the application to the merged
        translation bundles.
    """
    translations = {}

    for locale in const.LOCALES:
        translations[locale] = {}

        try:
            bundles = run_hook("kadi_get_translations_bundles", locale=locale)

            for bundle in bundles:
                if not isinstance(bundle, dict):
                    current_app.logger.error("Invalid translations bundle format.")
                    continue

                translations[locale].update(bundle)

        except Exception as e:
            current_app.logger.exception(e)

    return translations
