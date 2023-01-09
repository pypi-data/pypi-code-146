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
from io import BytesIO

import qrcode
from flask import json
from flask_login import current_user

from .schemas import CollectionSchema
from kadi.lib.resources.utils import get_linked_resources
from kadi.lib.web import url_for
from kadi.modules.records.export import get_dict_data as get_record_dict_data
from kadi.modules.records.export import RecordROCrate
from kadi.modules.records.models import Record


def get_json_data(collection, export_filter, user):
    """Export a collection as a JSON file.

    See :func:`get_export_data` for an explanation of the parameters and return value.
    """

    # Unnecessary meta attributes to exclude, also depending on whether user information
    # should be excluded.
    if export_filter.get("user", False):
        exclude_attrs = ["_actions", "_links", "creator"]
    else:
        exclude_attrs = ["_actions", "_links", "creator._actions", "creator._links"]

    # Collect the basic metadata of the collection.
    schema = CollectionSchema(exclude=exclude_attrs)
    collection_data = schema.dump(collection)

    # If not excluded, include all records the collection contains as "records" by
    # reusing the record export functionality.
    if not export_filter.get("records", False):
        collection_data["records"] = []

        records = get_linked_resources(Record, collection.records, user=user).order_by(
            Record.last_modified.desc()
        )
        for record in records:
            record_data = get_record_dict_data(record, export_filter, user)
            collection_data["records"].append(record_data)

    json_data = json.dumps(
        collection_data, ensure_ascii=False, indent=2, sort_keys=True
    )
    return BytesIO(json_data.encode())


def get_qr_data(collection):
    """Export a collection as a QR code in PNG format.

    See :func:`get_export_data` for an explanation of the parameters and return value.
    """
    image = qrcode.make(url_for("collections.view_collection", id=collection.id))

    image_data = BytesIO()
    image.save(image_data, format="PNG")
    image_data.seek(0)

    return image_data


def get_ro_crate_data(collection, export_filter, user):
    """Export a collection as a RO-Crate.

    See :func:`get_export_data` for an explanation of the parameters and return value.
    """

    # Check if records should be excluded, which only leaves us with the basic metadata
    # in the RO-Crate.
    if export_filter.get("records", False):
        records = []
    else:
        records = get_linked_resources(Record, collection.records, user=user).order_by(
            Record.last_modified.desc()
        )

    ro_crate = RecordROCrate(
        records, collection.identifier, export_filter=export_filter, user=user
    )

    if export_filter.get("metadata_only", False):
        return BytesIO(ro_crate.dump_metadata().encode())

    return ro_crate


def get_export_data(collection, export_type, export_filter=None, user=None):
    """Export a collection in a given format.

    :param collection: The collection to export.
    :param export_type: The export type, one of ``"json"``, ``"qr"`` or ``"ro-crate"``.
    :param export_filter: (optional) A dictionary specifying various filters to exclude
        certain information from the returned export data, depending on the export type.
        Only usable in combination with the ``"json"`` and ``"ro-crate"`` export types.

        **Example:**

        .. code-block:: python3

            {
                # Whether user information about the creator of the collection or any
                # linked resource should be excluded.
                "user": False,
                # Whether to exclude information about records that are part of the
                # collection.
                "records": False,
                # When record information is not excluded, whether to exclude all
                # (True), outgoing ("out") or incoming ("in") links of records with
                # other records.
                "links": False,
                # Whether to return only the metadata file of an exported RO-Crate.
                "metadata_only": False,
            }

    :param user: (optional) The user to check for various access permissions when
        generating the export data. Defaults to the current user.
    :return: The exported collection data as an in-memory byte stream or ``None`` if an
        unknown export type was given. Note that for the ``ro-crate`` export type, the
        returned data is an iterable producing the actual data on the fly instead,
        unless only the metadata file is exported by specifying the corresponding export
        filter.
    """
    export_filter = export_filter if export_filter is not None else {}
    user = user if user is not None else current_user

    if export_type == "json":
        return get_json_data(collection, export_filter, user)

    if export_type == "qr":
        return get_qr_data(collection)

    if export_type == "ro-crate":
        return get_ro_crate_data(collection, export_filter, user)

    return None
