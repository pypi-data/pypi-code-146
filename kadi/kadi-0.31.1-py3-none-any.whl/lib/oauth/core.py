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
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask_login import current_user

from .models import OAuth2Token
from kadi.lib.db import update_object
from kadi.lib.utils import utcnow


def _expiration_to_datetime(expires_at=None, expires_in=None):
    expires_at_datetime = None

    if expires_at is not None:
        expires_at_datetime = datetime.utcfromtimestamp(expires_at).replace(
            tzinfo=timezone.utc
        )
    elif expires_in is not None:
        expires_at_datetime = utcnow() + timedelta(seconds=expires_in)

    return expires_at_datetime


def create_oauth2_token(
    *,
    name,
    access_token,
    refresh_token=None,
    user=None,
    expires_at=None,
    expires_in=None,
):
    """Create a new OAuth2 token.

    :param name: See :attr:`.OAuth2Token.name`.
    :param access_token: See :attr:`.OAuth2Token.access_token`.
    :param refresh_token: (optional) See :attr:`.OAuth2Token.refresh_token`.
    :param user: (optional) The user the token should belong to. Defaults to the current
        user.
    :param expires_at: (optional) The expiration date and time of the access token as
        Unix timestamp. Will be preferred if ``expires_in`` is also given.
    :param expires_in: (optional) The lifetime of the access token in seconds.
    :return: The created OAuth2 token.
    """
    user = user if user is not None else current_user

    expires_at_datetime = _expiration_to_datetime(
        expires_at=expires_at, expires_in=expires_in
    )

    return OAuth2Token.create(
        user=user,
        name=name,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at_datetime,
    )


def update_oauth2_token(oauth2_token, expires_at=None, expires_in=None, **kwargs):
    r"""Update an existing OAuth2 token.

    :param oauth2_token: The OAuth2 token to update.
    :param expires_at: (optional) The expiration date and time of the access token as
        Unix timestamp. Will be preferred if ``expires_in`` is also given.
    :param expires_in: (optional) The lifetime of the access token in seconds.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    """
    if expires_at is not None or expires_in is not None:
        kwargs["expires_at"] = _expiration_to_datetime(
            expires_at=expires_at, expires_in=expires_in
        )

    update_object(oauth2_token, **kwargs)
