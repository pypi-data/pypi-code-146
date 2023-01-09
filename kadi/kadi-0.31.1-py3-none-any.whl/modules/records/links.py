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
from flask_babel import gettext as _
from flask_login import current_user

from .models import File
from .models import Record
from .models import RecordLink
from .models import RecordState
from .schemas import RecordRevisionSchema
from kadi.ext.db import db
from kadi.lib.conversion import truncate
from kadi.lib.db import update_object
from kadi.lib.exceptions import KadiPermissionError
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import has_permission
from kadi.lib.revisions.core import create_revision
from kadi.lib.revisions.models import Revision
from kadi.lib.revisions.schemas import ObjectRevisionSchema
from kadi.lib.web import url_for
from kadi.plugins.utils import signal_resource_change


def _trigger_record_revisions(record_from, record_to, user):
    record_from_revision_created = create_revision(record_from, user=user)
    record_to_revision_created = create_revision(record_to, user=user)

    db.session.commit()

    if record_from_revision_created:
        signal_resource_change(record_from, user=user)

    if record_to_revision_created:
        signal_resource_change(record_to, user=user)


def create_record_link(*, name, record_from, record_to, creator=None, term=None):
    """Create a new record link.

    Note that this function may issue a database commit.

    :param name: See :attr:`.RecordLink.name`.
    :param record_from: The record that is being linked from.
    :param record_to: The record that is being linked to.
    :param creator: (optional) The creator of the record link. Defaults to the current
        user.
    :param term: (optional) See :attr:`.RecordLink.term`.
    :return: The created record link.
    :raises KadiPermissionError: If the creator does not have the necessary permissions.
    :raises ValueError: When trying to link a record with itself or the link already
        exists.
    """
    creator = creator if creator is not None else current_user

    if not has_permission(
        creator, "link", "record", record_from.id
    ) or not has_permission(creator, "link", "record", record_to.id):
        raise KadiPermissionError("No permission to link records.")

    if record_from == record_to:
        raise ValueError("Cannot link record with itself.")

    previous_link = (
        RecordLink.query.filter_by(
            name=name, record_from_id=record_from.id, record_to_id=record_to.id
        )
        .with_entities(RecordLink.id)
        .first()
    )

    # Disallow duplicate links. Note that this constraint is not enforced on the
    # database level, which is why it is checked here instead.
    if previous_link is not None:
        raise ValueError(_("Link already exists."))

    record_link = RecordLink.create(
        creator=creator,
        name=name,
        record_from=record_from,
        record_to=record_to,
        term=term,
    )

    _trigger_record_revisions(record_from, record_to, creator)

    return record_link


def update_record_link(record_link, user=None, **kwargs):
    r"""Update an existing record link.

    Note that this function may issue a database commit.

    :param record_link: The record link to upate.
    :param user: (optional) The user performing the update operation. Defaults to the
        current user.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    :raises KadiPermissionError: If the user performing the operation does not have the
        necessary permissions.
    :raises ValueError: When the link already exists.
    """
    user = user if user is not None else current_user

    if not has_permission(
        user, "link", "record", record_link.record_from_id
    ) or not has_permission(user, "link", "record", record_link.record_to_id):
        raise KadiPermissionError("No permission to update record link.")

    if "name" in kwargs:
        previous_link = (
            RecordLink.query.filter_by(
                name=kwargs["name"],
                record_from_id=record_link.record_from_id,
                record_to_id=record_link.record_to_id,
            )
            .with_entities(RecordLink.id)
            .first()
        )

        # Disallow duplicate links. Note that this constraint is not enforced on the
        # database level, which is why it is checked here instead.
        if previous_link is not None and previous_link.id != record_link.id:
            raise ValueError(_("Link already exists."))

    update_object(record_link, **kwargs)

    record_from = record_link.record_from
    record_to = record_link.record_to

    if db.session.is_modified(record_link):
        record_from.update_timestamp()
        record_to.update_timestamp()

    _trigger_record_revisions(record_from, record_to, user)


