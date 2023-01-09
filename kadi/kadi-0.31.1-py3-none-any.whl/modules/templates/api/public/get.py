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
from flask_login import login_required

import kadi.lib.constants as const
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import check_access_token_scopes
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.api.utils import status
from kadi.lib.conversion import normalize
from kadi.lib.conversion import parse_json_object
from kadi.lib.conversion import strip
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.utils import permission_required
from kadi.lib.resources.api import get_resource_group_roles
from kadi.lib.resources.api import get_resource_user_roles
from kadi.lib.revisions.schemas import ObjectRevisionSchema
from kadi.lib.web import download_bytes
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.templates.export import get_export_data
from kadi.modules.templates.models import Template
from kadi.modules.templates.models import TemplateState
from kadi.modules.templates.schemas import TemplateSchema
from kadi.modules.templates.utils import search_templates


@bp.get("/templates")
@login_required
@scopes_required("template.read")
@paginated(page_max=100)
@qparam("query", parse=strip, description="A query to search the templates with.")
@qparam(
    "sort",
    default="_score",
    description="The order of the search results. One of ``_score``, ``last_modified``,"
    " ``-last_modified``, ``created_at``, ``-created_at``, ``title``, ``-title``,"
    " ``identifier`` or ``-identifier``. Falls back to ``-last_modified`` if no search"
    " query is given.",
)
@qparam(
    "visibility",
    description="A visibility value to filter the templates with. One of ``private``"
    " or ``public``.",
)
@qparam(
    "user",
    multiple=True,
    parse=int,
    description="User IDs to filter the templates with in relation to their creator."
    " All given users are filtered using an *OR* operation.",
)
@qparam(
    "type",
    description="A type value to filter the templates with. One of ``record`` or"
    " ``extras``.",
)
@status(200, "Return a paginated list of templates.")
def get_templates(page, per_page, qparams):
    """Search and filter for templates."""
    templates, total_templates = search_templates(
        search_query=qparams["query"],
        page=page,
        per_page=per_page,
        sort=qparams["sort"],
        visibility=qparams["visibility"],
        user_ids=qparams["user"],
        template_type=qparams["type"],
    )

    data = {
        "items": TemplateSchema(many=True).dump(templates),
        "_actions": {"new_template": url_for("api.new_template")},
        **create_pagination_data(total_templates, page, per_page, **qparams),
    }

    return json_response(200, data)


@bp.get("/templates/<int:id>")
@permission_required("read", "template", "id")
@scopes_required("template.read")
@status(200, "Return the template.")
def get_template(id):
    """Get the template specified by the given *id*."""
    template = Template.query.get_active_or_404(id)
    return json_response(200, TemplateSchema().dump(template))


@bp.get("/templates/identifier/<identifier:identifier>")
@login_required
@scopes_required("template.read")
@status(200, "Return the template.")
def get_template_by_identifier(identifier):
    """Get the template specified by the given *identifier*."""
    template = Template.query.filter_by(
        identifier=identifier, state=TemplateState.ACTIVE
    ).first_or_404()

    if not has_permission(current_user, "read", "template", template.id):
        return json_error_response(403)

    return json_response(200, TemplateSchema().dump(template))


@bp.get("/templates/<int:id>/roles/users")
@permission_required("read", "template", "id")
@scopes_required("template.read", "user.read")
@paginated
@qparam(
    "filter",
    parse=strip,
    description="A query to filter the users by their username or display name.",
)
@qparam("exclude", multiple=True, parse=int, description="User IDs to exclude.")
@status(
    200,
    "Return a paginated list of user roles, sorted by role name and then by user ID in"
    " ascending order. The creator will always be listed first.",
)
def get_template_user_roles(id, page, per_page, qparams):
    """Get the user roles of the template specified by the given *id*."""
    template = Template.query.get_active_or_404(id)

    items, total = get_resource_user_roles(
        template,
        page=page,
        per_page=per_page,
        filter_term=qparams["filter"],
        exclude=qparams["exclude"],
    )
    data = {
        "items": items,
        **create_pagination_data(total, page, per_page, id=template.id),
    }

    return json_response(200, data)


