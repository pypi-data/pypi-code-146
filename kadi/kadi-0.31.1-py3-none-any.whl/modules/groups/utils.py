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
from uuid import uuid4

from flask_login import current_user

from .models import Group
from .models import GroupState
from kadi.lib.permissions.models import Role
from kadi.lib.resources.utils import get_filtered_resources
from kadi.lib.resources.utils import search_resources
from kadi.lib.storage.misc import delete_thumbnail
from kadi.lib.storage.misc import save_as_thumbnail


def search_groups(
    search_query=None,
    page=1,
    per_page=10,
    sort="_score",
    visibility=None,
    user_ids=None,
    member_only=False,
    user=None,
):
    """Search and filter for groups.

    Uses :func:`kadi.lib.resources.utils.get_filtered_resources` and
    :func:`kadi.lib.resources.utils.search_resources`.

    :param search_query: (optional) See
        :func:`kadi.lib.resources.utils.search_resources`.
    :param page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param per_page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param sort: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param visibility: (optional) See
        :func:`kadi.lib.resources.utils.get_filtered_resources`.
    :param user_ids: (optional) See
        :func:`kadi.lib.resources.utils.get_filtered_resources`.
    :param member_only: (optional) Flag indicating whether to exclude groups without
        membership.
    :param user: (optional) The user to check for any permissions regarding the searched
        groups. Defaults to the current user.
    :return: The search results as returned by
        :func:`kadi.lib.resources.utils.search_resources`.
    """
    user = user if user is not None else current_user

    groups_query = get_filtered_resources(
        Group, visibility=visibility, user_ids=user_ids, user=user
    )

    if member_only:
        groups_query = groups_query.intersect(get_user_groups(user))

    group_ids = [g.id for g in groups_query.with_entities(Group.id)]

    return search_resources(
        Group,
        search_query=search_query,
        page=page,
        per_page=per_page,
        sort=sort,
        filter_ids=group_ids,
    )


def get_user_groups(user=None):
    """Get all groups a user is a member of.

    Group membership currently works through roles. As long as a user has any role
    inside a group, they are a member of it. Therefore, it is currently safe to assume
    that the given user has at least read permission for such groups. Note that inactive
    groups will be filtered out.

    :param user: (optional) The user to get the groups for. Defaults to the current
        user.
    :return: The groups of the given user as query.
    """
    user = user if user is not None else current_user

    group_ids_query = user.roles.filter(Role.object == "group").with_entities(
        Role.object_id
    )
    return Group.query.filter(
        Group.id.in_(group_ids_query), Group.state == GroupState.ACTIVE
    )


def save_group_image(group, file_object):
    """Set an image file as a group's profile image.

    Uses :func:`kadi.lib.storage.local.save_as_thumbnail` to create and save a thumbnail
    of the given image. Any previous image will be deleted beforehand using
    :func:`delete_group_image`, which will also be called if the image cannot be saved.

    :param group: The group to set the new profile image for.
    :param file_object: The image file object.
    """
    delete_group_image(group)

    group.image_name = uuid4()

    if not save_as_thumbnail(str(group.image_name), file_object):
        delete_group_image(group)


def delete_group_image(group):
    """Delete a group's profile image if one exists.

    Uses :func:`kadi.lib.storage.local.delete_thumbnail` to delete the actual thumbnail
    file.

    :param group: The group of which the profile image should be deleted.
    """
    if group.image_name:
        delete_thumbnail(str(group.image_name))
        group.image_name = None
