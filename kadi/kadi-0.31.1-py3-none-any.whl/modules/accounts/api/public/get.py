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
from flask import current_app
from flask import redirect
from flask import request
from flask_login import current_user
from flask_login import login_required
from sqlalchemy import true

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.api.utils import status
from kadi.lib.conversion import normalize
from kadi.lib.conversion import parse_boolean_string
from kadi.lib.conversion import strip
from kadi.lib.db import escape_like
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.resources import RESOURCE_TYPES
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import Identity
from kadi.modules.accounts.models import User
from kadi.modules.accounts.models import UserState
from kadi.modules.accounts.schemas import IdentitySchema
from kadi.modules.accounts.schemas import UserSchema
from kadi.modules.accounts.utils import get_filtered_user_ids
from kadi.modules.groups.models import Group
from kadi.modules.groups.models import GroupState
from kadi.modules.groups.schemas import GroupSchema
from kadi.modules.groups.utils import get_user_groups as _get_user_groups


@bp.get("/users")
@login_required
@scopes_required("user.read")
@paginated
@qparam(
    "filter",
    parse=strip,
    description="A query to filter the users by their display name or username.",
)
@qparam(
    "inactive",
    default=False,
    parse=parse_boolean_string,
    description="Flag indicating whether inactive users should be returned as well.",
)
@qparam(
    "sysadmins",
    default=False,
    parse=parse_boolean_string,
    description="Flag indicating whether only users marked as sysadmin should be"
    " returned.",
)
@status(
    200,
    "Return a paginated list of users, sorted by creation date in descending order.",
)
def get_users(page, per_page, qparams):
    """Get all users."""
    states = [UserState.ACTIVE]

    if qparams["inactive"]:
        states.append(UserState.INACTIVE)

    users_query = User.query.filter(
        User.id.in_(get_filtered_user_ids(qparams["filter"])), User.state.in_(states)
    )

    if qparams["sysadmins"]:
        users_query = users_query.filter(User.is_sysadmin == true())

    paginated_users = users_query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    data = {
        "items": UserSchema(many=True).dump(paginated_users),
        **create_pagination_data(paginated_users.total, page, per_page, **qparams),
    }

    return json_response(200, data)


@bp.get("/users/me")
@login_required
@scopes_required("user.read")
@status(200, "Return the current user.")
def get_current_user():
    """Get the current user."""
    return json_response(200, UserSchema().dump(current_user))


@bp.get("/users/<int:id>")
@login_required
@scopes_required("user.read")
@status(200, "Return the user.")
def get_user(id):
    """Get the user specified by the given *id*."""
    user = User.query.get_or_404(id)

    if user.is_merged:
        return redirect(url_for("api.get_user", id=user.new_user_id), code=301)

    return json_response(200, UserSchema().dump(user))


@bp.get("/users/<identity_type>/<username>")
@login_required
@scopes_required("user.read")
@status(200, "Return the user.")
def get_user_by_identity(identity_type, username):
    """Get the user specified by the given *identity_type* and *username*."""
    provider = current_app.config["AUTH_PROVIDERS"].get(identity_type)

    if provider is None:
        return json_error_response(404)

    identity_class = provider["identity_class"]
    identity = identity_class.query.filter_by(username=username).first_or_404()

    # No need to check whether the user was merged, as all identities are migrated to
    # the new user.
    return json_response(200, UserSchema().dump(identity.user))


@bp.get("/users/<int:id>/identities")
@login_required
@scopes_required("user.read")
@status(200, "Return a list of identities, sorted by type.")
def get_user_identities(id):
    """Get all identities of the user specified by the given *id*."""
    user = User.query.get_or_404(id)

    if user.is_merged:
        return redirect(
            url_for("api.get_user_identities", id=user.new_user_id), code=301
        )

    identities = user.identities.order_by(Identity.type)
    return json_response(200, IdentitySchema(many=True).dump(identities))


