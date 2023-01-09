# Copyright 2021 Karlsruhe Institute of Technology
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
from functools import wraps
from uuid import uuid4

from flask import abort
from flask_login import current_user
from flask_login import login_required

import kadi.lib.constants as const
from kadi.lib.config.core import get_sys_config
from kadi.lib.config.core import remove_sys_config
from kadi.lib.config.core import set_sys_config
from kadi.lib.config.models import ConfigItem
from kadi.lib.storage.misc import delete_thumbnail
from kadi.lib.storage.misc import save_as_thumbnail


def sysadmin_required(func):
    """Decorator to add access restrictions based on sysadmin status to an endpoint.

    If the current user is not authenticated, the decorator will behave the same as
    Flask-Login's ``login_required`` decorator.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_sysadmin:
            abort(404)

        return func(*args, **kwargs)

    return login_required(wrapper)


def save_index_image(file_object):
    """Set an image file used on the index page as a global config item.

    Uses ``"INDEX_IMAGE"`` as the key for the config item and
    :func:`kadi.lib.storage.local.save_as_thumbnail` to create and save a thumbnail of
    the given image. Any previous image will be deleted beforehand using
    :func:`delete_index_image`, which will also be called if the image cannot be saved.

    :param file_object: The image file object.
    """
    delete_index_image()

    config_item = set_sys_config(const.SYS_CONFIG_INDEX_IMAGE, str(uuid4()))

    if not save_as_thumbnail(
        config_item.value, file_object, max_resolution=(1_024, 1_024)
    ):
        delete_index_image()


def delete_index_image():
    """Delete the image file used on the index page, including the global config item.

    Uses ``"INDEX_IMAGE"`` as the key for the config item and
    :func:`kadi.lib.storage.local.delete_thumbnail` to delete the actual thumbnail file.
    """
    image_identifier = get_sys_config(const.SYS_CONFIG_INDEX_IMAGE, use_fallback=False)

    if image_identifier:
        delete_thumbnail(image_identifier)

    remove_sys_config(const.SYS_CONFIG_INDEX_IMAGE)


def legals_acceptance_required():
    """Check whether users need to accept the configured legal notices.

    :return: ``True`` if any of the relevant legal notices are configured and accepting
        them is enforced, ``False`` otherwise.
    """
    if not get_sys_config(const.SYS_CONFIG_ENFORCE_LEGALS):
        return False

    for key in [const.SYS_CONFIG_TERMS_OF_USE, const.SYS_CONFIG_PRIVACY_POLICY]:
        if get_sys_config(key):
            return True

    return False


def get_legals_modification_date():
    """Get the latest modification date of the configured legal notices.

    Note that only config items in the database are considered, as only these track
    their modification date.

    :return: The latest modification date as a datetime object as specified in Python's
        ``datetime`` module or ``None`` if none of the relevant legal notices is
        configured in the database.
    """
    modification_dates = []

    for key in [const.SYS_CONFIG_TERMS_OF_USE, const.SYS_CONFIG_PRIVACY_POLICY]:
        config_item = ConfigItem.query.filter(
            ConfigItem.key == key, ConfigItem.user_id.is_(None)
        ).first()

        if config_item is not None:
            modification_dates.append(config_item.last_modified)

    if modification_dates:
        return max(modification_dates)

    return None
