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
"""Workflow components of general use.
"""
import grok
from hurry.workflow.interfaces import IWorkflow, MANUAL, InvalidTransitionError
from hurry.workflow.workflow import (
    Transition, Workflow, WorkflowVersions, WorkflowInfo,
    NullCondition, nullCheckPermission)
from zope.security.interfaces import NoInteraction
from zope.security.management import getInteraction
from waeup.kofa.interfaces import IKofaWorkflowInfo

class KofaWorkflow(Workflow):
    """A :mod:`hurry.workflow` workflow with more appropriate error
       messages.
    """
    grok.provides(IWorkflow)

    def getTransition(self, source, transition_id):
        transition = self._id_transitions[transition_id]
        if transition.source != source:
            raise InvalidTransitionError(
                "Transition '%s' requires '%s' as source state (is: '%s')" % (
                    transition_id, transition.source, source))
        return transition


class WorkflowNullVersions(WorkflowVersions):
    """A workflow versions manager that does not handle versions.

    Sounds odd, but the default implementation of
    :class:`hurry.workflow.workflow.WorkflowVersions` is a base
    implementation that raises :exc:`NotImplemented` exceptions for
    most of the methods defined below.

    If we want to register a versionless workflow, an utility
    implementing IWorkflowVersions is looked up nevertheless by
    WorkflowInfo and WorkflowState components so we **have** to
    provide workflow versions, even if we do not support versioned
    workflows.

    This implementation returns empty result sets for any requests,
    but does not raise :exc:`NotImplemented`.
    """
    def getVersions(self, state, id):
        return []

    def getVersionsWithAutomaticTransitions(self):
        return []

    def hasVersion(self, id, state):
        return False

    def hasVersionId(self, id):
        return False

class KofaWorkflowInfo(WorkflowInfo):
    """A workflow info that provides a convenience transition getter.
    """

    grok.provides(IKofaWorkflowInfo)

    def getManualTransitions(self):
        """Get allowed manual transitions.

        Get a sorted list of tuples containing the `transition_id` and
        `title` of each allowed transition.
        """
        try:
            checkPermission = getInteraction().checkPermission
        except NoInteraction:
            checkPermission = nullCheckPermission
        return [(transition.transition_id, transition.title)
                for transition in sorted(self._getTransitions(MANUAL))
                if transition.condition(self, self.context) and
                checkPermission(transition.permission, self.context)]
