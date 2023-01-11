## $Id: workflow.py 15450 2019-06-04 07:01:04Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Workflow for students.
"""
import grok
from datetime import datetime
from zope.component import getUtility
from hurry.workflow.workflow import Transition, WorkflowState, NullCondition
from hurry.workflow.interfaces import IWorkflowState, IWorkflowTransitionEvent
from waeup.kofa.interfaces import (
    IObjectHistory, IKofaWorkflowInfo, IKofaUtils,
    CREATED, ADMITTED, CLEARANCE, REQUESTED, CLEARED, PAID, RETURNING,
    REGISTERED, VALIDATED, GRADUATED, TRANSREQ, TRANSVAL, TRANSREL,
    IExtFileStore)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.workflow import KofaWorkflow, KofaWorkflowInfo
from waeup.kofa.students.interfaces import IStudent, IStudentsUtils
from waeup.kofa.utils.helpers import get_current_principal


IMPORTABLE_STATES = (ADMITTED, CLEARANCE, REQUESTED, CLEARED, PAID, RETURNING,
    REGISTERED, VALIDATED, GRADUATED)

FORBIDDEN_POSTGRAD_STATES = (RETURNING, REGISTERED, VALIDATED)

ALUMNI_STATES = (GRADUATED, TRANSREQ, TRANSVAL, TRANSREL)

REGISTRATION_TRANSITIONS = (
    Transition(
        transition_id = 'create',
        title = _('Create student'),
        source = None,
        condition = NullCondition,
        msg = _('Record created'),
        destination = CREATED),

    Transition(
        transition_id = 'admit',
        title = _('Admit student'),
        msg = _('Admitted'),
        source = CREATED,
        destination = ADMITTED),

    Transition(
        transition_id = 'reset1',
        title = _('Reset student'),
        msg = _('Reset to initial state'),
        source = ADMITTED,
        destination = CREATED),

    Transition(
        transition_id = 'start_clearance',
        title = _('Start clearance'),
        msg = _('Clearance started'),
        source = ADMITTED,
        destination = CLEARANCE),

    Transition(
        transition_id = 'reset2',
        title = _('Reset to admitted'),
        msg = _("Reset to 'admitted'"),
        source = CLEARANCE,
        destination = ADMITTED),

    Transition(
        transition_id = 'request_clearance',
        title = _('Request clearance'),
        msg = _('Clearance requested'),
        source = CLEARANCE,
        destination = REQUESTED),

    Transition(
        transition_id = 'reset3',
        title = _('Reset to clearance started'),
        msg = _("Reset to 'clearance started'"),
        source = REQUESTED,
        destination = CLEARANCE),

    Transition(
        transition_id = 'clear',
        title = _('Clear student'),
        msg = _('Cleared'),
        source = REQUESTED,
        destination = CLEARED),

    Transition(
        transition_id = 'reset4',
        title = _('Reset to clearance started'),
        msg = _("Reset to 'clearance started'"),
        source = CLEARED,
        destination = CLEARANCE),

    Transition(
        transition_id = 'pay_first_school_fee',
        title = _('Pay school fee'),
        msg = _('First school fee payment made'),
        source = CLEARED,
        destination = PAID),

    Transition(
        transition_id = 'approve_first_school_fee',
        title = _('Approve payment'),
        msg = _('First school fee payment approved'),
        source = CLEARED,
        destination = PAID),

    Transition(
        transition_id = 'reset5',
        title = _('Reset to cleared'),
        msg = _("Reset to 'cleared'"),
        source = PAID,
        destination = CLEARED),

    Transition(
        transition_id = 'pay_school_fee',
        title = _('Pay school fee'),
        msg = _('School fee payment made'),
        source = RETURNING,
        destination = PAID),

    Transition(
        transition_id = 'pay_pg_fee',
        title = _('Pay PG school fee'),
        msg = _('PG school fee payment made'),
        source = PAID,
        destination = PAID),

    Transition(
        transition_id = 'approve_school_fee',
        title = _('Approve school fee payment'),
        msg = _('School fee payment approved'),
        source = RETURNING,
        destination = PAID),

    Transition(
        transition_id = 'approve_pg_fee',
        title = _('Approve PG school fee payment'),
        msg = _('PG school fee payment approved'),
        source = PAID,
        destination = PAID),

    Transition(
        transition_id = 'reset6',
        title = _('Reset to returning'),
        msg = _("Reset to 'returning'"),
        source = PAID,
        destination = RETURNING),

    Transition(
        transition_id = 'register_courses',
        title = _('Register courses'),
        msg = _('Courses registered'),
        source = PAID,
        destination = REGISTERED),

    Transition(
        transition_id = 'reset7',
        title = _('Unregister courses'),
        msg = _("Courses unregistered"),
        source = REGISTERED,
        destination = PAID),

    Transition(
        transition_id = 'validate_courses',
        title = _('Validate courses'),
        msg = _('Courses validated'),
        source = REGISTERED,
        destination = VALIDATED),

    Transition(
        transition_id = 'bypass_validation',
        title = _('Return and bypass validation'),
        msg = _("Course validation bypassed"),
        source = REGISTERED,
        destination = RETURNING),

    Transition(
        transition_id = 'reset8',
        title = _('Reset to school fee paid'),
        msg = _("Reset to 'school fee paid'"),
        source = VALIDATED,
        destination = PAID),

    Transition(
        transition_id = 'return',
        title = _('Return'),
        msg = _("Returned"),
        source = VALIDATED,
        destination = RETURNING),

    Transition(
        transition_id = 'reset9',
        title = _('Reset to courses validated'),
        msg = _("Reset to 'courses validated'"),
        source = RETURNING,
        destination = VALIDATED),

    # There is no transition to graduated.

    Transition(
        transition_id = 'request_transcript',
        title = _('Request transript'),
        msg = _("Transcript requested"),
        source = GRADUATED,
        destination = TRANSREQ),

    Transition(
        transition_id = 'reset10',
        title = _('Reject transcript request'),
        msg = _("Transcript request rejected"),
        source = TRANSREQ,
        destination = GRADUATED),

    Transition(
        transition_id = 'validate_transcript',
        title = _('Validate transcript'),
        msg = _("Transcript validated"),
        source = TRANSREQ,
        destination = TRANSVAL),

    Transition(
        transition_id = 'release_transcript',
        title = _('Release transcript'),
        msg = _("Transcript released"),
        source = TRANSVAL,
        destination = TRANSREL),

    Transition(
        transition_id = 'reset11',
        title = _('Reset to graduated'),
        msg = _("Transcript process reset"),
        source = TRANSREL,
        destination = GRADUATED),
    )


IMPORTABLE_TRANSITIONS = [i.transition_id for i in REGISTRATION_TRANSITIONS]

FORBIDDEN_POSTGRAD_TRANS = ['reset6', 'register_courses']

registration_workflow = KofaWorkflow(REGISTRATION_TRANSITIONS)

class RegistrationWorkflowState(WorkflowState, grok.Adapter):
    """An adapter to adapt Student objects to workflow states.
    """
    grok.context(IStudent)
    grok.provides(IWorkflowState)

    state_key = 'wf.registration.state'
    state_id = 'wf.registration.id'

class RegistrationWorkflowInfo(KofaWorkflowInfo, grok.Adapter):
    """Adapter to adapt Student objects to workflow info objects.
    """
    grok.context(IStudent)
    grok.provides(IKofaWorkflowInfo)

    def __init__(self, context):
        self.context = context
        self.wf = registration_workflow

@grok.subscribe(IStudent, IWorkflowTransitionEvent)
def handle_student_transition_event(obj, event):
    """Append message to student history and log file when transition happened.

    Lock and unlock clearance form.
    Trigger actions after school fee payment.
    """

    msg = event.transition.user_data['msg']
    history = IObjectHistory(obj)
    history.addMessage(msg)
    # School fee payment of returning students triggers the change of
    # current session, current level, and current verdict
    if event.transition.transition_id in (
        'pay_school_fee', 'approve_school_fee'):
        getUtility(IStudentsUtils).setReturningData(obj)
    elif event.transition.transition_id in (
        'pay_pg_fee', 'approve_pg_fee'):
        new_session = obj['studycourse'].current_session + 1
        obj['studycourse'].current_session = new_session
    elif event.transition.transition_id == 'validate_courses':
        current_level = obj['studycourse'].current_level
        level_object = obj['studycourse'].get(str(current_level), None)
        if level_object is not None:
            user = get_current_principal()
            if user is None:
                usertitle = 'system'
            else:
                usertitle = getattr(user, 'public_name', None)
                if not usertitle:
                    usertitle = user.title
            level_object.validated_by = usertitle
            level_object.validation_date = datetime.utcnow()
    elif event.transition.transition_id == 'clear':
        obj.officer_comment = None
    elif event.transition.transition_id == 'reset8':
        current_level = obj['studycourse'].current_level
        level_object = obj['studycourse'].get(str(current_level), None)
        if level_object is not None:
            level_object.validated_by = None
            level_object.validation_date = None
    elif event.transition.transition_id == 'reset11':
        transcript_file = getUtility(IExtFileStore).getFileByContext(
            obj, attr='final_transcript')
        if transcript_file:
            getUtility(IExtFileStore).deleteFileByContext(
                obj, attr='final_transcript')
        obj['studycourse'].transcript_comment = None
        obj['studycourse'].transcript_signees = None
    # In some tests we don't have a students container
    try:
        students_container = grok.getSite()['students']
        students_container.logger.info('%s - %s' % (obj.student_id,msg))
    except (TypeError, AttributeError):
        pass
    return
