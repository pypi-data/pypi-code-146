## $Id: interfaces.py 16526 2021-07-05 15:42:14Z henrik $
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
from zope.interface import Attribute
from zope import schema
from waeup.kofa.interfaces import (
    IKofaObject, SimpleKofaVocabulary, academic_sessions_vocab,
    ContextualDictSourceFactoryBase)
from waeup.kofa.interfaces import MessageFactory as _

payment_states = SimpleKofaVocabulary(
    (_('Not yet paid'),'unpaid'),
    (_('Paid'),'paid'),
    (_('Failed'),'failed'),
    (_('Fees waived'),'waived'),
    (_('Scholarship'),'scholarship'),
    )

class PaymentCategorySource(ContextualDictSourceFactoryBase):
    """A payment category source delivers all categories of payments.

    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'PAYMENT_CATEGORIES'

class PaymentOptionSource(ContextualDictSourceFactoryBase):
    """A payment option source delivers all options of a payment.

    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'PAYMENT_OPTIONS'

class CombiPaymentCategorySource(ContextualDictSourceFactoryBase):
    """A payment category source delivers all categories of payments.

    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'COMBI_PAYMENT_CATEGORIES'

class IPaymentsContainer(IKofaObject):
    """A container for all kind of payment objects.

    """

class IPayment(IKofaObject):
    """A base representation of payments.

    """
    p_id = Attribute('Payment identifier')

    p_category = schema.Choice(
        title = _(u'Payment Category'),
        #default = u'schoolfee',
        source = PaymentCategorySource(),
        required = True,
        )

    p_option = schema.Choice(
        title = _(u'Payment Option'),
        source = PaymentOptionSource(),
        required = False,
        )

    p_item = schema.TextLine(
        title = u'',
        default = None,
        required = False,
        )

    p_combi = schema.List(
        title = _(u'Combi Payment'),
        value_type = schema.Choice(
            source = CombiPaymentCategorySource(),
            ),
        required = False,
        defaultFactory=list,
        )

    display_item = schema.TextLine(
        title = _(u'Payment Item'),
        required = False,
        readonly = True,
        )

    p_session = schema.Choice(
        title = _(u'Payment Session'),
        source = academic_sessions_vocab,
        required = True,
        )

    p_state = schema.Choice(
        title = _(u'Payment State'),
        default = u'unpaid',
        vocabulary = payment_states,
        required = True,
        )

    creation_date = schema.Datetime(
        title = _(u'Ticket Creation Date'),
        readonly = False,
        required = False,
        )

    payment_date = schema.Datetime(
        title = _(u'Payment Date'),
        required = False,
        readonly = False,
        )

    amount_auth = schema.Float(
        title = _(u'Amount Authorized'),
        default = 0.0,
        required = True,
        readonly = False,
        )

class IOnlinePayment(IPayment):
    """A payment via payment gateways.

    """

    ac = schema.TextLine(
        title = _(u'Activation Code'),
        default = None,
        required = False,
        readonly = False,
        )

    r_amount_approved = schema.Float(
        title = _(u'Response Amount Approved'),
        default = 0.0,
        required = False,
        readonly = False,
        )

    r_code = schema.TextLine(
        title = _(u'Response Code'),
        default = None,
        required = False,
        readonly = False,
        )

    r_desc = schema.TextLine(
        title = _(u'Response Description'),
        default = None,
        required = False,
        readonly = False,
        )

    def approve():
        "Approve an online payment and set to paid."

class IPayer(IKofaObject):
    """An interface for an adapter to publish student and applicant data
    through a simple webservice. Also used in payment modules.

    """
    payer = Attribute("The payer object")
    display_fullname = Attribute('Name of payer')
    id = Attribute('Id of payer')
    reg_number = Attribute('Reg number of payer')
    matric_number = Attribute('Matric number of payer')
    faculty = Attribute('Faculty of payer')
    department = Attribute('Department of payer')
    email= Attribute('Email of payer')
    phone= Attribute('Phone number of payer')
    current_mode= Attribute('Current study mode of payer')
    current_level= Attribute('Current level of payer')

    def doAfterPayment():
        "Do after payment was made."
