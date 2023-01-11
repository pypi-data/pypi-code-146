## $Id: workflow.py 12438 2015-01-11 08:27:37Z henrik $
##
## Copyright (C) 2014 Uli Fouquet & Henrik Bettermann
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
"""Workflow for documents.
"""

import grok
from zope.component import getUtility
from hurry.workflow.workflow import Transition, WorkflowState, NullCondition
from hurry.workflow.interfaces import (
    IWorkflowState, IWorkflowTransitionEvent, InvalidTransitionError)
from waeup.kofa.interfaces import (
    IObjectHistory, IKofaWorkflowInfo,
    SimpleKofaVocabulary)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.workflow import KofaWorkflow, KofaWorkflowInfo
from waeup.kofa.documents.interfaces import IPublicDocument

CREATED = 'created'
PUBLISHED = 'published'

PUBLISHING_TRANSITIONS = (
    Transition(
        transition_id = 'create',
        title = _('Create document'),
        source = None,
        condition = NullCondition,
        msg = _('Document created'),
        destination = CREATED),

    Transition(
        transition_id = 'publish',
        title = _('Publish document'),
        source = CREATED,
        condition = NullCondition,
        msg = _('Document published'),
        destination = PUBLISHED),

    Transition(
        transition_id = 'retract',
        title = _('Retract documet'),
        source = PUBLISHED,
        condition = NullCondition,
        msg = _('Document retracted'),
        destination = CREATED),
    )

publishing_workflow = KofaWorkflow(PUBLISHING_TRANSITIONS)

class PublishingWorkflowState(WorkflowState, grok.Adapter):
    """An adapter to adapt Document objects to workflow states.
    """
    grok.context(IPublicDocument)
    grok.provides(IWorkflowState)

    state_key = 'wf.publishing.state'
    state_id = 'wf.publishing.id'


class PublishingWorkflowInfo(KofaWorkflowInfo, grok.Adapter):
    """Adapter to adapt CustomerDocument objects to workflow info objects.
    """
    grok.context(IPublicDocument)
    grok.provides(IKofaWorkflowInfo)

    def __init__(self, context):
        self.context = context
        self.wf = publishing_workflow


@grok.subscribe(IPublicDocument, IWorkflowTransitionEvent)
def handle_public_document_transition_event(obj, event):
    """Append message to document history and log file.

    """
    msg = event.transition.user_data['msg']
    history = IObjectHistory(obj)
    history.addMessage(msg)
    try:
        grok.getSite().logger.info('%s - %s' % (obj.document_id, msg))
    except (TypeError, AttributeError):
        pass
    return