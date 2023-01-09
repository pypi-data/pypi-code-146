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
from flask import redirect
from flask import render_template
from flask import request
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import login_required

import kadi.lib.constants as const
from .blueprint import bp
from .core import create_record
from .core import delete_record as _delete_record
from .core import update_record
from .files import delete_file as _delete_file
from .files import get_direct_upload_type
from .files import update_file
from .forms import AddRolesForm
from .forms import EditFileForm
from .forms import EditRecordForm
from .forms import EditRecordLinkForm
from .forms import LinkCollectionsForm
from .forms import NewRecordForm
from .forms import NewRecordLinkForm
from .links import create_record_link
from .links import get_record_changes
from .links import remove_record_link as _remove_record_link
from .links import update_record_link
from .models import File
from .models import FileState
from .models import Record
from .models import RecordLink
from .schemas import FileSchema
from .schemas import RecordSchema
from kadi.ext.db import db
from kadi.lib.conversion import parse_boolean_string
from kadi.lib.exceptions import KadiPermissionError
from kadi.lib.exceptions import KadiValidationError
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.utils import permission_required
from kadi.lib.publication import get_publication_provider
from kadi.lib.publication import get_publication_providers
from kadi.lib.resources.tasks import start_publish_resource_task
from kadi.lib.resources.views import add_links
from kadi.lib.resources.views import update_roles
from kadi.lib.storage.core import get_storages
from kadi.lib.validation import validate_uuid
from kadi.lib.web import flash_danger
from kadi.lib.web import flash_info
from kadi.lib.web import flash_success
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.collections.models import Collection
from kadi.modules.collections.models import CollectionState
from kadi.modules.templates.models import Template
from kadi.modules.templates.models import TemplateType


@bp.get("")
@login_required
@qparam("user", multiple=True, parse=int)
@qparam("collection", multiple=True, parse=int)
def records(qparams):
    """Record overview page.

    Allows users to search and filter for records or create new ones.
    """
    users = []
    collections = []

    if qparams["user"]:
        users = User.query.filter(User.id.in_(qparams["user"]))

    if qparams["collection"]:
        collections = (
            get_permitted_objects(current_user, "read", "collection")
            .filter(
                Collection.state == CollectionState.ACTIVE,
                Collection.id.in_(qparams["collection"]),
            )
            .with_entities(Collection.id, Collection.identifier)
        )

    return render_template(
        "records/records.html",
        title=_("Records"),
        js_context={
            "new_record_endpoint": url_for("records.new_record"),
            "users": [(u.id, f"@{u.identity.username}") for u in users],
            "collections": [(c.id, f"@{c.identifier}") for c in collections],
        },
    )


