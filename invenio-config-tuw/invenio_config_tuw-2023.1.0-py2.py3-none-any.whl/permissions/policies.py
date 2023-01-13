# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_rdm_records.services import RDMRecordPermissionPolicy
from invenio_rdm_records.services.generators import (
    CommunityAction,
    IfRestricted,
    RecordOwners,
    SubmissionReviewer,
)
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    SystemProcess,
)
from invenio_requests.services.permissions import (
    PermissionPolicy as RequestsPermissionPolicy,
)

from .generators import (
    DisableIfReadOnly,
    TrustedPublisherRecordOwners,
    TrustedRecordOwners,
    TrustedUsers,
    secret_links,
)

# TODO override permissions for vocabularies and users-resources


class TUWRecordPermissionPolicy(RDMRecordPermissionPolicy):
    """Record permission policy of TU Wien."""

    # current state: invenio-rdm-records v0.39.1
    #
    # note: edit := create a draft from a record (i.e. putting it in edit mode),
    #               which does not imply the permission to save the edits
    # note: can_search_* is the permission for the search in general, the records
    #       (drafts) will be filtered as per can_read_* permissions
    #
    # fmt: off
    #
    # high-level permissions: not used directly (only collections for reuse);
    #                         and get more permissive from top to bottom
    # most keys were taken from invenio-rdm-records and tweaked
    # also, we disable write operations if the system is in read-only mode
    # some explanations:
    # > can_basics:       gives all rights to the system, and admins
    # > can_access_draft: slightly less strict version of can_manage,
    #                     e.g. to not break user-records search
    # > can_curate:       people with curation rights (e.g. community curators)
    # > can_review:       slightly expanded from 'can_curate', can edit drafts
    can_basics             = [SystemProcess()]
    can_manage             = can_basics       + [TrustedRecordOwners(), CommunityAction("curate")]                      # noqa
    can_access_draft       = can_manage       + [RecordOwners(), SubmissionReviewer()]                                  # noqa
    can_curate             = can_manage                                                      + secret_links["edit"]     # noqa
    can_review             = can_curate       + [SubmissionReviewer()]                                                  # noqa
    can_preview            = can_access_draft                                                + secret_links["preview"]  # noqa
    can_view               = can_access_draft + [CommunityAction("view")]                    + secret_links["view"]     # noqa
    can_authenticated      = can_basics       + [AuthenticatedUser()]                                                   # noqa
    can_all                = can_basics       + [AnyUser()]                                                             # noqa

    # records
    can_search             = can_all                                                                                    # noqa
    can_read               = [IfRestricted("record", then_=can_view, else_=can_all)] + secret_links["view_record"]      # noqa
    can_read_files         = [IfRestricted("files", then_=can_view, else_=can_all) ] + secret_links["view_files"]       # noqa
    can_create             = can_basics + [TrustedUsers(), DisableIfReadOnly()]                                         # noqa

    # drafts
    can_search_drafts      = can_authenticated                                                                          # noqa
    can_read_draft         = can_preview                                                                                # noqa
    can_draft_read_files   = can_preview                                                                                # noqa
    can_update_draft       = can_review + [DisableIfReadOnly()]                                                         # noqa
    can_draft_create_files = can_review + [DisableIfReadOnly()]                                                         # noqa
    can_draft_update_files = can_review + [DisableIfReadOnly()]                                                         # noqa
    can_draft_delete_files = can_review + [DisableIfReadOnly()]                                                         # noqa

    # PIDs
    can_pid_create         = can_review + [DisableIfReadOnly()]                                                         # noqa
    can_pid_register       = can_review + [DisableIfReadOnly()]                                                         # noqa
    can_pid_update         = can_review + [DisableIfReadOnly()]                                                         # noqa
    can_pid_discard        = can_review + [DisableIfReadOnly()]                                                         # noqa
    can_pid_delete         = can_review + [DisableIfReadOnly()]                                                         # noqa

    # actions
    # > can_edit: RecordOwners is needed to not break the 'edit' button
    #             on the dashboard (UX)
    # > can_publish: TODO (trusted) submission reviewers should be allowed too
    can_edit               = can_curate + [RecordOwners(), DisableIfReadOnly()]                                         # noqa
    can_delete_draft       = can_curate + [DisableIfReadOnly()]                                                         # noqa
    can_new_version        = can_curate + [DisableIfReadOnly()]                                                         # noqa
    can_lift_embargo       = can_manage + [DisableIfReadOnly()]                                                         # noqa
    can_publish            = can_basics + [TrustedPublisherRecordOwners(), DisableIfReadOnly()]                         # noqa

    # disabled (record management in InvenioRDM goes through drafts)
    can_update             = [Disable()]                                                                                # noqa
    can_delete             = [Disable()]                                                                                # noqa
    can_create_files       = [Disable()]                                                                                # noqa
    can_update_files       = [Disable()]                                                                                # noqa
    can_delete_files       = [Disable()]                                                                                # noqa
    # fmt: on


