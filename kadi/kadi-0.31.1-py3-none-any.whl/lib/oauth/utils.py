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
import warnings

from flask import current_app
from flask_login import current_user
from markupsafe import Markup

from .core import update_oauth2_token
from .models import OAuth2Token
from kadi.ext.db import db
from kadi.ext.oauth import oauth
from kadi.lib.exceptions import KadiDecryptionKeyError
from kadi.lib.utils import find_dict_in_list
from kadi.plugins.core import run_hook


def get_oauth2_token(name, user=None, delete_on_error=False, auto_refresh=False):
    """Get an OAuth2 token of a user by its name.

    :param name: The name of the token.
    :param user: (optional) The user the token belongs to. Defaults to the current user.
    :param delete_on_error: (optional) Flag indicating whether the token should be
        deleted from the database if either the access token or refresh token cannot be
        decrypted due to an invalid decryption key or if the access token is expired and
        cannot be refreshed if ``auto_refresh`` is ``True``.
    :param auto_refresh: (optional) Flag indicating whether the underlying access token
        should be refreshed automatically if it is expired. This requires that the
        OAuth2 provider used to create the token is registered with the application and
        that a valid refresh token is stored as well.
    :return: The OAuth2 token or ``None`` if no token could be retrieved or refreshed.
    """
    user = user if user is not None else current_user
    oauth2_token_query = user.oauth2_tokens.filter(OAuth2Token.name == name)

    try:
        oauth2_token = oauth2_token_query.first()
    except KadiDecryptionKeyError:
        current_app.logger.error(
            f"Error decrypting OAuth2 token values for '{name}' of {user!r}."
        )

        if delete_on_error:
            oauth2_token_query.delete()

        return None

    if (
        auto_refresh
        and oauth2_token is not None
        and oauth2_token.is_expired
        and oauth2_token.refresh_token is not None
    ):
        client = oauth.create_client(name)

        if client is not None:
            try:
                # Since there is no documented way to manually update the access token
                # by using the Flask integration of Authlib, we use the underlying
                # OAuth2 session directly.
                token = client._get_oauth_client().refresh_token(
                    client.access_token_url, refresh_token=oauth2_token.refresh_token
                )
            except Exception as e:
                current_app.logger.exception(e)

                if delete_on_error:
                    oauth2_token_query.delete()

                return None

            update_oauth2_token(
                oauth2_token,
                access_token=token["access_token"],
                refresh_token=token.get("refresh_token"),
                expires_at=token.get("expires_at"),
                expires_in=token.get("expires_in"),
            )

    return oauth2_token


def has_oauth2_providers():
    """Check if at least one OAuth2 provider is registered.

    Uses the :func:`kadi.plugins.spec.kadi_get_oauth2_providers` plugin hook to check
    for potential OAuth2 providers.

    :return: ``True`` if at least one OAuth2 provider is registered, ``False``
        otherwise.
    """
    try:
        providers = run_hook("kadi_get_oauth2_providers")
    except Exception as e:
        current_app.logger.exception(e)
        return False

    return bool(providers)


def get_oauth2_providers(user=None):
    """Get a list of registered OAuth2 providers.

    Uses the :func:`kadi.plugins.spec.kadi_get_oauth2_providers` plugin hook to collect
    potential OAuth2 providers.

    Note that this function may issue one or more database commits.

    :param user: (optional) The user who should be checked for whether they are
        connected with an OAuth2 provider, in which case ``"is_connected"`` will be set
        to ``True`` for the respective provider. Defaults to the current user.
    :return: A list of provider dictionaries in the following form, sorted by whether
        the provider is connected first and the name of the provider second:

        .. code-block:: python3

            [
                {
                    "name": "example",
                    "title": "Example provider",
                    "website": "https://example.com",
                    "description": "An example OAuth2 provider.",
                    "is_connected": True,
                },
            ]
    """
    user = user if user is not None else current_user

    try:
        providers = run_hook("kadi_get_oauth2_providers")
    except Exception as e:
        current_app.logger.exception(e)
        return []

    oauth2_providers = []
    provider_names = set()

    for provider in providers:
        if not isinstance(provider, dict):
            current_app.logger.error("Invalid OAuth2 provider format.")
            continue

        provider_name = provider.get("name")

        if provider_name is None or provider_name not in oauth._clients:
            current_app.logger.error(f"Invalid OAuth2 provider '{provider_name}'.")
            continue

        if provider_name in provider_names:
            warnings.warn(f"Provider '{provider_name}' is already registered.")
            continue

        provider_names.add(provider_name)

        oauth2_token = get_oauth2_token(provider_name, user=user, delete_on_error=True)
        db.session.commit()

        oauth2_providers.append(
            {
                "name": provider_name,
                "title": provider.get("title", provider_name),
                "website": provider.get("website", ""),
                "description": Markup(provider.get("description", "")),
                "is_connected": oauth2_token is not None,
            }
        )

    return sorted(
        oauth2_providers,
        key=lambda provider: (not provider["is_connected"], provider["name"]),
    )


def get_oauth2_provider(provider, user=None):
    """Get a specific, registered OAuth2 provider.

    Note that this function may issue one or more database commits.

    :param provider: The unique name of the OAuth2 provider.
    :param user: (optional) See :func:`get_oauth2_providers`.
    :return: The publication provider in a format as described in
        :func:`get_oauth2_providers` or ``None`` if no provider with the given name
        could be found.
    """
    user = user if user is not None else current_user

    providers = get_oauth2_providers(user=user)
    return find_dict_in_list(providers, "name", provider)
