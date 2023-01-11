## $Id: payment.py 13012 2015-05-28 13:55:06Z henrik $
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
These are the payment tickets.
"""
import grok
from datetime import datetime
from grok import index
from zope.event import notify
from zope.component import getUtility
from zope.i18n import translate
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.payments.interfaces import (
    IPayment, IOnlinePayment,
    payment_states)
from waeup.kofa.utils.helpers import attrs_to_fields, get_current_principal
from waeup.kofa.utils.logger import Logger

class Payment(grok.Container, Logger):
    """This is a payment.
    """
    grok.implements(IPayment)
    grok.provides(IPayment)
    grok.baseclass()

    logger_name = 'waeup.kofa.${sitename}.payments'
    logger_filename = 'payments.log'
    logger_format_str = '"%(asctime)s","%(user)s",%(message)s'

    #def logger_info(self, comment=None):
    #    """Get the logger's info method.
    #    """
    #    self.logger.info('%s' % comment)
    #    return

    def __init__(self):
        super(Payment, self).__init__()
        self.creation_date = datetime.utcnow()
        self.p_id = None
        return

    @property
    def p_state_title(self):
        return payment_states.getTermByToken(self.p_state).title

    @property
    def category(self):
        utils = getUtility(IKofaUtils)
        return utils.PAYMENT_CATEGORIES.get(self.p_category, None)

    @property
    def display_item(self):
        kofa_utils = getUtility(IKofaUtils)
        return kofa_utils.getPaymentItem(self)

class OnlinePayment(Payment):
    """This is an online payment.
    """
    grok.implements(IOnlinePayment)
    grok.provides(IOnlinePayment)

    def __init__(self):
        super(OnlinePayment, self).__init__()
        p_id = None
        return

    def approve(self):
        "Approve online payment and set to paid."
        self.r_amount_approved = self.amount_auth
        self.r_code = u'AP'
        self.p_state = 'paid'
        user = get_current_principal()
        if user is None:
            # in tests
            usertitle = 'system'
        else:
            usertitle = getattr(user, 'public_name', None)
            if not usertitle:
                usertitle = user.title
        r_desc = _('Payment approved by ${a}', mapping = {'a': usertitle})
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.r_desc = translate(r_desc, 'waeup.kofa',
            target_language=portal_language)
        self.payment_date = datetime.utcnow()
        # Update catalog
        notify(grok.ObjectModifiedEvent(self))
        return

OnlinePayment = attrs_to_fields(OnlinePayment, omit=['display_item'])
