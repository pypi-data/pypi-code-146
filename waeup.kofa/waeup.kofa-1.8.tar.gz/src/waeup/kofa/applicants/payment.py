## $Id: payment.py 16527 2021-07-06 05:51:42Z henrik $
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
Application fee payment.
"""
import grok
import sys
from hurry.workflow.interfaces import (
    IWorkflowInfo, InvalidTransitionError)
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.payments import OnlinePayment
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.applicants.interfaces import IApplicantOnlinePayment
from waeup.kofa.applicants.workflow import PAID
from waeup.kofa.utils.helpers import attrs_to_fields

class ApplicantOnlinePayment(OnlinePayment):
    """This is an online payment.
    """
    grok.implements(IApplicantOnlinePayment)
    grok.provides(IApplicantOnlinePayment)

    def __init__(self):
        super(ApplicantOnlinePayment, self).__init__()
        return

    def doAfterApplicantPaymentApproval(self):
        """Process applicant after payment was approved.
        """
        if self.__parent__.state != PAID \
            and (self.p_category in ('application', 'transcript') \
                 or self.__parent__.special):
            wf_info = IWorkflowInfo(self.__parent__)
            try:
                wf_info.fireTransition('approve')
            except InvalidTransitionError:
                msg = log = 'Error: %s' % sys.exc_info()[1]
                return 'danger', msg, log
        log = 'approved: %s' % self.p_id
        msg = _('Payment approved')
        flashtype = 'success'
        return flashtype, msg, log

    def doAfterApplicantPayment(self):
        """Process applicant after payment was made.
        """
        if self.__parent__.state != PAID \
            and (self.p_category in ('application', 'transcript') \
                 or self.__parent__.special):
            wf_info = IWorkflowInfo(self.__parent__)
            try:
                wf_info.fireTransition('pay')
            except InvalidTransitionError:
                msg = log = 'Error: %s' % sys.exc_info()[1]
                return 'danger', msg, log
        log = 'successful payment: %s' % self.p_id
        msg = _('Payment successfully completed. Kindly submit application for processing.')
        flashtype = 'success'
        return flashtype, msg, log

    def approveApplicantPayment(self):
        """Approve payment and process applicant.
        """
        if self.p_state == 'paid':
            return 'warning', _('This ticket has already been paid.'), None
        self.approve()
        return self.doAfterApplicantPaymentApproval()

ApplicantOnlinePayment = attrs_to_fields(
    ApplicantOnlinePayment, omit=['display_item'])

class Payer(grok.Adapter):
    """An adapter to publish applicant data through a simple webservice.
    """
    grok.context(IApplicantOnlinePayment)
    grok.implements(IPayer)

    @property
    def payer(self):
        "The payer object"
        return self.context.__parent__

    @property
    def display_fullname(self):
        "Name of  payer"
        return self.context.__parent__.display_fullname

    @property
    def id(self):
        "Id of payer"
        return self.context.__parent__.applicant_id

    @property
    def reg_number(self):
        "Reg number of payer"
        return self.context.__parent__.reg_number

    @property
    def matric_number(self):
        return 'N/A'

    @property
    def faculty(self):
        return 'N/A'

    @property
    def department(self):
        return 'N/A'

    @property
    def email(self):
        "Email of payer"
        return self.context.__parent__.email

    @property
    def phone(self):
        "Phone number of payer"
        return self.context.__parent__.phone

    @property
    def current_mode(self):
        "Current study mode of payer"
        return 'N/A'

    @property
    def current_level(self):
        "Current level of payer"
        return 'N/A'

    def doAfterPayment(self):
        "Do after payment was made."
        return self.context.doAfterApplicantPayment()

# Applicant online payments must be importable. So we might need a factory.
class ApplicantOnlinePaymentFactory(grok.GlobalUtility):
    """A factory for applicant online payments.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.ApplicantOnlinePayment')
    title = u"Create a new online payment.",
    description = u"This factory instantiates new online payment instances."

    def __call__(self, *args, **kw):
        return ApplicantOnlinePayment()

    def getInterfaces(self):
        return implementedBy(ApplicantOnlinePayment)
