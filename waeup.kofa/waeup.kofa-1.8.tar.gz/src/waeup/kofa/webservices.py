## $Id: webservices.py 10477 2013-08-10 01:10:04Z uli $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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

import grok
from zope.component import getUtility
from zope.catalog.interfaces import ICatalog
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.interfaces import IUniversity, academic_sessions_vocab

class PaymentDataWebservice(grok.View):
    """A simple webservice to publish payment and payer details on request from
    accepted IP addresses without authentication.

    """
    grok.context(IUniversity)
    grok.name('paymentrequest')
    grok.require('waeup.Public')

    #ACCEPTED_IP = ('174.36.230.28', )
    ACCEPTED_IP = ('127.0.0.1', )

    def update(self, P_ID=None):
        if P_ID == None:
            self.output = '-1'
            return
        real_ip = self.request.get('HTTP_X_FORWARDED_FOR', None)
        if real_ip:
            self.context.logger.info('PaymentDataWebservice called: %s' % real_ip)
        if real_ip and self.ACCEPTED_IP:
            if real_ip not in  self.ACCEPTED_IP:
                self.output = '-4'
                return
        cat = getUtility(ICatalog, name='payments_catalog')
        results = list(
            cat.searchResults(p_id=(P_ID, P_ID), p_state=('paid', 'paid')))
        if len(results) != 1:
            self.output = '-1'
            return
        try:
            owner = IPayer(results[0])
            full_name = owner.display_fullname
            reg_number = owner.reg_number
            matric_number = owner.matric_number
            faculty = owner.faculty
            department = owner.department
        except (TypeError, AttributeError):
            self.output = '-3'
            return
        amount = results[0].amount_auth
        payment_category = results[0].category
        payment_item = results[0].p_item
        academic_session = academic_sessions_vocab.getTerm(
            results[0].p_session).title
        self.output = (
            'FULL_NAME=%s&' +
            'FACULTY=%s&' +
            'DEPARTMENT=%s&' +
            'PAYMENT_ITEM=%s&' +
            'PAYMENT_CATEGORY=%s&' +
            'ACADEMIC_SESSION=%s&' +
            'MATRIC_NUMBER=%s&' +
            'REG_NUMBER=%s&' +
            'FEE_AMOUNT=%s') % (full_name, faculty,
            department, payment_item, payment_category,
            academic_session, matric_number, reg_number, amount)
        return

    def render(self):
        return self.output

class XMLRPCPermission(grok.Permission):
    """Permission for using XMLRPC functions.
    """
    grok.name('waeup.xmlrpc')

class XMLRPCUsers1(grok.Role):
    """Usergroup 1
    """
    grok.name('waeup.xmlrpcusers1')
    grok.title('XMLRPC Users Group 1')
    grok.permissions('waeup.xmlrpc',)

class UniversityXMLRPC(grok.XMLRPC):
    """XMLRPC webservices for KOFA portals.

    Please note, that XMLRPC does not support real keyword arguments
    but positional arguments only.
    """
    grok.context(IUniversity)

    @grok.require('waeup.Public')
    def xmlrpc_api_version(self):
        """Return the current API version for XMLRPC clients.
        """
        return u'0.1'
