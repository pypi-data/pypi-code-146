## $Id: test_configuration.py 7811 2012-03-08 19:00:51Z uli $
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
"""Tests for configuration containers and related.
"""
from zope.component.interfaces import IFactory
from zope.interface import verify
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.configuration import (
    ConfigurationContainer, SessionConfiguration, SessionConfigurationFactory)
from waeup.kofa.interfaces import(
    IConfigurationContainer, ISessionConfiguration, ISessionConfigurationAdd)

class ConfigurationTest(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(ConfigurationTest, self).setUp()
        self.confcontainer = ConfigurationContainer()
        self.sessionconf = SessionConfiguration()
        return

    def tearDown(self):
        super(ConfigurationTest, self).tearDown()
        return

    def test_interfaces(self):
        verify.verifyClass(IConfigurationContainer, ConfigurationContainer)
        verify.verifyObject(IConfigurationContainer, self.confcontainer)
        verify.verifyClass(ISessionConfiguration, SessionConfiguration)
        verify.verifyObject(ISessionConfiguration, self.sessionconf)
        verify.verifyClass(ISessionConfigurationAdd, SessionConfiguration)
        verify.verifyObject(ISessionConfigurationAdd, self.sessionconf)

class SessionConfigurationFactoryTest(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(SessionConfigurationFactoryTest, self).setUp()
        self.factory = SessionConfigurationFactory()

    def tearDown(self):
        super(SessionConfigurationFactoryTest, self).tearDown()

    def test_interfaces(self):
        verify.verifyClass(IFactory, SessionConfigurationFactory)
        verify.verifyObject(IFactory, self.factory)

    def test_factory(self):
        obj = self.factory()
        assert isinstance(obj, SessionConfiguration)

    def test_getInterfaces(self):
        implemented_by = self.factory.getInterfaces()
        assert implemented_by.isOrExtends(ISessionConfiguration)
