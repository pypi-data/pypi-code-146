## $Id: test_authentication.py 17269 2023-01-11 08:27:19Z henrik $
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
import grok
import logging
import time
import unittest
from cStringIO import StringIO
from zope.component import getGlobalSiteManager, queryUtility
from zope.component.hooks import setSite, clearSite
from zope.interface.verify import verifyClass, verifyObject
from zope.password.testing import setUpPasswordManagers
from zope.pluggableauth import PluggableAuthentication
from zope.pluggableauth.interfaces import (
    IAuthenticatorPlugin, ICredentialsPlugin)
from zope.publisher.browser import TestRequest
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from waeup.kofa.testing import FunctionalTestCase, FunctionalLayer
from waeup.kofa.app import University
from waeup.kofa.authentication import (
    UserAuthenticatorPlugin, Account, KofaPrincipalInfo, FailedLoginInfo,
    get_principal_role_manager, UsersPlugin, KofaXMLRPCCredentialsPlugin,
    setup_authentication, UpdatePAUPlugin)
from waeup.kofa.interfaces import (
    IAuthPluginUtility, IUserAccount, IFailedLoginInfo, IKofaPrincipalInfo,
    IKofaPluggable)

SECRET = 'HgtuZZZ8'

class FakeSite(grok.Site, grok.Container):
    #def getSiteManager(self):
    #    return None
    #    return getGlobalSiteManager()
    pass


class FakeAuthPlugin(object):
    def register(self, pau):
        pau.credentialsPlugins += ('foo', )


class Test_setup_authentication(FunctionalTestCase):
    # Tests for the `setup_authentication` function

    layer = FunctionalLayer

    def tearDown(self):
        # clean up registry.
        gsm = getGlobalSiteManager()
        for iface, name in ((IAuthPluginUtility, 'myauth'), ):
            to_delete = queryUtility(iface, name=name)
            if to_delete is not None:
                gsm.unregisterUtility(provided=iface, name=name)
        super(Test_setup_authentication, self).tearDown()

    def test_plugins_are_registered(self):
        # We can populate a PAU with (hardcoded set of) plugins
        pau = PluggableAuthentication()
        setup_authentication(pau)
        for name in (
                'No Challenge if Authenticated',
                'xmlrpc-credentials',
                'credentials'):
            assert name in pau.credentialsPlugins
        for name in ('users', ):
            assert name in pau.authenticatorPlugins

    def test_external_plugins_are_registered(self):
        # registered plugins are called as well
        gsm = getGlobalSiteManager()
        gsm.registerUtility(
            FakeAuthPlugin(), IAuthPluginUtility, name='myauth')
        pau = PluggableAuthentication()
        setup_authentication(pau)
        assert 'foo' in pau.credentialsPlugins


class KofaXMLRPCCredentialsPluginTests(FunctionalTestCase):
    # Test for XMLRPC credentials plugin

    layer = FunctionalLayer

    def test_ifaces(self):
        # we meet interface requirements
        plugin = KofaXMLRPCCredentialsPlugin()
        self.assertTrue(
            verifyClass(ICredentialsPlugin, KofaXMLRPCCredentialsPlugin))

    def test_util_is_registered(self):
        # we can query this named utility
        util = queryUtility(ICredentialsPlugin, name='xmlrpc-credentials')
        assert util is not None

    def test_can_extract_creds(self):
        # we can extract credentials from appropriate requests
        req = TestRequest(
            environ={'HTTP_AUTHORIZATION': u'Basic bWdyOm1ncnB3'})
        plugin = KofaXMLRPCCredentialsPlugin()
        assert plugin.extractCredentials(req) == {
            'login': 'mgr', 'password': 'mgrpw'}

    def test_challenge_disabled(self):
        # we will not challenge people
        plugin = KofaXMLRPCCredentialsPlugin()
        assert plugin.challenge(TestRequest()) is False

    def test_logout_disabled(self):
        # we do not support logging out. HTTP basic auth cannot do this.
        plugin = KofaXMLRPCCredentialsPlugin()
        assert plugin.logout(TestRequest()) is False