@bp.route("/new", methods=["GET", "POST"])
@permission_required("create", "record", None)
@qparam("record", default=None, parse=int)
@qparam("template", default=None, parse=int)
@qparam("collection", default=None, parse=int)
@qparam("redirect", default="files")
def new_record(qparams):
    """Page to create a new record."""
    copied_record = None
    current_template = None
    linked_collection = None

    if request.method == "GET":
        # Copy a record's metadata.
        if qparams["record"] is not None:
            copied_record = Record.query.get_active(qparams["record"])

            if copied_record is not None and not has_permission(
                current_user, "read", "record", copied_record.id
            ):
                copied_record = None

        # Apply a "record" or "extras" template.
        if qparams["template"] is not None:
            current_template = Template.query.get_active(qparams["template"])

            if current_template is not None and (
                current_template.type not in [TemplateType.RECORD, TemplateType.EXTRAS]
                or not has_permission(
                    current_user, "read", "template", current_template.id
                )
            ):
                current_template = None

        # Directly link a record with a collection.
        if qparams["collection"] is not None:
            linked_collection = Collection.query.get_active(qparams["collection"])

            if linked_collection is not None and (
                not has_permission(
                    current_user, "read", "collection", linked_collection.id
                )
                or not has_permission(
                    current_user, "link", "collection", linked_collection.id
                )
            ):
                linked_collection = None

    form = NewRecordForm(
        record=copied_record, template=current_template, collection=linked_collection
    )

    if request.method == "POST":
        if form.validate():
            record = create_record(
                title=form.title.data,
                identifier=form.identifier.data,
                type=form.type.data,
                description=form.description.data,
                license=form.license.data,
                visibility=form.visibility.data,
                tags=form.tags.data,
                extras=form.extras.data,
            )

            if record:
                add_links(Collection, record.collections, form.collections.data)
                update_roles(record, form.roles.data)
                db.session.commit()

                flash_success(_("Record created successfully."))
                return redirect(
                    url_for("records.add_files", id=record.id, tab=qparams["redirect"])
                )

        flash_danger(_("Error creating record."))

    record_template = (
        current_template
        if current_template is not None
        and current_template.type == TemplateType.RECORD
        and copied_record is None
        else None
    )

    return render_template(
        "records/new_record.html",
        title=_("New record"),
        form=form,
        record_template=record_template,
        show_template_selection=copied_record is None,
        redirect=qparams["redirect"],
        js_context={"title_field": form.title.to_dict()},
    )


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@permission_required("update", "record", "id")
@qparam("key", multiple=True)
def edit_record(id, qparams):
    """Page to edit an existing record."""
    record = Record.query.get_active_or_404(id)
    form = EditRecordForm(record)

    if request.method == "POST":
        if form.validate():
            if update_record(
                record,
                title=form.title.data,
                identifier=form.identifier.data,
                type=form.type.data,
                description=form.description.data,
                license=form.license.data,
                visibility=form.visibility.data,
                tags=form.tags.data,
                extras=form.extras.data,
            ):
                flash_success(_("Changes saved successfully."))

                if form.submit_quit.data:
                    return redirect(url_for("records.view_record", id=record.id))

                return redirect(url_for("records.edit_record", id=record.id))

        flash_danger(_("Error editing record."))

    return render_template(
        "records/edit_record.html",
        title=_("Edit record"),
        form=form,
        record=record,
        js_context={
            "title_field": form.title.to_dict(),
            "edit_extra_keys": qparams["key"],
        },
    )


@bp.get("/<int:id>")
@permission_required("read", "record", "id")
def view_record(id):
    """Page to view a record."""
    record = Record.query.get_active_or_404(id)
    schema = RecordSchema(only=["id", "title", "identifier"])

    return render_template(
        "records/view_record.html",
        record=record,
        publication_providers=get_publication_providers(record),
        FileState=FileState,
        js_context={"record": schema.dump(record)},
    )


@bp.get("/<int:id>/export/<export_type>")
@permission_required("read", "record", "id")
def export_record(id, export_type):
    """Page to view the exported data of a record.

    Currently ``"json"`` and ``"qr"`` are supported as export type.
    """
    record = Record.query.get_active_or_404(id)
    export_types = const.EXPORT_TYPES["record"]

    if export_type not in export_types:
        abort(404)

    return render_template(
        "records/export_record.html",
        title=export_types[export_type],
        record=record,
        export_type=export_type,
    )


@bp.route("/<int:id>/publish/<provider>", methods=["GET", "POST"])
@permission_required("read", "record", "id")
def publish_record(id, provider):
    """Page to publish a record using a given provider."""
    record = Record.query.get_active_or_404(id)
    publication_provider = get_publication_provider(provider, record)

    if publication_provider is None:
        abort(404)

    if request.method == "POST":
        endpoint = url_for("records.publish_record", id=record.id, provider=provider)

        if not publication_provider["is_connected"]:
            return redirect(endpoint)

        status, task = start_publish_resource_task(provider, record, dict(request.form))

        if not status:
            flash_info(_("A publishing task is already in progress."))
        elif not task:
            flash_danger(_("Error starting publishing task."))
        else:
            flash_success(_("Publishing task started successfully."))

        return redirect(endpoint)

    return render_template(
        "records/publish_record.html",
        title=publication_provider["title"],
        record=record,
        provider=publication_provider,
    )