class TUWRequestsPermissionPolicy(RequestsPermissionPolicy):
    """Requests permission policy of TU Wien."""

    # disable write operations if the system is in read-only mode
    #
    # current state: invenio-requests v0.5.5

    # fmt: off
    can_create         = RequestsPermissionPolicy.can_create         + [DisableIfReadOnly()]  # noqa
    can_update         = RequestsPermissionPolicy.can_update         + [DisableIfReadOnly()]  # noqa
    can_delete         = RequestsPermissionPolicy.can_delete         + [DisableIfReadOnly()]  # noqa
    can_action_submit  = RequestsPermissionPolicy.can_action_submit  + [DisableIfReadOnly()]  # noqa
    can_action_cancel  = RequestsPermissionPolicy.can_action_cancel  + [DisableIfReadOnly()]  # noqa
    can_action_expire  = RequestsPermissionPolicy.can_action_expire  + [DisableIfReadOnly()]  # noqa
    can_action_accept  = RequestsPermissionPolicy.can_action_accept  + [DisableIfReadOnly()]  # noqa
    can_action_decline = RequestsPermissionPolicy.can_action_decline + [DisableIfReadOnly()]  # noqa
    can_create_comment = RequestsPermissionPolicy.can_read           + [DisableIfReadOnly()]  # noqa  # TODO s/can_read/can_create_comment for invenio-requests > 0.5.5
    can_update_comment = RequestsPermissionPolicy.can_update_comment + [DisableIfReadOnly()]  # noqa
    can_delete_comment = RequestsPermissionPolicy.can_delete_comment + [DisableIfReadOnly()]  # noqa
    # fmt: on


class TUWCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """Communities permission policy of TU Wien."""

    # for now, we want to restrict the creation of communities to admins
    # and disable write operations if the system is in read-only mode
    #
    # current state: invenio-communities v3.1.0
    #
    # TODO: discuss who should have permissions to create communities
    #       -> new role?
    can_create = [SystemProcess(), DisableIfReadOnly()]

    # fmt: off
    can_update              = CommunityPermissionPolicy.can_update              + [DisableIfReadOnly()]  # noqa
    can_delete              = CommunityPermissionPolicy.can_delete              + [DisableIfReadOnly()]  # noqa
    can_rename              = CommunityPermissionPolicy.can_rename              + [DisableIfReadOnly()]  # noqa
    can_submit_record       = CommunityPermissionPolicy.can_submit_record       + [DisableIfReadOnly()]  # noqa
    can_members_add         = CommunityPermissionPolicy.can_members_add         + [DisableIfReadOnly()]  # noqa
    can_members_invite      = CommunityPermissionPolicy.can_members_invite      + [DisableIfReadOnly()]  # noqa
    can_members_manage      = CommunityPermissionPolicy.can_members_manage      + [DisableIfReadOnly()]  # noqa
    can_members_bulk_update = CommunityPermissionPolicy.can_members_bulk_update + [DisableIfReadOnly()]  # noqa
    can_members_bulk_delete = CommunityPermissionPolicy.can_members_bulk_delete + [DisableIfReadOnly()]  # noqa
    can_members_update      = CommunityPermissionPolicy.can_members_update      + [DisableIfReadOnly()]  # noqa
    can_members_delete      = CommunityPermissionPolicy.can_members_delete      + [DisableIfReadOnly()]  # noqa
    can_invite_owners       = CommunityPermissionPolicy.can_invite_owners       + [DisableIfReadOnly()]  # noqa
    can_featured_create     = CommunityPermissionPolicy.can_featured_create     + [DisableIfReadOnly()]  # noqa
    can_featured_update     = CommunityPermissionPolicy.can_featured_update     + [DisableIfReadOnly()]  # noqa
    can_featured_delete     = CommunityPermissionPolicy.can_featured_delete     + [DisableIfReadOnly()]  # noqa
    # fmt: on