class UserAuthenticatorPluginTests(FunctionalTestCase):
    # Must be functional because of various utility lookups and the like

    layer = FunctionalLayer

    def setUp(self):
        super(UserAuthenticatorPluginTests, self).setUp()
        self.getRootFolder()['app'] = FakeSite()
        self.site = self.getRootFolder()['app']
        self.site['users'] = {'bob': Account('bob', SECRET)}
        setSite(self.site)
        return

    def tearDown(self):
        super(UserAuthenticatorPluginTests, self).tearDown()
        clearSite()
        return

    def test_ifaces(self):
        # make sure, interfaces requirements are met
        plugin = UserAuthenticatorPlugin()
        plugin.__parent__ = None # This attribute is required by iface
        self.assertTrue(
            verifyClass(IAuthenticatorPlugin, UserAuthenticatorPlugin))
        self.assertTrue(verifyObject(IAuthenticatorPlugin, plugin))
        return

    def test_authenticate_credentials(self):
        # make sure authentication works as expected
        plugin = UserAuthenticatorPlugin()
        result1 = plugin.authenticateCredentials(
            dict(login='bob', password=SECRET))
        result2 = plugin.authenticateCredentials(
            dict(login='bob', password='nonsense'))
        self.assertTrue(isinstance(result1, KofaPrincipalInfo))
        self.assertTrue(result2 is None)
        return

    def test_principal_info(self):
        # make sure we can get a principal info
        plugin = UserAuthenticatorPlugin()
        result1 = plugin.principalInfo('bob')
        result2 = plugin.principalInfo('manfred')
        self.assertTrue(isinstance(result1, KofaPrincipalInfo))
        self.assertTrue(result2 is None)
        return

    def test_get_principal_role_manager(self):
        # make sure we get different role managers for different situations
        prm1 = get_principal_role_manager()
        clearSite(None)
        prm2 = get_principal_role_manager()
        self.assertTrue(IPrincipalRoleManager.providedBy(prm1))
        self.assertTrue(IPrincipalRoleManager.providedBy(prm2))
        self.assertTrue(prm1._context is self.site)
        self.assertTrue(hasattr(prm2, '_context') is False)
        return

    def make_failed_logins(self, num):
        # do `num` failed logins and a valid one afterwards
        del self.site['users']
        self.site['users'] = {'bob': Account('bob', SECRET)}
        plugin = UserAuthenticatorPlugin()
        resultlist = []
        # reset accounts
        for x in range(num):
            resultlist.append(plugin.authenticateCredentials(
                dict(login='bob', password='wrongsecret')))
        resultlist.append(plugin.authenticateCredentials(
            dict(login='bob', password=SECRET)))
        return resultlist

    def DISABLED_test_failed_logins(self):
        # after three failed logins, an account is blocked
        # XXX: this tests authenticator with time penalty (currently
        # disabled)
        results = []
        succ_principal = KofaPrincipalInfo(
            id='bob',
            title='bob',
            description=None,
            email=None,
            phone=None,
            public_name=None,
            user_type=u'user')
        for x in range(4):
            results.append(self.make_failed_logins(x))
        self.assertEqual(results[2], [None, None, succ_principal])
        # last login was blocked although correctly entered due to
        # time penalty
        self.assertEqual(results[3], [None, None, None, None])
        return

class KofaPrincipalInfoTests(unittest.TestCase):

    def create_info(self):
        return KofaPrincipalInfo(
            id='bob',
            title='bob',
            description=None,
            email=None,
            phone=None,
            public_name=None,
            user_type=u'user')

    def test_iface(self):
        # make sure we implement the promised interfaces
        info = self.create_info()
        verifyClass(IKofaPrincipalInfo, KofaPrincipalInfo)
        verifyObject(IKofaPrincipalInfo, info)
        return

    def test_equality(self):
        # we can test two infos for equality
        info1 = self.create_info()
        info2 = self.create_info()
        self.assertEqual(info1, info2)
        self.assertTrue(info1 == info2)
        info1.id = 'blah'
        self.assertTrue(info1 != info2)
        self.assertTrue((info1 == info2) is False)
        info1.id = 'bob'
        info2.id = 'blah'
        self.assertTrue(info1 != info2)
        self.assertTrue((info1 == info2) is False)
        return

class FailedLoginInfoTests(unittest.TestCase):

    def test_iface(self):
        # make sure we fullfill the promised interfaces
        info1 = FailedLoginInfo()
        info2 = FailedLoginInfo(num=1, last=time.time())
        self.assertTrue(
            verifyClass(IFailedLoginInfo, FailedLoginInfo))
        self.assertTrue(verifyObject(IFailedLoginInfo, info1))
        # make sure the stored values have correct type if not None
        self.assertTrue(verifyObject(IFailedLoginInfo, info2))
        return

    def test_default_values(self):
        # By default we get 0, None
        info = FailedLoginInfo()
        self.assertEqual(info.num, 0)
        self.assertEqual(info.last, None)
        return

    def test_set_values_by_attribute(self):
        # we can set values by attribute
        ts = time.gmtime(0)
        info = FailedLoginInfo()
        info.num = 5
        info.last = ts
        self.assertEqual(info.num, 5)
        self.assertEqual(info.last, ts)
        return

    def test_set_values_by_constructor(self):
        # we can set values by constructor args
        ts = time.gmtime(0)
        info = FailedLoginInfo(5, ts)
        self.assertEqual(info.num, 5)
        self.assertEqual(info.last, ts)
        return

    def test_set_values_by_keywords(self):
        # we can set values by constructor keywords
        ts = time.gmtime(0)
        info = FailedLoginInfo(last=ts, num=3)
        self.assertEqual(info.num, 3)
        self.assertEqual(info.last, ts)
        return

    def test_as_tuple(self):
        # we can get the info values as tuple
        ts = time.gmtime(0)
        info = FailedLoginInfo(last=ts, num=3)
        self.assertEqual(info.as_tuple(), (3, ts))
        return

    def test_set_values(self):
        # we can set the values of a an info instance
        ts = time.time()
        info = FailedLoginInfo()
        info.set_values(num=3, last=ts)
        self.assertEqual(info.num, 3)
        self.assertEqual(info.last, ts)
        return

    def test_increase(self):
        # we can increase the number of failed logins
        ts1 = time.time()
        info = FailedLoginInfo()
        info.increase()
        self.assertEqual(info.num, 1)
        # on fast machines the timestamp may not have increased
        self.assertTrue(info.last >= ts1)
        ts2 = info.last
        info.increase()
        self.assertEqual(info.num, 2)
        self.assertTrue(info.last >= ts2)
        return

    def test_reset(self):
        # we can reset failed login infos.
        info = FailedLoginInfo()
        info.increase()
        info.reset()
        self.assertEqual(info.num, 0)
        self.assertEqual(info.last, None)
        return

