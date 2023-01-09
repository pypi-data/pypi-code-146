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
from flask_login import current_user

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import reqform
from kadi.lib.api.utils import reqschema
from kadi.lib.api.utils import status
from kadi.lib.exceptions import KadiChecksumMismatchError
from kadi.lib.exceptions import KadiFilesizeExceededError
from kadi.lib.exceptions import KadiFilesizeMismatchError
from kadi.lib.permissions.utils import permission_required
from kadi.lib.storage.core import get_storage
from kadi.modules.records.api.utils import check_storage_compatibility
from kadi.modules.records.api.utils import check_upload_user_quota
from kadi.modules.records.forms import ChunkForm
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.records.models import Upload
from kadi.modules.records.models import UploadState
from kadi.modules.records.models import UploadType
from kadi.modules.records.schemas import UploadSchema
from kadi.modules.records.uploads import save_chunk


@bp.put("/records/<int:record_id>/files/<uuid:file_id>")
@permission_required("update", "record", "record_id")
@scopes_required("record.update")
@reqschema(
    UploadSchema(exclude=["name"]), description="The metadata of the new upload."
)
@status(
    201,
    "Return the new upload. Additionally, the required size for uploading file chunks"
    " is returned as the ``_meta.chunk_size`` property.",
)
@status(413, "An upload quota was exceeded.")
def edit_file_data(record_id, file_id, schema):
    """Change the data of a file of a record via a new chunked upload.

    Will initiate a new chunked upload in the record specified by the given *record_id*
    replacing the data of the file specified by the given *file_id*. Once the new upload
    is initiated, the actual file chunks can be uploaded by sending one or more *PUT*
    requests to the endpoint specified in the ``_actions.upload_chunk`` property of the
    upload.
    """
    record = Record.query.get_active_or_404(record_id)
    file = record.active_files.filter(File.id == file_id).first_or_404()

    data = schema.load_or_400()

    response = check_storage_compatibility(
        file.storage, get_storage(data["storage"]["storage_type"])
    )
    if response is not None:
        return response

    # Since the upload replaces a file, the quota check needs to take this into account.
    response = check_upload_user_quota(additional_size=data["size"] - file.size)

    if response is not None:
        return response

    # If no MIME type was provided, take the one from the previous file.
    if "mimetype" not in data:
        data["mimetype"] = file.mimetype

    # If no description was provided, take the one from the previous file.
    if "description" not in data:
        data["description"] = file.description

    upload = Upload.create(
        creator=current_user,
        record=record,
        file=file,
        upload_type=UploadType.CHUNKED,
        name=file.name,
        **data,
    )
    db.session.commit()

    data = {
        **UploadSchema().dump(upload),
        "_meta": {"chunk_size": current_app.config["UPLOAD_CHUNK_SIZE"]},
    }

    return json_response(201, data)


@bp.put("/records/<int:record_id>/uploads/<uuid:upload_id>")
@permission_required("update", "record", "record_id")
@scopes_required("record.update")
@reqform(
    [
        ("checksum", {"type": "String"}),
        ("index", {"type": "Integer", "required": True}),
        ("size", {"type": "Integer", "required": True}),
        ("blob", {"type": "File", "required": True}),
    ],
    description="The actual data and metadata of the chunk to upload. Indices start at"
    " ``0`` for each file and need to be incremented in order of the file chunks.",
)
@status(200, "Return the updated upload.")
@status(413, "An upload quota was exceeded.")
def upload_chunk(record_id, upload_id):
    """Upload a chunk of a chunked upload.

    Will upload a chunk of the upload specified by the given *upload_id* of the record
    specified by the given *record_id*. Once all chunks have been uploaded, the upload
    can be finished by sending a *POST* request to the endpoint specified in the
    ``_actions.finish_upload`` property of the upload. Only uploads owned by the current
    user can be updated.
    """
    record = Record.query.get_active_or_404(record_id)
    upload = record.uploads.filter(
        Upload.id == upload_id,
        Upload.user_id == current_user.id,
        Upload.state == UploadState.ACTIVE,
        Upload.upload_type == UploadType.CHUNKED,
    ).first_or_404()

    chunk_size = current_app.config["UPLOAD_CHUNK_SIZE"]
    form = ChunkForm(upload.chunk_count, chunk_size)

    if not form.validate():
        return json_error_response(400, errors=form.errors)

    # Check the quota again when uploading chunks. If the upload replaces a file, the
    # quota check needs to take this into account.
    response = check_upload_user_quota(
        additional_size=-upload.file.size if upload.file else 0
    )
    if response is not None:
        return response

    try:
        save_chunk(
            upload=upload,
            file_object=form.blob.data,
            index=form.index.data,
            size=form.size.data,
            checksum=form.checksum.data,
        )
        return json_response(200, UploadSchema().dump(upload))
    except (
        KadiFilesizeExceededError,
        KadiFilesizeMismatchError,
        KadiChecksumMismatchError,
    ) as e:
        return json_error_response(400, description=str(e))
