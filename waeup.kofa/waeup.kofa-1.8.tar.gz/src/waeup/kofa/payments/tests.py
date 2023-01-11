## $Id: tests.py 13012 2015-05-28 13:55:06Z henrik $
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
Tests for payments.
"""
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.payments.interfaces import (
    IPaymentsContainer, IOnlinePayment)
from waeup.kofa.payments.container import PaymentsContainer
from waeup.kofa.payments.payment import OnlinePayment
from waeup.kofa.testing import (FunctionalLayer, FunctionalTestCase)

class PaymentsContainerTestCase(FunctionalTestCase):

    layer = FunctionalLayer

    def test_interfaces(self):
        # Make sure the correct interfaces are implemented.
        self.assertTrue(
            verifyClass(
                IPaymentsContainer, PaymentsContainer)
            )
        self.assertTrue(
            verifyObject(
                IPaymentsContainer, PaymentsContainer())
            )
        self.assertTrue(
            verifyClass(
                IOnlinePayment, OnlinePayment)
            )
        self.assertTrue(
            verifyObject(
                IOnlinePayment, OnlinePayment())
            )
        return

    def test_base(self):
        # We cannot call the fundamental methods of a base in that case
        container = PaymentsContainer()
        self.assertRaises(
            NotImplementedError, container.archive)
        self.assertRaises(
            NotImplementedError, container.clear)
