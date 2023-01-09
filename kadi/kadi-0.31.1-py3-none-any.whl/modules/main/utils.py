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
from flask_login import current_user

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.db import escape_like
from kadi.lib.favorites.models import Favorite
from kadi.lib.licenses.models import License
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.resources import RESOURCE_TYPES
from kadi.lib.tags.models import Tag
from kadi.lib.web import url_for
from kadi.modules.collections.models import Collection
from kadi.modules.groups.utils import get_user_groups
from kadi.modules.records.models import Record


def get_tags(filter_term="", resource_type=None, user=None):
    """Get all distinct tags of resources a user can access.

    :param filter_term: (optional) A (case insensitive) term to filter the tags by their
        name.
    :param resource_type: (optional) A resource type to limit the tags to. One of
        ``"record"`` or ``"collection"``.
    :param user: (optional) The user who will be checked for access permissions.
        Defaults to the current user.
    :return: The tags as query, ordered by their name in ascending order.
    """
    user = user if user is not None else current_user

    tag_queries = []

    if resource_type == "record":
        models = [Record]
    elif resource_type == "collection":
        models = [Collection]
    else:
        models = [Record, Collection]

    for model in models:
        tags_query = Tag.query.join(model.tags).filter(
            model.state == const.MODEL_STATE_ACTIVE,
            model.id.in_(
                get_permitted_objects(user, "read", model.__tablename__).with_entities(
                    model.id
                )
            ),
        )
        tag_queries.append(tags_query)

    tags_query = (
        tag_queries[0]
        .union(*tag_queries[1:])
        .filter(Tag.name.ilike(f"%{escape_like(filter_term)}%"))
        .distinct()
        .order_by(Tag.name)
    )

    return tags_query


def get_licenses(filter_term=""):
    """Get all licenses.

    :param filter_term: (optional) A (case insensitive) term to filter the licenses by
        their title or name.
    :return: The licenses as query, ordered by their title in ascending order.
    """
    filter_term = escape_like(filter_term)
    licenses_query = License.query.filter(
        db.or_(
            License.title.ilike(f"%{filter_term}%"),
            License.name.ilike(f"%{filter_term}%"),
        )
    ).order_by(License.title)

    return licenses_query


def get_favorite_resources(max_items=6, user=None):
    """Get a list of serialized resources favorited by the given user.

    :param max_items: (optional) The maximum number of resource to return.
    :param user: (optional) The user the favorite resources belong to. Defaults to the
        current user.
    :return: The serialized resources as a list of dictionaries, each resource
        additionally containing its type in a human-readable manner as ``pretty_type``.
    """
    user = user if user is not None else current_user

    resource_queries = []

    for resource_type, resource_meta in RESOURCE_TYPES.items():
        favorite_ids_query = user.favorites.filter(
            Favorite.object == resource_type
        ).with_entities(Favorite.object_id)

        if not favorite_ids_query.count():
            continue

        model = resource_meta["model"]

        # Only query the ID, modification date and type, as the resulting resources will
        # not be serialized as-is.
        resources_query = (
            get_permitted_objects(user, "read", resource_type)
            .filter(
                model.state == const.MODEL_STATE_ACTIVE,
                model.id.in_(favorite_ids_query),
            )
            .with_entities(
                model.id,
                model.last_modified.label("last_modified"),
                db.literal(resource_type).label("type"),
            )
        )

        resource_queries.append(resources_query)

    if not resource_queries:
        return []

    resources = (
        resource_queries[0]
        .union(*resource_queries[1:])
        .order_by(db.desc("last_modified"))
        .limit(max_items)
    )

    serialized_resources = []

    for resource in resources:
        resource_meta = RESOURCE_TYPES[resource.type]

        model = resource_meta["model"]
        schema = resource_meta["schema"](_internal=True)

        serialized_resources.append(
            {
                **schema.dump(model.query.get(resource.id)),
                "pretty_type": resource_meta["title"],
            }
        )

    return serialized_resources


def _get_resource_data(resource_config, user):
    resource_type = resource_config["resource"]
    resource_type_meta = RESOURCE_TYPES[resource_type]

    model = resource_type_meta["model"]
    schema = resource_type_meta["schema"]

    endpoint_args = {}

    if resource_config["creator"] == "any":
        # Only include groups with membership in this case.
        if resource_type == "group":
            resources_query = get_user_groups(user)
            endpoint_args["member_only"] = True
        else:
            resources_query = get_permitted_objects(user, "read", resource_type)
    else:
        resources_query = model.query.filter(model.user_id == user.id)
        endpoint_args["user"] = user.id

    if resource_config["visibility"] != "all":
        resources_query = resources_query.filter(
            model.visibility == resource_config["visibility"]
        )
        endpoint_args["visibility"] = resource_config["visibility"]

    resources = (
        resources_query.filter(model.state == const.MODEL_STATE_ACTIVE)
        .order_by(model.last_modified.desc())
        .limit(resource_config["max_items"])
        .all()
    )

    if not resources:
        return None

    return {
        "title": str(resource_type_meta["title_plural"]),
        "url": url_for(resource_type_meta["endpoint"], **endpoint_args),
        "items": schema(many=True, _internal=True).dump(resources),
    }


def get_latest_resources(user=None):
    """Get a list of serialized resources according to their modification date.

    Uses the home page layout as configured via the user-specific ``"HOME_LAYOUT"``
    config item to determine how many resources of each type to collect.

    :param user: (optional) The user the layout belongs to. Defaults to the current
        user.
    :return: The serialized resources as a list of dictionaries per resource type, each
        containing the localized resource title (``"title"``), the resource search url
        (``"url"``) and the serialized resources themselves (``"items"``).
    """
    user = user if user is not None else current_user

    home_layout = user.get_config(
        const.USER_CONFIG_HOME_LAYOUT, default=const.USER_CONFIG_HOME_LAYOUT_DEFAULT
    )

    serialized_resources = []

    for resource_config in home_layout:
        resource_data = _get_resource_data(resource_config, user)

        if resource_data is not None:
            serialized_resources.append(resource_data)

    return serialized_resources
