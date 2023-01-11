## $Id: test_payment.py 10030 2013-03-17 08:40:59Z henrik $
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
"""Tests for application payments.

"""
import unittest
from zope.interface import verify
from waeup.kofa.applicants.payment import (
    ApplicantOnlinePayment, ApplicantOnlinePaymentFactory, Payer)
from waeup.kofa.payments.interfaces import IOnlinePayment, IPayer

class ApplicantOnlinePaymentFactoryTest(unittest.TestCase):

    def setUp(self):
        self.factory = ApplicantOnlinePaymentFactory()
        return

    def test_factory(self):
        obj = self.factory()
        assert isinstance(obj, ApplicantOnlinePayment)

    def test_getInterfaces(self):
        implemented_by = self.factory.getInterfaces()
        assert implemented_by.isOrExtends(IOnlinePayment)

    def test_payer_interface(self):
        verify.verifyClass(IPayer, Payer)
