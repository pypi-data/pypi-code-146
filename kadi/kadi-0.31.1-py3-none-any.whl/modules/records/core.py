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

from .files import remove_file
from .files import remove_temporary_file
from .models import Record
from .models import RecordLink
from .models import RecordState
from .models import RecordVisibility
from .uploads import remove_upload
from kadi.ext.db import db
from kadi.lib.conversion import strip_markdown
from kadi.lib.licenses.models import License
from kadi.lib.resources.core import create_resource
from kadi.lib.resources.core import delete_resource
from kadi.lib.resources.core import purge_resource
from kadi.lib.resources.core import restore_resource
from kadi.lib.resources.core import update_resource
from kadi.lib.revisions.core import create_revision
from kadi.plugins.utils import signal_resource_change


def create_record(
    *,
    identifier,
    title,
    creator=None,
    type=None,
    description="",
    license=None,
    extras=None,
    visibility=RecordVisibility.PRIVATE,
    state=RecordState.ACTIVE,
    tags=None,
):
    """Create a new record.

    Uses :func:`kadi.lib.resources.core.create_resource`.

    :param identifier: See :attr:`.Record.identifier`.
    :param title: See :attr:`.Record.title`.
    :param creator: (optional) The creator of the record. Defaults to the current user.
    :param type: (optional) See :attr:`.Record.type`.
    :param description: (optional) See :attr:`.Record.description`.
    :param license: (optional) The name of the license to reference the record with. See
        also :class:`.License`.
    :param extras: (optional) See :attr:`.Record.extras`.
    :param visibility: (optional) See :attr:`.Record.visibility`.
    :param state: (optional) See :attr:`.Record.state`.
    :param tags: (optional) A list of tag names to tag the record with. See also
        :class:`.Tag`.
    :return: See :func:`kadi.lib.resources.core.create_resource`.
    """
    creator = creator if creator is not None else current_user
    license = License.query.filter_by(name=license).first()

    return create_resource(
        Record,
        creator=creator,
        identifier=identifier,
        title=title,
        type=type,
        description=description,
        plain_description=strip_markdown(description),
        license=license,
        extras=extras,
        visibility=visibility,
        state=state,
        tags=tags,
    )


def update_record(record, tags=None, user=None, **kwargs):
    r"""Update an existing record.

    Uses :func:`kadi.lib.resources.core.update_resource`.

    :param record: The record to update.
    :param tags: (optional) A list of tag names to tag the record with. See also
        :class:`.Tag`.
    :param user: (optional) The user who triggered the update. Defaults to the current
        user.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.resources.update_resource`.
    :return: See :func:`kadi.lib.resources.core.update_resource`.
    """
    user = user if user is not None else current_user

    if "description" in kwargs:
        kwargs["plain_description"] = strip_markdown(kwargs["description"])

    if kwargs.get("license") is not None:
        kwargs["license"] = License.query.filter_by(name=kwargs["license"]).first()

    return update_resource(record, user=user, tags=tags, **kwargs)


def delete_record(record, user=None):
    """Delete an existing record.

    Uses :func:`kadi.lib.resources.core.delete_resource`.

    :param record: The record to delete.
    :param user: (optional) The user who triggered the deletion. Defaults to the current
        user.
    """
    user = user if user is not None else current_user
    delete_resource(record, user=user)


def restore_record(record, user=None):
    """Restore a deleted record.

    Uses :func:`kadi.lib.resources.core.restore_resource`.

    :param record: The record to restore.
    :param user: (optional) The user who triggered the restoration. Defaults to the
        current user.
    """
    user = user if user is not None else current_user
    restore_resource(record, user=user)


def purge_record(record):
    """Purge an existing record.

    This will also remove all files, uploads and temporary files of the record.

    Uses :func:`kadi.lib.resources.core.purge_resource`.

    :param record: The record to purge.
    """

    # Save some references for later use before actually deleting the record, including
    # all record links the record is part of.
    record_id = record.id
    record_creator = record.creator
    record_link_attrs = [RecordLink.record_from_id, RecordLink.record_to_id]

    record_links = (
        record.links_to.with_entities(*record_link_attrs)
        .union(record.linked_from.with_entities(*record_link_attrs))
        .all()
    )

    # Perform the actual deletions.
    for file in record.files:
        remove_file(file)

    for upload in record.uploads:
        remove_upload(upload)

    for temporary_file in record.temporary_files:
        remove_temporary_file(temporary_file)

    purge_resource(record)

    # Since record links are also tracked as part of the revisions, deleting the record
    # needs to trigger a new revision in all of its linked records. Since records can
    # currently only be purged by their creator, we simply take the creator of the
    # purged record as the user for the revisions, even if the initial deletion may have
    # technically been performed by someone else.
    for record_link in record_links:
        if record_link.record_from_id == record_id:
            linked_record_id = record_link.record_to_id
        else:
            linked_record_id = record_link.record_from_id

        linked_record = Record.query.filter(Record.id == linked_record_id).first()

        # Note that the checks in this function already ensure that only a single
        # revision is created, even if a record is linked multiple times.
        revision_created = create_revision(linked_record, user=record_creator)
        db.session.commit()

        if revision_created:
            signal_resource_change(linked_record, user=record_creator)
