## $Id: refereereport.py 16243 2020-09-23 19:42:07Z henrik $
##
## Copyright (C) 2016 Uli Fouquet & Henrik Bettermann
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
import os
import grok
from datetime import datetime
from zope.component import getUtility, createObject, getAdapter
from zope.component.interfaces import IFactory
from zope.event import notify
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.interface import implementedBy
from zope.schema.interfaces import RequiredMissing, ConstraintNotSatisfied
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.applicants.interfaces import IApplicantRefereeReport


class ApplicantRefereeReport(grok.Model):
    """This is referee report.
    """
    grok.implements(IApplicantRefereeReport)
    grok.provides(IApplicantRefereeReport)

    def __init__(self):
        super(ApplicantRefereeReport, self).__init__()
        self.r_id = None
        self.creation_date = datetime.utcnow()
        self.email = None
        return

ApplicantRefereeReport = attrs_to_fields(ApplicantRefereeReport)


class ApplicantRefereeReportFactory(grok.GlobalUtility):
    """A factory for applicant online payments.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.ApplicantRefereeReport')
    title = u"Create a new referee report.",
    description = u"This factory instantiates new referee report instances."

    def __call__(self, *args, **kw):
        return ApplicantRefereeReport()

    def getInterfaces(self):
        return implementedBy(ApplicantRefereeReport)