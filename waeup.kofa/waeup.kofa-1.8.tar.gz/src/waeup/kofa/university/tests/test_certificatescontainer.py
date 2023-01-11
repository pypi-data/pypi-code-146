## $Id: test_certificatescontainer.py 7811 2012-03-08 19:00:51Z uli $
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
Tests for certificate containers and related components.
"""
import shutil
import tempfile
import unittest
from zope.component.hooks import setSite, clearSite
from zope.interface.verify import verifyClass, verifyObject

from waeup.kofa.app import University
from waeup.kofa.interfaces import DuplicationError
from waeup.kofa.testing import (
    FunctionalLayer, doctestsuite_for_module, FunctionalTestCase)
from waeup.kofa.university.certificate import Certificate
from waeup.kofa.university.certificatescontainer import CertificatesContainer
from waeup.kofa.university.interfaces import ICertificatesContainer


class CertificatesContainerTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(CertificatesContainerTests, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(self.app)

    def tearDown(self):
        super(CertificatesContainerTests, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)

    def test_create(self):
        # we can create instances
        container = CertificatesContainer()
        result = isinstance(container, CertificatesContainer)
        assert result is True

    def test_provides_icertificatescontainer(self):
        # instances tell they provide their main interface
        container = CertificatesContainer()
        result = ICertificatesContainer.providedBy(container)
        assert result is True

    def test_interfaces(self):
        # class and instances comply with their main interface
        container = CertificatesContainer()
        self.assertTrue(verifyClass(ICertificatesContainer, CertificatesContainer))
        self.assertTrue(verifyObject(ICertificatesContainer, container))

    def test_add_certificate_non_icertificate(self):
        # we cannot add certificates that do not implement ICertificate.
        container = CertificatesContainer()
        self.assertRaises(
            TypeError, container.addCertificate, 'some_string')

    def test_add_certificate_no_duplicate_entry(self):
        # we cannot add certificates that are registered already.
        container = CertificatesContainer()
        # We must place this container in the ZODB to make catalogs work.
        self.app['certs'] = container
        cert1 = Certificate(code="CERT1")
        cert2 = Certificate(code="CERT1")
        container.addCertificate(cert1)
        self.assertRaises(
            DuplicationError,
            container.addCertificate, cert2)

    def test_setitem_duplicate_entry(self):
        # we cannot add certificates whose code exists already in catalog
        container1 = CertificatesContainer()
        container2 = CertificatesContainer()
        self.app['certs1'] = container1 # enable catalogs
        self.app['certs2'] = container2
        cert1 = Certificate(code="CERT1")
        cert2 = Certificate(code="CERT1")
        self.app['certs1']['CERT1'] = cert1
        self.assertRaises(
            DuplicationError,
            self.app['certs2'].__setitem__, 'CERT1', cert2)
        assert len(container2) == 0

    def test_setitem_name_unequal_code(self):
        # we cannot add certificates whose code != key
        container = CertificatesContainer()
        self.app['certs'] = container # enable catalogs
        cert1 = Certificate(code="CERT1")
        self.assertRaises(
            ValueError,
            container.__setitem__, 'OtherKey', cert1)
        assert len(container) == 0

    def test_clear(self):
        # clear() really empties the container.
        container = CertificatesContainer()
        self.app['certs'] = container # enable catalogs
        cert1 = Certificate(code="CERT1")
        cert2 = Certificate(code="CERT2")
        container['CERT1'] = cert1
        container['CERT2'] = cert2
        container.clear()
        assert len(container) == 0


def test_suite():
    suite = unittest.TestSuite((
        unittest.makeSuite(CertificatesContainerTests),
        doctestsuite_for_module(
                'waeup.kofa.university.certificatescontainer'),
        ))
    return suite

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
