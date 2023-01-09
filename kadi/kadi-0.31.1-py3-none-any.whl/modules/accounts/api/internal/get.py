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
from flask import abort
from flask import current_app
from flask import redirect
from flask import render_template
from flask import send_file
from flask_login import current_user
from flask_login import login_required

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.conversion import strip
from kadi.lib.db import escape_like
from kadi.lib.favorites.models import Favorite
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.utils import get_user_roles
from kadi.lib.resources import RESOURCE_TYPES
from kadi.lib.storage.misc import create_misc_storage
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.accounts.models import UserState


@bp.get("/users/<int:id>/image", v=None)
@login_required
@internal
def preview_user_image(id):
    """Preview a user's image thumbnail directly in the browser."""
    user = User.query.get_or_404(id)

    if user.is_merged:
        return redirect(
            url_for("api.preview_user_image", id=user.new_user_id), code=301
        )

    if user.image_name:
        storage = create_misc_storage()
        filepath = storage.create_filepath(str(user.image_name))

        if storage.exists(filepath):
            return send_file(
                filepath,
                mimetype="image/jpeg",
                download_name=f"{user.identity.username}.jpg",
            )

    return json_error_response(404)


@bp.get("/users/favorites/<resource_type>", v=None)
@login_required
@internal
@paginated
def get_favorite_resources(resource_type, page, per_page):
    """Get all favorited resources of a specific type of the current user."""
    if resource_type not in RESOURCE_TYPES:
        abort(404)

    model = RESOURCE_TYPES[resource_type]["model"]
    schema = RESOURCE_TYPES[resource_type]["schema"]

    paginated_resources = (
        get_permitted_objects(current_user, "read", resource_type)
        .filter(
            model.state == const.MODEL_STATE_ACTIVE,
            model.id.in_(
                current_user.favorites.filter(
                    Favorite.object == resource_type
                ).with_entities(Favorite.object_id)
            ),
        )
        .order_by(model.last_modified.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    data = {
        "items": schema(many=True).dump(paginated_resources),
        **create_pagination_data(
            paginated_resources.total, page, per_page, resource_type=resource_type
        ),
    }

    return json_response(200, data)


@bp.get("/users/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=strip)
@qparam("exclude", multiple=True, parse=int)
@qparam("resource_type")
@qparam("resource_id", default=None, parse=int)
def select_users(qparams):
    """Search users in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Note that users
    with multiple identities are only returned once, using their latest identity, and
    merged users are always excluded, as they do not have any identities anymore.
    """
    filter_term = escape_like(qparams["term"])
    excluded_ids = qparams["exclude"]
    resource_type = qparams["resource_type"]
    resource_id = qparams["resource_id"]

    # If applicable, exclude users that already have any role in the specified resource.
    if resource_type in RESOURCE_TYPES and resource_id is not None:
        model = RESOURCE_TYPES[resource_type]["model"]
        resource = model.query.get_active(resource_id)

        if resource is not None and has_permission(
            current_user, "read", resource_type, resource_id
        ):
            user_ids_query = get_user_roles(
                resource_type, object_id=resource_id
            ).with_entities(User.id)
            excluded_ids += [u.id for u in user_ids_query]

    identity_queries = []

    for provider_config in current_app.config["AUTH_PROVIDERS"].values():
        model = provider_config["identity_class"]

        identities_query = (
            model.query.join(User, User.latest_identity_id == model.id)
            .filter(
                User.state == UserState.ACTIVE,
                User.id.notin_(excluded_ids),
                db.or_(
                    model.displayname.ilike(f"%{filter_term}%"),
                    model.username.ilike(f"%{filter_term}%"),
                ),
            )
            .with_entities(
                model.user_id,
                model.username,
                model.displayname.label("displayname"),
                db.literal(str(model.Meta.identity_type["name"])).label("type"),
            )
        )

        identity_queries.append(identities_query)

    paginated_identities = (
        identity_queries[0]
        .union(*identity_queries[1:])
        .order_by("displayname")
        .paginate(page=qparams["page"], per_page=10, error_out=False)
    )

    data = {
        "results": [],
        "pagination": {"more": paginated_identities.has_next},
    }
    for identity in paginated_identities:
        data["results"].append(
            {
                "id": identity.user_id,
                "text": f"@{identity.username}",
                "body": render_template(
                    "accounts/snippets/select_user.html",
                    displayname=identity.displayname,
                    username=identity.username,
                    type=identity.type,
                ),
            }
        )

    return json_response(200, data)
