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
from flask_login import current_user

from .models import Favorite
from kadi.ext.db import db


class FavoriteMixin:
    """Mixin for SQLALchemy models to check whether an object is favorited."""

    def is_favorite(self, user=None):
        """Check if the current object is favorited by the given user.

        Wraps :func:`is_favorite` with the type and ID of the current object.

        :param user: (optional) The user whose favorites should be checked. Defaults to
            the current user.
        :return: See :func:`is_favorite`.
        """
        user = user if user is not None else current_user

        return is_favorite(self.__tablename__, self.id, user=user)


def is_favorite(object_name, object_id, user=None):
    """Check if the given object is favorited by the given user.

    :param object_name: The type of object.
    :param object_id: The ID of a specific object.
    :param user: (optional) The user whose favorites should be checked. Defaults to the
        current user.
    :return: ``True`` if the object is favorited, ``False`` otherwise.
    """
    user = user if user is not None else current_user

    favorite = (
        user.favorites.filter(
            Favorite.object == object_name, Favorite.object_id == object_id
        )
        .with_entities(Favorite.id)
        .first()
    )
    return favorite is not None


def toggle_favorite(object_name, object_id, user=None):
    """Toggle the favorite state of the given object.

    If a favorite already exists for the given object and user, it will be deleted from
    the database, otherwise it will be created.

    :param object_name: The type of object.
    :param object_id: The ID of a specific object.
    :param user: (optional) The user the favorite object belongs to. Defaults to the
        current user.
    """
    user = user if user is not None else current_user

    favorite = user.favorites.filter(
        Favorite.object == object_name, Favorite.object_id == object_id
    ).first()

    if favorite is not None:
        db.session.delete(favorite)
    else:
        Favorite.create(user=user, object=object_name, object_id=object_id)
