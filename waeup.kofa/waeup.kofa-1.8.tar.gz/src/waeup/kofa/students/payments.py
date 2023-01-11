## $Id: payments.py 16527 2021-07-06 05:51:42Z henrik $
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
Student payment components.
"""
import grok
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from zope.schema.interfaces import ConstraintNotSatisfied
from hurry.workflow.interfaces import IWorkflowInfo
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.students.interfaces import (
    IStudentPaymentsContainer, IStudentNavigation, IStudentOnlinePayment)
from waeup.kofa.students.workflow import CLEARED, RETURNING, PAID
from waeup.kofa.payments import PaymentsContainer, OnlinePayment
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.accesscodes import create_accesscode

class StudentPaymentsContainer(PaymentsContainer):
    """This is a container for student payments.
    """
    grok.implements(IStudentPaymentsContainer, IStudentNavigation)
    grok.provides(IStudentPaymentsContainer)

    def __init__(self):
        super(StudentPaymentsContainer, self).__init__()
        return

    @property
    def student(self):
        return self.__parent__

    @property
    def certificate(self):
        try:
            return self.student['studycourse'].certificate
        except TypeError:
            return None

    def writeLogMessage(self, view, message):
        return self.__parent__.writeLogMessage(view, message)

StudentPaymentsContainer = attrs_to_fields(StudentPaymentsContainer)

class StudentOnlinePayment(OnlinePayment):
    """This is an online payment.
    """
    grok.implements(IStudentOnlinePayment, IStudentNavigation)
    grok.provides(IStudentOnlinePayment)

    def __init__(self):
        super(StudentOnlinePayment, self).__init__()
        return

    @property
    def student(self):
        try:
            return self.__parent__.__parent__
        except AttributeError:
            return None

    @property
    def certificate(self):
        try:
            return self.student['studycourse'].certificate
        except TypeError:
            return None

    def writeLogMessage(self, view, message):
        return self.__parent__.__parent__.writeLogMessage(view, message)

    def redeemTicket(self):
        """Either create an appropriate access code or trigger an action
        directly.
        """
        student = self.student
        if self.p_category == 'clearance':
            # Create CLR access code
            pin, error = create_accesscode(
                'CLR',0,self.amount_auth,student.student_id)
            if error:
                return error
            self.ac = pin
        elif self.p_category.startswith('schoolfee'):
            # Bypass activation code creation if next session
            # can be started directly.
            if student['studycourse'].next_session_allowed:
                try:
                    if student.state == CLEARED:
                        IWorkflowInfo(student).fireTransition(
                            'pay_first_school_fee')
                        return None
                    elif student.state == RETURNING:
                        IWorkflowInfo(student).fireTransition(
                            'pay_school_fee')
                        return None
                    elif student.state == PAID:
                        IWorkflowInfo(student).fireTransition(
                            'pay_pg_fee')
                        return None
                except ConstraintNotSatisfied:
                    pass
            # Create SFE access code
            pin, error = create_accesscode(
                'SFE',0,self.amount_auth,student.student_id)
            if error:
                return error
            self.ac = pin
        elif self.p_category == 'bed_allocation':
            # Create HOS access code
            pin, error = create_accesscode(
                'HOS',0,self.amount_auth,student.student_id)
            if error:
                return error
            self.ac = pin
        elif self.p_category == 'transcript':
            # Create TSC access code
            pin, error = create_accesscode(
                'TSC',0,self.amount_auth,student.student_id)
            if error:
                return error
            self.ac = pin
        return None

    def doAfterStudentPayment(self):
        """Process student after payment was made.
        """
        if self.p_current:
            error = self.redeemTicket()
            if error is not None:
                return 'danger', error, error
        log = 'successful %s payment: %s' % (self.p_category, self.p_id)
        msg = _('Payment successfully completed')
        flashtype = 'success'
        return flashtype, msg, log

    def doAfterStudentPaymentApproval(self):
        """Process student after payment was approved.
        """
        if self.p_current:
            error = self.redeemTicket()
            if error is not None:
                return 'danger', error, error
        log = '%s payment approved: %s' % (self.p_category, self.p_id)
        msg = _('Payment approved')
        flashtype = 'success'
        return flashtype, msg, log

    def approveStudentPayment(self):
        """Approve payment and process student.
        """
        if self.p_state == 'paid':
            return 'warning', _('This ticket has already been paid.'), None
        self.approve()
        return self.doAfterStudentPaymentApproval()


StudentOnlinePayment = attrs_to_fields(
    StudentOnlinePayment, omit=['display_item'])

class Payer(grok.Adapter):
    """An adapter to publish student data through a simple webservice.
    """
    grok.context(IStudentOnlinePayment)
    grok.implements(IPayer)

    @property
    def payer(self):
        "The payer object"
        return self.context.student

    @property
    def display_fullname(self):
        "Name of  payer"
        return self.context.student.display_fullname

    @property
    def id(self):
        "Id of payer"
        return self.context.student.student_id

    @property
    def matric_number(self):
        "Matric number or reg number of payer"
        return self.context.student.matric_number

    @property
    def reg_number(self):
        "Reg number or reg number of payer"
        return self.context.student.reg_number

    @property
    def faculty(self):
        "Faculty of payer"
        return self.context.student.faccode

    @property
    def department(self):
        "Department of payer"
        return self.context.student.depcode

    @property
    def email(self):
        "Email of payer"
        return self.context.student.email

    @property
    def phone(self):
        "Phone number of payer"
        return self.context.student.phone

    @property
    def current_mode(self):
        "Current study mode of payer"
        return self.context.student.current_mode

    @property
    def current_level(self):
        "Current level of payer"
        return self.context.student.current_level

    def doAfterPayment(self):
        "Do after payment was made."
        return self.context.doAfterStudentPayment()

# Student online payments must be importable. So we might need a factory.
class StudentOnlinePaymentFactory(grok.GlobalUtility):
    """A factory for student online payments.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.StudentOnlinePayment')
    title = u"Create a new online payment.",
    description = u"This factory instantiates new online payment instances."

    def __call__(self, *args, **kw):
        return StudentOnlinePayment()

    def getInterfaces(self):
        return implementedBy(StudentOnlinePayment)
