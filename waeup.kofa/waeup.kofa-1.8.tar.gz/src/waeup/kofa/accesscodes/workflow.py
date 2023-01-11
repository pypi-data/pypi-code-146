## $Id: workflow.py 7819 2012-03-08 22:28:46Z henrik $
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
"""
Workflows for access codes/pins.
"""
import grok
from zope.i18n import translate
from zope.component import getUtility
from datetime import datetime
from hurry.workflow.workflow import Transition, WorkflowState, NullCondition
from hurry.workflow.interfaces import IWorkflowState, IWorkflowTransitionEvent
from waeup.kofa.accesscodes.interfaces import IAccessCode
from waeup.kofa.interfaces import IObjectHistory, IKofaWorkflowInfo
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.workflow import KofaWorkflow, KofaWorkflowInfo

INITIALIZED = 'initialized'
USED = 'used'
DISABLED = 'disabled'

ac_states_dict = {
    INITIALIZED: _('initialized'),
    USED: _('used'),
    DISABLED: _('disabled'),
    }

def invalidate_action(wf, context):
    """Side actions taken when an access code is invalidated.
    """
    batch = getattr(context, '__parent__', None)
    if batch is None:
        return
    batch.used_num += 1
    return

def disable_used_action(wf, context):
    """Side actions taken when a used access code is disabled.
    """
    batch = getattr(context, '__parent__', None)
    if batch is None:
        return
    batch.used_num -= 1
    batch.disabled_num += 1

def disable_unused_action(wf, context):
    """Side actions taken when an unused access code is invalidated.
    """
    batch = getattr(context, '__parent__', None)
    if batch is None:
        return
    batch.disabled_num += 1
    return

def reenable_action(wf, context):
    """Side actions taken when an access code is reenabled.
    """
    batch = getattr(context, '__parent__', None)
    if batch is None:
        return
    batch.disabled_num -= 1
    return

ACCESSCODE_TRANSITIONS = (
    Transition(
        transition_id = 'init',
        title = _('Initialize PIN'),
        source = None,
        condition = NullCondition,
        destination = INITIALIZED),

    Transition(
        transition_id = 'use',
        title = _('Use PIN'),
        source = INITIALIZED,
        destination = USED,
        action = invalidate_action),

    Transition(
        transition_id = 'disable_unused',
        title = _('Disable unused PIN'),
        source = INITIALIZED,
        destination = DISABLED,
        action = disable_unused_action),

    Transition(
        transition_id = 'disable_used',
        title = _('Disable used PIN'),
        source = USED,
        destination = DISABLED,
        action = disable_used_action),

    Transition(
        transition_id = 'reenable',
        title = _('Reenable disabled PIN'),
        source = DISABLED,
        destination = INITIALIZED,
        action = reenable_action),
    )

accesscode_workflow = KofaWorkflow(ACCESSCODE_TRANSITIONS)

class AccessCodeWorkflowState(WorkflowState, grok.Adapter):
    grok.context(IAccessCode)
    grok.provides(IWorkflowState)

    state_key = 'wf.accesscode.state'
    state_id = 'wf.accesscode.id'

class AccessCodeWorkflowInfo(KofaWorkflowInfo, grok.Adapter):
    grok.context(IAccessCode)
    grok.provides(IKofaWorkflowInfo)

    def __init__(self, context):
        self.context = context
        self.wf = accesscode_workflow

@grok.subscribe(IAccessCode, IWorkflowTransitionEvent)
def handle_accesscode_transition_event(obj, event):
    # append message to history
    if event.comment is not None:
        msg = event.comment
    else:
        msg = ac_states_dict[event.destination]
    history = IObjectHistory(obj)
    history.addMessage(msg)
    return
