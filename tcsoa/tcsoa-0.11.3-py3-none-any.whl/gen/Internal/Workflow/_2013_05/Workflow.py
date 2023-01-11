from __future__ import annotations

from enum import Enum


class SoaEPMAction(Enum):
    """
    SoaEPMAction
    """
    SOA_EPM_assign_action_2013_05 = 'SOA_EPM_assign_action_2013_05'
    SOA_EPM_start_action_2013_05 = 'SOA_EPM_start_action_2013_05'
    SOA_EPM_remove_attachment_action_2013_05 = 'SOA_EPM_remove_attachment_action_2013_05'
    SOA_EPM_approve_action_2013_05 = 'SOA_EPM_approve_action_2013_05'
    SOA_EPM_reject_action_2013_05 = 'SOA_EPM_reject_action_2013_05'
    SOA_EPM_promote_action_2013_05 = 'SOA_EPM_promote_action_2013_05'
    SOA_EPM_demote_action_2013_05 = 'SOA_EPM_demote_action_2013_05'
    SOA_EPM_refuse_action_2013_05 = 'SOA_EPM_refuse_action_2013_05'
    SOA_EPM_assign_approver_action_2013_05 = 'SOA_EPM_assign_approver_action_2013_05'
    SOA_EPM_notify_action_2013_05 = 'SOA_EPM_notify_action_2013_05'
    SOA_EPM_no_action_2013_05 = 'SOA_EPM_no_action_2013_05'
    SOA_EPM_fail_action_2013_05 = 'SOA_EPM_fail_action_2013_05'
    SOA_EPM_complete_action_2013_05 = 'SOA_EPM_complete_action_2013_05'
    SOA_EPM_skip_action_2013_05 = 'SOA_EPM_skip_action_2013_05'
    SOA_EPM_suspend_action_2013_05 = 'SOA_EPM_suspend_action_2013_05'
    SOA_EPM_resume_action_2013_05 = 'SOA_EPM_resume_action_2013_05'
    SOA_EPM_undo_action_2013_05 = 'SOA_EPM_undo_action_2013_05'
    SOA_EPM_abort_action_2013_05 = 'SOA_EPM_abort_action_2013_05'
    SOA_EPM_perform_action_2013_05 = 'SOA_EPM_perform_action_2013_05'
    SOA_EPM_add_attachment_action_2013_05 = 'SOA_EPM_add_attachment_action_2013_05'


class SoaEPMSupportingValues(Enum):
    """
    SoaEPMSupportingValues
    """
    SOA_EPM_no_decision_2013_05 = 'SOA_EPM_no_decision_2013_05'
    SOA_EPM_approve_2013_05 = 'SOA_EPM_approve_2013_05'
    SOA_EPM_reject_2013_05 = 'SOA_EPM_reject_2013_05'
    SOA_EPM_unset_2013_05 = 'SOA_EPM_unset_2013_05'
    SOA_EPM_completed_2013_05 = 'SOA_EPM_completed_2013_05'
    SOA_EPM_unable_to_complete_2013_05 = 'SOA_EPM_unable_to_complete_2013_05'
    SOA_EPM_true_2013_05 = 'SOA_EPM_true_2013_05'
    SOA_EPM_false_2013_05 = 'SOA_EPM_false_2013_05'
    SOA_EPM_no_error_2013_05 = 'SOA_EPM_no_error_2013_05'