def remove_record_link(record_link, user=None):
    """Remove an existing record link.

    Note that this function may issue a database commit.

    :param record_link: The record link to remove.
    :param user: (optional) The user performing the remove operation. Defaults to the
        current user.
    :raises KadiPermissionError: If the user performing the operation does not have the
        necessary permissions.
    """
    user = user if user is not None else current_user

    if not has_permission(
        user, "link", "record", record_link.record_from_id
    ) or not has_permission(user, "link", "record", record_link.record_to_id):
        raise KadiPermissionError("No permission to remove record link.")

    record_from = record_link.record_from
    record_to = record_link.record_to

    # Remove the record link via the respective relationships to properly trigger all
    # related events.
    record_from.links_to.remove(record_link)
    record_to.linked_from.remove(record_link)

    _trigger_record_revisions(record_from, record_to, user)


def get_permitted_record_links(record_or_id, direction=None, user=None):
    """Convenience function to get all links of a record that a user can access.

    In this context having access to a record link means having read permission for each
    record the given record links to or is linked from.

    :param record_or_id: The record or ID of a record whose links should be obtained.
    :param direction: (optional) A direction to limit the returned record links to. One
        of ``"out"`` for outgoing links from the given record, or ``"in"`` for incoming
        links to the given record.
    :param user: (optional) The user to check for access permissions. Defaults to the
        current user.
    :return: The permitted record link objects as query.
    """
    user = user if user is not None else current_user
    record_id = record_or_id.id if isinstance(record_or_id, Record) else record_or_id

    record_ids_query = (
        get_permitted_objects(user, "read", "record")
        .filter(Record.state == RecordState.ACTIVE)
        .with_entities(Record.id)
    )

    # Records linked to from the given record.
    filter_to = db.and_(
        RecordLink.record_from_id == record_id,
        RecordLink.record_to_id.in_(record_ids_query),
    )
    # Records that link to the given record.
    filter_from = db.and_(
        RecordLink.record_to_id == record_id,
        RecordLink.record_from_id.in_(record_ids_query),
    )

    if direction == "out":
        filters = [filter_to]
    elif direction == "in":
        filters = [filter_from]
    else:
        filters = [filter_to, filter_from]

    return RecordLink.query.filter(db.or_(*filters))


def get_record_changes(record_link):
    """Get all changes of linked records since the given record link was created.

    The changes are based on the record and file revisions of the two linked records
    that were triggered after the record link was initially created.

    :param record_link: The record link representing the two linked records whose
        changes should be collected.
    :return: The changes of the linked records, consisting of the amount of new record
        and file revisions for each record. For the record revisions, the revision at
        the point of creation of the record link will also be included. The changes are
        returned as a dictionary in the following form:

        .. code-block:: python3

            {
                <record_from_id>: {
                    "record": {
                        "count": 0,
                        "revision": <revision>,
                    },
                    "files": {
                        "count": 0,
                    },
                },
                <record_to_id>: {
                    "record": {
                        "count": 1,
                        "revision": <revision>,
                    },
                    "files": {
                        "count": 2,
                    },
                },
            }
    """
    changes = {}

    for record in [record_link.record_from, record_link.record_to]:
        num_revisions = record.ordered_revisions.filter(
            Revision.timestamp > record_link.created_at
        ).count()

        nearest_revision = record.ordered_revisions.filter(
            Revision.timestamp < record_link.created_at
        ).first()

        # Due to the creation of record links also triggering new revisions, the child
        # of the nearest revision is actually the correct one. However, as record link
        # revisions were added later to the existing revisions, previous links might
        # appear together with other changes in a single revision, which needs to be
        # taken into account.
        if nearest_revision is not None and nearest_revision.child is not None:
            schema = ObjectRevisionSchema(RecordRevisionSchema, only=["diff"])
            diff = schema.dump(nearest_revision.child)["diff"]

            # Check if the diff only contains a single change related to creating a
            # single record link, in which case the child revision is taken instead.
            if len(diff) == 1:
                link_revision_key = None

                if "links_to" in diff:
                    link_revision_key = "links_to"
                elif "linked_from" in diff:
                    link_revision_key = "linked_from"

                if link_revision_key is not None:
                    link_revision = diff[link_revision_key]

                    if len(link_revision["new"]) - len(link_revision["prev"]) == 1:
                        nearest_revision = nearest_revision.child
                        # Also adjust the total number of revisions accordingly.
                        num_revisions -= 1

        changes[record.id] = {
            "record": {
                "count": num_revisions,
                "revision": nearest_revision,
            }
        }

        num_revisions = (
            File.revision_class.query.join(File)
            .join(Revision)
            .order_by(Revision.timestamp.desc())
            .filter(
                File.record_id == record.id, Revision.timestamp > record_link.created_at
            )
            .count()
        )

        changes[record.id]["files"] = {"count": num_revisions}

    return changes


