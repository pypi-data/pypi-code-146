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
from flask_login import current_user

from .models import Collection
from .models import CollectionState
from .models import CollectionVisibility
from kadi.lib.conversion import strip_markdown
from kadi.lib.db import acquire_lock
from kadi.lib.exceptions import KadiPermissionError
from kadi.lib.permissions.core import has_permission
from kadi.lib.resources.core import create_resource
from kadi.lib.resources.core import delete_resource
from kadi.lib.resources.core import purge_resource
from kadi.lib.resources.core import restore_resource
from kadi.lib.resources.core import update_resource


def create_collection(
    *,
    identifier,
    title,
    creator=None,
    description="",
    visibility=CollectionVisibility.PRIVATE,
    state=CollectionState.ACTIVE,
    tags=None,
):
    """Create a new collection.

    Uses :func:`kadi.lib.resources.core.create_resource`.

    :param identifier: See :attr:`.Collection.identifier`.
    :param title: See :attr:`.Collection.title`.
    :param creator: (optional) The creator of the collection. Defaults to the current
        user.
    :param description: (optional) See :attr:`.Collection.description`.
    :param visibility: (optional) See :attr:`.Collection.visibility`.
    :param state: (optional) See :attr:`.Collection.state`.
    :param tags: (optional) A list of tag names to tag the collection with. See also
        :class:`.Tag`.
    :return: See :func:`kadi.lib.resources.core.create_resource`.
    """
    creator = creator if creator is not None else current_user

    return create_resource(
        Collection,
        creator=creator,
        identifier=identifier,
        title=title,
        description=description,
        plain_description=strip_markdown(description),
        visibility=visibility,
        state=state,
        tags=tags,
    )


def update_collection(collection, tags=None, user=None, **kwargs):
    r"""Update an existing collection.

    Uses :func:`kadi.lib.resources.core.update_resource`.

    :param collection: The collection to update.
    :param tags: (optional) A list of tag names to tag the collection with. See also
        :class:`.Tag`.
    :param user: (optional) The user who triggered the update. Defaults to the current
        user.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.resources.core.update_resource`.
    :return: See :func:`kadi.lib.resources.core.update_resource`.
    """
    user = user if user is not None else current_user

    if "description" in kwargs:
        kwargs["plain_description"] = strip_markdown(kwargs["description"])

    return update_resource(collection, user=user, tags=tags, **kwargs)


def delete_collection(collection, user=None):
    """Delete an existing collection.

    Uses :func:`kadi.lib.resources.core.delete_resource`.

    :param collection: The collection to delete.
    :param user: (optional) The user who triggered the deletion. Defaults to the current
        user.
    """
    user = user if user is not None else current_user
    delete_resource(collection, user=user)


def restore_collection(collection, user=None):
    """Restore a deleted collection.

    Uses :func:`kadi.lib.resources.core.restore_resource`.

    :param collection: The collection to restore.
    :param user: (optional) The user who triggered the restoration. Defaults to the
        current user.
    """
    user = user if user is not None else current_user
    restore_resource(collection, user=user)


def purge_collection(collection):
    """Purge an existing collection.

    Uses :func:`kadi.lib.resources.core.purge_resource`.

    :param collection: The collection to purge.
    """
    purge_resource(collection)


def link_collections(parent_collection, child_collection, user=None):
    """Link two collections together.

    Note that this function acquires a lock on the given collections.

    :param parent_collection: The parent collection.
    :param child_collection: The child collection.
    :param user: (optional) The user performing the link operation. Defaults to the
        current user.
    :return: ``True`` if the collections were linked successfully, ``False`` if both
        given collections refer to the same object, if the given child collection
        already has a parent or if the given child collection is already a parent of the
        parent collection.
    :raises KadiPermissionError: If the user performing the operation does not have the
        necessary permissions.
    """
    user = user if user is not None else current_user

    if not has_permission(
        user, "link", "collection", parent_collection.id
    ) or not has_permission(user, "link", "collection", child_collection.id):
        raise KadiPermissionError("No permission to link collections.")

    # Acquire a lock on the given collections to ensure that all cycle checks use up to
    # date values.
    parent_collection = acquire_lock(parent_collection)
    child_collection = acquire_lock(child_collection)

    if child_collection == parent_collection:
        return False

    if child_collection.parent_id:
        return False

    # Check that the child collection is not already a parent of the parent collection
    # to prevent cycles.
    current_parent = parent_collection.parent

    while current_parent is not None:
        if current_parent == child_collection:
            return False

        current_parent = current_parent.parent

    # No need for further checks, since we already know the collection does not have any
    # parent.
    parent_collection.children.append(child_collection)
    return True
