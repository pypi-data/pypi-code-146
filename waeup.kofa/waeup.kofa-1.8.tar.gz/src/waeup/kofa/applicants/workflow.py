## $Id: workflow.py 15875 2019-12-09 14:55:15Z henrik $
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
"""Workflow for applicants.
"""
import grok
from hurry.workflow.workflow import Transition, WorkflowState, NullCondition
from hurry.workflow.interfaces import IWorkflowState, IWorkflowTransitionEvent
from waeup.kofa.applicants.interfaces import IApplicantBaseData
from waeup.kofa.interfaces import IObjectHistory, IKofaWorkflowInfo, IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.workflow import KofaWorkflow, KofaWorkflowInfo

INITIALIZED = 'initialized'
STARTED = 'started'
PAID = 'paid'
SUBMITTED = 'submitted'
ADMITTED = 'admitted'
NOT_ADMITTED = 'not admitted'
CREATED = 'created'
PROCESSED = 'processed'


IMPORTABLE_STATES = (INITIALIZED, STARTED, PAID,
                     SUBMITTED, ADMITTED, NOT_ADMITTED, PROCESSED)

application_states_dict = {
    INITIALIZED: _('initialized'),
    STARTED: _('started'),
    PAID: _('paid'),
    SUBMITTED: _('submitted'),
    ADMITTED: _('admitted'),
    NOT_ADMITTED: _('not admitted'),
    CREATED: _('created'),
    PROCESSED: _('processed'),
    }

APPLICATION_TRANSITIONS = (
    Transition(
        transition_id = 'init',
        title = _('Initialize application'),
        source = None,
        condition = NullCondition,
        msg = _('Application initialized'),
        destination = INITIALIZED),

    Transition(
        transition_id = 'start',
        title = _('Start application'),
        msg = _('Application started'),
        source = INITIALIZED,
        destination = STARTED),

    Transition(
        transition_id = 'pay',
        title = _('Pay application fee'),
        msg = _('Payment made'),
        source = STARTED,
        destination = PAID),

    Transition(
        transition_id = 'approve',
        title = _('Approve payment'),
        msg = _('Payment approved'),
        source = STARTED,
        destination = PAID),

    Transition(
        transition_id = 'submit',
        title = _('Submit application'),
        msg = _('Application submitted'),
        source = PAID,
        destination = SUBMITTED),

    Transition(
        transition_id = 'admit',
        title = _('Admit applicant'),
        msg = _('Applicant admitted'),
        source = SUBMITTED,
        destination = ADMITTED),

    Transition(
        transition_id = 'refuse1',
        title = _('Refuse application'),
        msg = _('Application refused'),
        source = SUBMITTED,
        destination = NOT_ADMITTED),

    Transition(
        transition_id = 'process',
        title = _('Process application'),
        msg = _('Application processed'),
        source = SUBMITTED,
        destination = PROCESSED),

    Transition(
        transition_id = 'refuse2',
        title = _('Refuse application'),
        msg = _('Application refused'),
        source = ADMITTED,
        destination = NOT_ADMITTED),

    Transition(
        transition_id = 'create',
        title = _('Create student'),
        msg = _('Student record created'),
        source = ADMITTED,
        destination = CREATED),

    Transition(
        transition_id = 'reset1',
        title = _('Reset application to started'),
        msg = _('Application reset'),
        source = PAID,
        destination = STARTED),

    Transition(
        transition_id = 'reset2',
        title = _('Reset application to paid'),
        msg = _('Application reset to paid'),
        source = SUBMITTED,
        destination = PAID),

    Transition(
        transition_id = 'reset3',
        title = _('Reset application to started'),
        msg = _('Application reset'),
        source = SUBMITTED,
        destination = STARTED),

    Transition(
        transition_id = 'reset4',
        title = _('Reset application to started'),
        msg = _('Application reset'),
        source = ADMITTED,
        destination = STARTED),

    Transition(
        transition_id = 'reset5',
        title = _('Reset application to started'),
        msg = _('Application reset'),
        source = NOT_ADMITTED,
        destination = STARTED),

    Transition(
        transition_id = 'reset6',
        title = _('Reset application to submitted'),
        msg = _('Application reset'),
        source = PROCESSED,
        destination = SUBMITTED),

    )

application_workflow = KofaWorkflow(APPLICATION_TRANSITIONS)

class ApplicationWorkflowState(WorkflowState, grok.Adapter):
    """An adapter to adapt Applicant objects to workflow states.
    """
    grok.context(IApplicantBaseData)
    grok.provides(IWorkflowState)

    state_key = 'wf.application.state'
    state_id = 'wf.application.id'

class ApplicationWorkflowInfo(KofaWorkflowInfo, grok.Adapter):
    """Adapter to adapt Applicant objects to workflow info objects.
    """
    grok.context(IApplicantBaseData)
    grok.provides(IKofaWorkflowInfo)

    def __init__(self, context):
        self.context = context
        self.wf = application_workflow

@grok.subscribe(IApplicantBaseData, IWorkflowTransitionEvent)
def handle_applicant_transition_event(obj, event):
    """Append message to applicant history and lock form
    when transition happened.
    """
    msg = event.transition.user_data['msg']
    if event.transition.transition_id == 'create':
        msg += ' (%s)' % obj.student_id
        obj.locked = True
    if event.transition.transition_id == 'submit':
        obj.locked = True
    history = IObjectHistory(obj)
    history.addMessage(msg)
    # In some tests we don't have a an applicants root or a user
    try:
        applicants_root = grok.getSite()['applicants']
        applicants_root.logger.info('%s - %s' % (obj.applicant_id,msg))
    except (TypeError, AttributeError):
        pass
    return