def _get_user_resources(resource_type, user_id, page, per_page, qparams):
    user = User.query.get_or_404(user_id)

    if user.is_merged:
        return redirect(url_for(request.endpoint, id=user.new_user_id), code=301)

    resource_creator = user
    resource_viewer = current_user

    if qparams["shared"]:
        resource_creator = current_user
        resource_viewer = user

    model = RESOURCE_TYPES[resource_type]["model"]
    schema = RESOURCE_TYPES[resource_type]["schema"]

    # Do not check the default permissions when retrieving the (explicitly) shared
    # resources.
    object_ids_query = get_permitted_objects(
        resource_viewer, "read", resource_type, check_defaults=not qparams["shared"]
    ).with_entities(model.id)

    filter_term = escape_like(qparams["filter"])
    paginated_resources = (
        model.query.filter(
            model.state == const.MODEL_STATE_ACTIVE,
            model.user_id == resource_creator.id,
            model.id.in_(object_ids_query),
            db.or_(
                model.title.ilike(f"%{filter_term}%"),
                model.identifier.ilike(f"%{filter_term}%"),
            ),
        )
        .order_by(model.last_modified.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    data = {
        "items": schema(many=True).dump(paginated_resources),
        **create_pagination_data(
            paginated_resources.total, page, per_page, id=user.id, **qparams
        ),
    }

    return json_response(200, data)


@bp.get("/users/<int:id>/records")
@login_required
@scopes_required("user.read", "record.read")
@paginated
@qparam(
    "filter",
    parse=normalize,
    description="A query to filter the records by their title or identifier.",
)
@qparam(
    "shared",
    default=False,
    parse=parse_boolean_string,
    description="Flag indicating whether records the user created should be returned or"
    " records created by the current user that were explicitly shared with the user.",
)
@status(
    200,
    "Return a list of paginated records, sorted by last modification date in descending"
    " order.",
)
def get_user_records(id, page, per_page, qparams):
    """Get all created or shared records of the user specified by the given *id*.

    Shared means that the user needs to have at least explicit read permission for a
    record.
    """
    return _get_user_resources("record", id, page, per_page, qparams)


@bp.get("/users/<int:id>/collections")
@login_required
@scopes_required("user.read", "collection.read")
@paginated
@qparam(
    "filter",
    parse=normalize,
    description="A query to filter the collections by their title or identifier.",
)
@qparam(
    "shared",
    default=False,
    parse=parse_boolean_string,
    description="Flag indicating whether collections the user created should be"
    " returned or collections created by the current user that were explicitly shared"
    " with the user.",
)
@status(
    200,
    "Return a list of paginated collections, sorted by last modification date in"
    " descending order.",
)
def get_user_collections(id, page, per_page, qparams):
    """Get all created or shared collections of the user specified by the given *id*.

    Shared means that the user needs to have at least explicit read permission for a
    collection.
    """
    return _get_user_resources("collection", id, page, per_page, qparams)


@bp.get("/users/<int:id>/templates")
@login_required
@scopes_required("user.read", "template.read")
@paginated
@qparam(
    "filter",
    parse=normalize,
    description="A query to filter the templates by their title or identifier.",
)
@qparam(
    "shared",
    default=False,
    parse=parse_boolean_string,
    description="Flag indicating whether templates the user created should be returned"
    " or templates created by the current user that were explicitly shared with the"
    " user.",
)
@status(
    200,
    "Return a list of paginated templates, sorted by last modification date in"
    " descending order.",
)
def get_user_templates(id, page, per_page, qparams):
    """Get all created or shared templates of the user specified by the given *id*.

    Shared means that the user needs to have at least read permission for a template.
    """
    return _get_user_resources("template", id, page, per_page, qparams)


@bp.get("/users/<int:id>/groups")
@login_required
@scopes_required("user.read", "group.read")
@paginated
@qparam(
    "filter",
    parse=normalize,
    description="A query to filter the groups by their title or identifier.",
)
@qparam(
    "common",
    default=False,
    parse=parse_boolean_string,
    description="Flag indicating whether groups the user created should be returned or"
    " groups that the current user and the specified user have in common regarding"
    " group membership.",
)
@status(
    200,
    "Return a list of paginated groups, sorted by last modification date in descending"
    " order.",
)
def get_user_groups(id, page, per_page, qparams):
    """Get all created or common groups of the user specified by the given *id*.

    Common means that both the current and the specified user need to be a member of a
    group.
    """
    user = User.query.get_or_404(id)

    if user.is_merged:
        return redirect(url_for("api.get_user_groups", id=user.new_user_id), code=301)

    if qparams["common"]:
        # No need to check the permissions separately in this case because of the
        # intersection.
        user_groups = _get_user_groups(user).intersect(_get_user_groups(current_user))
    else:
        user_groups = user.groups.filter(
            Group.state == GroupState.ACTIVE,
            Group.id.in_(
                get_permitted_objects(current_user, "read", "group").with_entities(
                    Group.id
                )
            ),
        )

    filter_term = escape_like(qparams["filter"])
    paginated_groups = (
        user_groups.filter(
            db.or_(
                Group.title.ilike(f"%{filter_term}%"),
                Group.identifier.ilike(f"%{filter_term}%"),
            )
        )
        .order_by(Group.last_modified.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    data = {
        "items": GroupSchema(many=True).dump(paginated_groups),
        **create_pagination_data(
            paginated_groups.total, page, per_page, id=user.id, **qparams
        ),
    }

    return json_response(200, data)