@bp.get("/templates/<int:id>/roles/groups")
@permission_required("read", "template", "id")
@scopes_required("template.read", "group.read")
@paginated
@qparam(
    "filter",
    parse=normalize,
    description="A query to filter the groups by their title or identifier.",
)
@status(
    200,
    "Return a paginated list of group roles, sorted by role name and then by group ID"
    " in ascending order.",
)
def get_template_group_roles(id, page, per_page, qparams):
    """Get the group roles of the template specified by the given *id*.

    If a user can manage permissions in this template, all group roles are returned.
    However, groups that a user can normally not read include only a limited subset of
    attributes.
    """
    template = Template.query.get_active_or_404(id)

    items, total = get_resource_group_roles(
        template, page=page, per_page=per_page, filter_term=qparams["filter"]
    )
    data = {
        "items": items,
        **create_pagination_data(total, page, per_page, id=template.id),
    }

    return json_response(200, data)


@bp.get("/templates/<int:id>/revisions")
@permission_required("read", "template", "id")
@scopes_required("template.read")
@paginated
@status(
    200,
    "Return a paginated list of revisions, sorted by revision timestamp in descending"
    " order.",
)
def get_template_revisions(id, page, per_page):
    """Get the revisions of the template specified by the given *id*."""
    template = Template.query.get_active_or_404(id)
    paginated_revisions = template.ordered_revisions.paginate(
        page=page, per_page=per_page, error_out=False
    )

    schema = ObjectRevisionSchema(
        TemplateSchema,
        many=True,
        api_endpoint="api.get_template_revision",
        view_endpoint="templates.view_revision",
        endpoint_args={"template_id": template.id},
    )
    data = {
        "items": schema.dump(paginated_revisions),
        **create_pagination_data(
            paginated_revisions.total, page, per_page, id=template.id
        ),
    }

    return json_response(200, data)


@bp.get("/templates/<int:template_id>/revisions/<int:revision_id>")
@permission_required("read", "template", "template_id")
@scopes_required("template.read")
@qparam(
    "revision",
    default=None,
    parse=int,
    description="The ID of a revision to compare with instead of the previous one.",
)
@status(200, "Return the revision.")
def get_template_revision(template_id, revision_id, qparams):
    """Get a template revision.

    Will return the revision specified by the given *revision_id* of the template
    specified by the given *template_id*.
    """
    template = Template.query.get_active_or_404(template_id)
    revision = template.revisions.filter(
        Template.revision_class.id == revision_id
    ).first_or_404()

    compared_revision = None

    if qparams["revision"]:
        compared_revision = template.revisions.filter(
            Template.revision_class.id == qparams["revision"]
        ).first()

    schema = ObjectRevisionSchema(
        TemplateSchema,
        compared_revision=compared_revision,
        api_endpoint="api.get_template_revision",
        view_endpoint="templates.view_revision",
        endpoint_args={"template_id": template.id},
    )

    return json_response(200, schema.dump(revision))


@bp.get("/templates/<int:id>/export/<export_type>")
@permission_required("read", "template", "id")
@scopes_required("template.read")
@qparam(
    "filter",
    default=lambda: {},
    parse=parse_json_object,
    description="An URL-encoded JSON object to specify various filters to exclude"
    " certain information from the returned export data. See the ``export_filter``"
    " parameter in :func:`kadi.modules.templates.export.get_export_data` for a more"
    " detailed description (in Python syntax).",
)
@status(200, "Return the exported template data.")
def get_template_export(id, export_type, qparams):
    """Export the template specified by the given *id* using a specific *export_type*.

    Currently ``json`` and ``json-schema`` are supported as export types.
    """
    template = Template.query.get_active_or_404(id)
    export_types = const.EXPORT_TYPES["template"]

    if export_type not in export_types:
        return json_error_response(404)

    export_filter = qparams["filter"]

    # Always exclude the user information if the access token scopes are insufficient.
    if not check_access_token_scopes("user.read"):
        export_filter["user"] = True

    data = get_export_data(template, export_type, export_filter=export_filter)
    return download_bytes(data, f"{template.identifier}.json")