def _append_node(nodes, record, depth):
    nodes.append(
        {
            "id": record.id,
            "identifier": truncate(record.identifier, 25),
            "identifier_full": record.identifier,
            "type": truncate(record.type, 25),
            "type_full": record.type,
            "url": url_for(
                "records.view_record",
                id=record.id,
                tab="links",
                visualize="true",
                depth=depth,
            ),
        }
    )


def _collect_link_data(
    record_id,
    link_direction,
    depth,
    nodes,
    links,
    processed_record_ids,
    added_record_ids,
    user,
):
    new_record_ids = set()
    link_indices = {}
    link_lengths = {}

    record_links_query = (
        get_permitted_record_links(record_id, direction=link_direction, user=user)
        .order_by(RecordLink.created_at.desc())
        .limit(100)
    )

    for record_link in record_links_query:
        # Skip all links involving records that were already checked for their links.
        if (
            record_link.record_from_id in processed_record_ids
            or record_link.record_to_id in processed_record_ids
        ):
            continue

        source = record_link.record_from
        target = record_link.record_to

        for record in [source, target]:
            new_record_ids.add(record.id)

            if record.id not in added_record_ids:
                _append_node(nodes, record, depth)
                added_record_ids.add(record.id)

        # The link indices are used to calculate the "curve" of a link when rendering
        # it. The index of a link is increased for each link that has the same source
        # and target, starting at 1.
        link_index = 1
        key = (source.id, target.id)

        if key in link_indices:
            link_indices[key] += 1
            link_index = link_indices[key]
        else:
            link_indices[key] = link_index

        # The link lengths are used to apply varying strengths of link forces to the
        # corresponding nodes based on the length of the (truncated) link name. Only the
        # largest length between each source and target record is taken, after all links
        # have been processed.
        link_name = truncate(record_link.name, 25)
        link_length = len(link_name)
        key = (
            (source.id, target.id) if source.id < target.id else (target.id, source.id)
        )

        if key in link_lengths:
            link_lengths[key] = max(link_length, link_lengths[key])
        else:
            link_lengths[key] = link_length

        links.append(
            {
                "source": source.id,
                "target": target.id,
                "name": link_name,
                "name_full": record_link.name,
                "link_index": link_index,
                "link_length": link_length,
                # Just take the outgoing record as a base for the link overview URL.
                "url": url_for(
                    "records.view_record_link",
                    record_id=record_link.record_from_id,
                    link_id=record_link.id,
                ),
            }
        )

    for link in links:
        key = (
            (link["source"], link["target"])
            if link["source"] < link["target"]
            else (link["target"], link["source"])
        )

        if key in link_lengths:
            link["link_length"] = link_lengths[key]

    processed_record_ids.add(record_id)
    return new_record_ids


def get_record_links_graph(record, depth=1, direction=None, user=None):
    """Get all links of a record for visualizing them in a graph.

    Used in conjunction with "D3.js" to visualize all returned nodes and links in a
    force directed graph.

    :param record: The record to start with.
    :param depth: (optional) The link depth.
    :param direction: (optional) A direction to limit the returned record links to. One
        of ``"out"`` for outgoing links from the start record, or ``"in"`` for incoming
        links to the start record.
    :param user: (optional) The user to check for access permissions regarding the
        linked records. Defaults to the current user.
    :return: A dictionary containing the record links (``"links"``) as well as all
        records involved in the links (``"nodes"``).
    """
    user = user if user is not None else current_user

    nodes = []
    links = []

    # Records to still check for their links.
    record_ids_to_process = {record.id}
    # Records already checked for their links.
    processed_record_ids = set()
    # Records already added to the node list.
    added_record_ids = set()

    # Add the start record itself to the nodes.
    _append_node(nodes, record, depth)
    added_record_ids.add(record.id)

    for _ in range(0, depth):
        # Newly added records in the last iteration that are not processed yet.
        new_record_ids = set()

        for record_id in record_ids_to_process:
            link_direction = None

            # Only specify the direction for the start record.
            if record_id == record.id:
                link_direction = direction

            new_record_ids |= _collect_link_data(
                record_id,
                link_direction,
                depth,
                nodes,
                links,
                processed_record_ids,
                added_record_ids,
                user,
            )

        record_ids_to_process = new_record_ids

    return {"nodes": nodes, "links": links}