class AccountTests(unittest.TestCase):

    def setUp(self):
        setUpPasswordManagers()
        return

    def test_iface(self):
        acct = Account('bob', 'mypasswd')
        self.assertTrue(
            verifyClass(IUserAccount, Account))
        self.assertTrue(
            verifyObject(IUserAccount, acct))
        return

    def test_failed_logins(self):
        # we can retrieve infos about failed logins
        ts = time.time()
        acct = Account('bob', 'mypasswd')
        self.assertTrue(hasattr(acct, 'failed_logins'))
        acct.failed_logins.set_values(num=3, last=ts)
        self.assertEqual(acct.failed_logins.last, ts)
        self.assertEqual(acct.failed_logins.num, 3)
        return

    def test_failed_logins_per_inst(self):
        # we get a different counter for each Account instance
        acct1 = Account('bob', 'secret')
        acct2 = Account('alice', 'alsosecret')
        self.assertTrue(acct1.failed_logins is not acct2.failed_logins)
        return

class FakeUserAccount(object):
    pass


def get_logger():
    logger = logging.getLogger('waeup.test')
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.addHandler(handler)
    return logger, stream


class UsersPluginTests(unittest.TestCase):

    def setUp(self):
        setUpPasswordManagers()
        self.site = FakeSite()
        self.site['users'] = grok.Container()
        return

    def test_ifaces(self):
        # make sure we implement the promised interfaces
        plugin = UsersPlugin()
        verifyClass(IKofaPluggable, UsersPlugin)
        verifyObject(IKofaPluggable, plugin)
        return

    def test_update(self):
        # make sure user accounts are updated properly.
        plugin = UsersPlugin()
        logger, stream = get_logger()
        plugin.update(self.site, 'app', logger)
        stream.seek(0)
        self.assertEqual(stream.read(), '')
        self.site['users']['bob'] = FakeUserAccount()
        logger, stream = get_logger()
        plugin.update(self.site, 'app', logger)
        stream.seek(0)
        log_content = stream.read()
        self.assertTrue(hasattr(self.site['users']['bob'], 'description'))
        self.assertTrue(hasattr(self.site['users']['bob'], 'failed_logins'))
        self.assertTrue(
            isinstance(self.site['users']['bob'].failed_logins,
                       FailedLoginInfo))
        self.assertTrue('attribute description added' in log_content)
        self.assertTrue('attribute failed_logins added' in log_content)
        return


class TestUpdatePAUPlugin(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(TestUpdatePAUPlugin, self).setUp()
        self.getRootFolder()['app'] = University()
        self.site = self.getRootFolder()['app']

    def tearDown(self):
        clearSite()
        super(TestUpdatePAUPlugin, self).tearDown()

    def get_pau(self):
        # the PAU is registered as a local utility in local site manager.
        # the name is derived from class name.
        pau = self.site.getSiteManager()['PluggableAuthentication']
        assert pau is not None
        return pau

    def test_update_outdated(self):
        # we can update outdated sites.
        plugin = UpdatePAUPlugin()
        logger, stream = get_logger()
        pau = self.get_pau()
        pau.credentialsPlugins = ('foo', 'credentials', 'bar')
        plugin.update(self.site, 'xmlrpc-credentials', logger)
        assert 'xmlrpc-credentials' in pau.credentialsPlugins
        assert pau.credentialsPlugins.index('xmlrpc-credentials') == 1

    def test_update_uptodate(self):
        # we cope with already updated sites.
        plugin = UpdatePAUPlugin()
        logger, stream = get_logger()
        pau = self.get_pau()
        pau.credentialsPlugins = ('foo', 'xmlrpc-credentials', 'bar')
        plugin.update(self.site, 'xmlrpc-credentials', logger)
        assert pau.credentialsPlugins.count('xmlrpc-credentials') == 1