@bp.route("/<int:id>/links", methods=["GET", "POST"])
@permission_required("link", "record", "id")
@qparam("tab", default="records")
def manage_links(id, qparams):
    """Page to link a record to other records or collections."""
    record = Record.query.get_active_or_404(id)

    record_form = NewRecordLinkForm(suffix="record")
    collections_form = LinkCollectionsForm(suffix="collections")

    if qparams["tab"] == "records" and request.method == "POST":
        if record_form.validate():
            linked_record = Record.query.get_active(record_form.record.data)

            if linked_record is not None:
                link_direction = record_form.link_direction.data
                record_from = record if link_direction == "out" else linked_record
                record_to = linked_record if link_direction == "out" else record

                try:
                    create_record_link(
                        record_from=record_from,
                        record_to=record_to,
                        name=record_form.name.data,
                        term=record_form.term.data,
                    )

                    flash_success(_("Record link created successfully."))
                    return redirect(url_for("records.manage_links", id=record.id))

                except (ValueError, KadiPermissionError) as e:
                    flash_danger(str(e))
        else:
            flash_danger(_("Error creating record link."))

    if qparams["tab"] == "collections" and collections_form.validate_on_submit():
        add_links(Collection, record.collections, collections_form.collections.data)
        db.session.commit()

        flash_success(_("Changes saved successfully."))

    return render_template(
        "records/manage_links.html",
        title=_("Manage links"),
        record_form=record_form,
        collections_form=collections_form,
        record=record,
    )


def _check_record_link_permissions(record, record_link, action):
    if record.id not in {record_link.record_from_id, record_link.record_to_id}:
        abort(404)

    if record_link.record_from_id == record.id:
        linked_record_id = record_link.record_to_id
    else:
        linked_record_id = record_link.record_from_id

    if not has_permission(current_user, action, "record", linked_record_id):
        abort(403)


@bp.get("/<int:record_id>/links/<int:link_id>")
@permission_required("read", "record", "record_id")
def view_record_link(record_id, link_id):
    """Page to view a record link."""
    record = Record.query.get_active_or_404(record_id)
    record_link = RecordLink.query.get_or_404(link_id)

    _check_record_link_permissions(record, record_link, "read")

    record_changes = get_record_changes(record_link)

    return render_template(
        "records/view_record_link.html",
        record=record,
        record_link=record_link,
        record_changes=record_changes,
    )


@bp.route("/<int:record_id>/links/<int:link_id>/edit", methods=["GET", "POST"])
@permission_required("link", "record", "record_id")
def edit_record_link(record_id, link_id):
    """Page to edit an existing record link."""
    record = Record.query.get_active_or_404(record_id)
    record_link = RecordLink.query.get_or_404(link_id)

    _check_record_link_permissions(record, record_link, "link")

    form = EditRecordLinkForm(record_link)

    if request.method == "POST":
        if form.validate():
            try:
                update_record_link(
                    record_link, name=form.name.data, term=form.term.data
                )

                flash_success(_("Changes saved successfully."))
                return redirect(
                    url_for(
                        "records.view_record_link",
                        record_id=record.id,
                        link_id=record_link.id,
                    )
                )
            except (ValueError, KadiPermissionError) as e:
                flash_danger(str(e))
        else:
            flash_danger(_("Error editing record link."))

    return render_template(
        "records/edit_record_link.html",
        title=_("Edit record link"),
        record=record,
        record_link=record_link,
        form=form,
    )


@bp.route("/<int:id>/permissions", methods=["GET", "POST"])
@permission_required("permissions", "record", "id")
def manage_permissions(id):
    """Page to manage access permissions of a record."""
    record = Record.query.get_active_or_404(id)
    form = AddRolesForm()

    if form.validate_on_submit():
        update_roles(record, form.roles.data)
        db.session.commit()

        flash_success(_("Changes saved successfully."))
        return redirect(url_for("records.manage_permissions", id=record.id))

    return render_template(
        "records/manage_permissions.html",
        title=_("Manage permissions"),
        form=form,
        record=record,
    )


@bp.get("/<int:id>/files")
@permission_required("update", "record", "id")
@qparam("file")
def add_files(id, qparams):
    """Page to add files to a record."""
    record = Record.query.get_active_or_404(id)

    file_upload_type = None
    current_file = None
    current_file_data = None

    try:
        validate_uuid(qparams["file"])
        current_file = record.active_files.filter(File.id == qparams["file"]).first()
        file_upload_type = get_direct_upload_type(current_file)
    except KadiValidationError:
        pass

    if file_upload_type is not None:
        current_file_data = FileSchema().dump(current_file)

    return render_template(
        "records/add_files.html",
        title=_("Add files"),
        record=record,
        current_file=current_file,
        js_context={
            "file_type": file_upload_type,
            "current_file": current_file_data,
            "storage_types": [
                {"id": key, "title": storage.storage_name}
                for key, storage in get_storages().items()
            ],
        },
    )


