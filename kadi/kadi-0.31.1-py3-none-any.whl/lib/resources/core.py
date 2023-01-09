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
from sqlalchemy.exc import IntegrityError

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.db import update_object
from kadi.lib.permissions.core import add_role
from kadi.lib.permissions.core import delete_permissions
from kadi.lib.permissions.core import setup_permissions
from kadi.lib.revisions.core import create_revision
from kadi.lib.revisions.core import delete_revisions
from kadi.lib.tags.core import TaggingMixin
from kadi.plugins.utils import signal_resource_change


def create_resource(model, creator=None, **kwargs):
    r"""Convenience function to create a new resource.

    This will also create all default permissions of the resource.

    Note that this function issues a database commit or rollback.

    :param model: The model that represents the type of the new resource. One of
        :class:`.Record`, :class:`.Collection`, :class:`.Template` or :class:`.Group`.
    :param creator: (optional) The creator of the resource. Defaults to the current
        user.
    :param \**kwargs: Keyword arguments that will be used to intialize the data of the
        new resource. Note that if the given model inherits from :class:`.TaggingMixin`
        and a list of tags is given via ``tags``, these will be set accordingly.
    :return: The created resource or ``None`` if the resource could not be created.
    """
    creator = creator if creator is not None else current_user
    tags = kwargs.pop("tags", None)

    resource = model.create(creator=creator, **kwargs)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return None

    if (
        isinstance(resource, TaggingMixin)
        and tags is not None
        and not resource.set_tags(tags)
    ):
        db.session.rollback()
        return None

    setup_permissions(model.__tablename__, resource.id)
    add_role(creator, model.__tablename__, resource.id, "admin")

    create_revision(resource, user=creator)
    db.session.commit()

    signal_resource_change(resource, user=creator, created=True)

    return resource


def update_resource(resource, user=None, **kwargs):
    r"""Convenience function to update an existing resource.

    Note that this function may issue a database commit or rollback.

    :param resource: The resource to update. An instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Template` or :class:`.Group`.
    :param user: (optional) The user who triggered the update. Defaults to the current
        user.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`. Note that if the type of the given resource
        inherits from :class:`.TaggingMixin` and a list of tags is given via ``tags``,
        these will be set accordingly.
    :return: ``True`` if the resource was updated successfully, ``False`` otherwise.
    """
    user = user if user is not None else current_user
    tags = kwargs.pop("tags", None)

    if resource.state != const.MODEL_STATE_ACTIVE:
        return False

    update_object(resource, **kwargs)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    if (
        isinstance(resource, TaggingMixin)
        and tags is not None
        and not resource.set_tags(tags)
    ):
        db.session.rollback()
        return False

    revision_created = create_revision(resource, user=user)
    db.session.commit()

    if revision_created:
        signal_resource_change(resource, user=user)

    return True


def delete_resource(resource, user=None):
    """Convenience function to delete an existing resource.

    This will perform a soft deletion, i.e. only the resource's state will be changed.

    Note that this function issues a database commit.

    :param resource: The resource to delete. An instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Template` or :class:`.Group`.
    :param user: (optional) The user who triggered the deletion. Defaults to the current
        user.
    """
    user = user if user is not None else current_user

    revision_created = False

    if resource.state == const.MODEL_STATE_ACTIVE:
        resource.state = const.MODEL_STATE_DELETED
        revision_created = create_revision(resource, user=user)

    db.session.commit()

    if revision_created:
        signal_resource_change(resource, user=user)


def restore_resource(resource, user=None):
    """Convenience function to restore a deleted resource.

    Note that this function issues a database commit.

    :param resource: The resource to restore. An instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Template` or :class:`.Group`.
    :param user: (optional) The user who triggered the restoration. Defaults to the
        current user.
    """
    user = user if user is not None else current_user

    revision_created = False

    if resource.state == const.MODEL_STATE_DELETED:
        resource.state = const.MODEL_STATE_ACTIVE
        revision_created = create_revision(resource, user=user)

    db.session.commit()

    if revision_created:
        signal_resource_change(resource, user=user)


def purge_resource(resource):
    """Convenience function to purge an existing resource.

    This will completely delete the resource from the database.

    Note that this function issues a database commit.

    :param resource: The resource to purge. An instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Template` or :class:`.Group`.
    """
    delete_revisions(resource)
    delete_permissions(resource.__class__.__tablename__, resource.id)

    db.session.delete(resource)
    db.session.commit()