@bp.get("/<int:record_id>/files/<uuid:file_id>")
@permission_required("read", "record", "record_id")
def view_file(record_id, file_id):
    """Page to view a file of a record."""
    record = Record.query.get_active_or_404(record_id)
    file = record.active_files.filter(File.id == file_id).first_or_404()

    prev_file = (
        record.active_files.filter(File.last_modified > file.last_modified)
        .order_by(File.last_modified.asc())
        .first()
    )
    next_file = (
        record.active_files.filter(File.last_modified < file.last_modified)
        .order_by(File.last_modified.desc())
        .first()
    )

    return render_template(
        "records/view_file.html",
        record=record,
        file=file,
        prev_file=prev_file,
        next_file=next_file,
        js_context={
            "get_file_preview_endpoint": url_for(
                "api.get_file_preview", record_id=record.id, file_id=file.id
            )
        },
    )


@bp.route("/<int:record_id>/files/<uuid:file_id>/edit", methods=["GET", "POST"])
@permission_required("update", "record", "record_id")
def edit_file_metadata(record_id, file_id):
    """Page to edit the metadata of an an existing file of a record."""
    record = Record.query.get_active_or_404(record_id)
    file = record.active_files.filter(File.id == file_id).first_or_404()

    form = EditFileForm(file)

    if form.validate_on_submit():
        if update_file(
            file,
            name=form.name.data,
            mimetype=form.mimetype.data,
            description=form.description.data,
        ):
            flash_success(_("Changes saved successfully."))
            return redirect(
                url_for("records.view_file", record_id=record.id, file_id=file.id)
            )

        flash_danger(_("Error editing file."))

    return render_template(
        "records/edit_file_metadata.html",
        title=_("Edit file"),
        form=form,
        record=record,
        file=file,
    )


@bp.get("/<int:record_id>/revisions/<int:revision_id>")
@permission_required("read", "record", "record_id")
@qparam("compare_latest", default=False, parse=parse_boolean_string)
def view_record_revision(record_id, revision_id, qparams):
    """Page to view a specific revision of a record."""
    record = Record.query.get_active_or_404(record_id)
    revision = record.revisions.filter(
        Record.revision_class.id == revision_id
    ).first_or_404()

    return render_template(
        "records/view_revision.html",
        title=_("Revision"),
        record=record,
        revision=revision,
        js_context={"compare_latest": qparams["compare_latest"]},
    )


@bp.get("/<int:record_id>/files/revisions/<int:revision_id>")
@permission_required("read", "record", "record_id")
def view_file_revision(record_id, revision_id):
    """Page to view a specific file revision of a record."""
    record = Record.query.get_active_or_404(record_id)
    revision = File.revision_class.query.get_or_404(revision_id)

    if record.id != revision.file.record_id:
        abort(404)

    return render_template(
        "records/view_revision.html",
        title=_("Revision"),
        record=record,
        revision=revision,
    )


@bp.post("/<int:id>/delete")
@permission_required("delete", "record", "id")
def delete_record(id):
    """Endpoint to delete an existing record.

    Works the same as the corresponding API endpoint.
    """
    record = Record.query.get_active_or_404(id)
    _delete_record(record)

    flash_success(_("Record deleted successfully."))
    return redirect(url_for("records.records"))


@bp.post("/<int:record_id>/links/<int:link_id>/delete")
@permission_required("link", "record", "record_id")
def remove_record_link(record_id, link_id):
    """Endpoint to delete an existing record link.

    Works the same as the corresponding API endpoint.
    """
    record = Record.query.get_active_or_404(record_id)
    record_link = RecordLink.query.get_or_404(link_id)

    _check_record_link_permissions(record, record_link, "link")

    try:
        _remove_record_link(record_link)
        flash_success(_("Record link removed successfully."))
    except KadiPermissionError:
        pass

    return redirect(url_for("records.view_record", id=record.id, tab="links"))


@bp.post("/<int:record_id>/files/<uuid:file_id>/delete")
@permission_required("update", "record", "record_id")
def delete_file(record_id, file_id):
    """Endpoint to delete an existing file.

    Works the same as the corresponding API endpoint.
    """
    record = Record.query.get_active_or_404(record_id)
    file = record.active_files.filter(File.id == file_id).first_or_404()

    _delete_file(file)

    flash_success(_("File deleted successfully."))
    return redirect(url_for("records.view_record", id=record.id, tab="files"))
