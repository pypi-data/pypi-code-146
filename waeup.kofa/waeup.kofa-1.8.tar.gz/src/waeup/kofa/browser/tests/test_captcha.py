## $Id: test_captcha.py 15012 2018-05-19 21:47:54Z uli $
## 
## Copyright (C) 2011 Uli Fouquet
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
from zope.component import getAdapter, getUtility
from zope.component.hooks import setSite, clearSite
from zope.interface import verify
from zope.publisher.browser import TestRequest
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.browser.captcha import (
    CaptchaResponse, CaptchaRequest, NullCaptcha, StaticCaptcha, ReCaptcha,
    CaptchaManager)
from waeup.kofa.browser.interfaces import (
    ICaptchaRequest, ICaptchaResponse, ICaptcha, ICaptchaConfig,
    ICaptchaManager)


class CaptchaResponseTests(FunctionalTestCase):

    layer = FunctionalLayer

    def test_ifaces(self):
        # make sure we implement the promised interfaces
        obj = CaptchaResponse(True)
        verify.verifyClass(ICaptchaResponse, CaptchaResponse)
        verify.verifyObject(ICaptchaResponse, obj)
        return

    def test_init_vals(self):
        # make sure the initial values are stored
        resp = CaptchaResponse(False, 'some-msg')
        self.assertEqual(resp.is_valid, False)
        self.assertEqual(resp.error_code, 'some-msg')
        return

class CaptchaRequestTests(FunctionalTestCase):

    layer = FunctionalLayer

    def test_ifaces(self):
        # make sure we implement the promised interfces
        obj = CaptchaRequest(None)
        verify.verifyClass(ICaptchaRequest, CaptchaRequest)
        verify.verifyObject(ICaptchaRequest, obj)
        return

    def test_init_vals(self):
        # make sure initial values are stored
        req = CaptchaRequest('my-solution', 'my-challenge')
        self.assertEqual(req.solution, 'my-solution')
        self.assertEqual(req.challenge, 'my-challenge')
        return

class CaptchaTestBase(object):

    def test_ifaces(self):
        # make sure we implement the promised interfaces
        obj = self.factory()
        verify.verifyClass(ICaptcha, self.factory)
        verify.verifyObject(ICaptcha, obj)
        return

    def test_utility(self):
        # the null captcha is also registered as a utility for ICaptcha
        captcha = getUtility(ICaptcha, name=self.name)
        self.assertTrue(isinstance(captcha, self.factory))
        return

class NullCaptchaTests(FunctionalTestCase, CaptchaTestBase):

    layer = FunctionalLayer

    factory = NullCaptcha
    name = 'No captcha'

    def test_verify(self):
        # null captchas accept any input request
        captcha = self.factory()
        result1 = captcha.verify(TestRequest())
        result2 = captcha.verify(
            TestRequest(form={'solution': 'a', 'challenge': 'b'}))
        self.assertEqual(result1.is_valid, True)
        self.assertEqual(result2.is_valid, True)
        return

    def test_display(self):
        # null captchas do not generate additional HTML code
        captcha = self.factory()
        result = captcha.display()
        self.assertEqual(result, u'')
        return

class StaticCaptchaTests(FunctionalTestCase, CaptchaTestBase):

    layer = FunctionalLayer

    factory = StaticCaptcha
    name = 'Testing captcha'

    def test_verify(self):
        # id captchas accept any solution that matches challenge and
        # is not empty or None
        captcha = self.factory()
        request1 = TestRequest(form={'solution': 'my-sol',
                                     'challenge': 'my-challenge'})
        request2 = TestRequest()
        request3 = TestRequest(form={'solution': '', 'challenge': ''})
        request4 = TestRequest(form={'solution': 'my-sol',
                                     'challenge': 'my-sol'})
        result1 = captcha.verify(request1)
        result2 = captcha.verify(request2)
        result3 = captcha.verify(request3)
        result4 = captcha.verify(request4)
        self.assertEqual(result1.is_valid, False)
        self.assertEqual(result2.is_valid, False)
        self.assertEqual(result3.is_valid, False)
        self.assertEqual(result4.is_valid, True)
        return

    def test_display(self):
        # id captchas provide a simple HTML input
        captcha = self.factory()
        result = captcha.display()
        self.assertMatches(
            '<input type="hidden" name="challenge"'
            '      value="..." /><br />Type: ...<br />'
            '<input type="text" name="solution" value="the-solution" /><br />',
            result)
        return

class ReCaptchaTests(FunctionalTestCase, CaptchaTestBase):

    layer = FunctionalLayer

    factory = ReCaptcha
    name = 'ReCaptcha'

    def DISABLEDtest_verify(self):
        # recaptcha verification cannot be tested easily. As the
        # solution and other environment parameters is only known to
        # the remote server, we cannot guess on server side what the
        # solution is.  Further more this test contacts a remote
        # server so that we might want to disable this test by
        # default.
        captcha = self.factory()
        request1 = TestRequest(
            form={'recaptcha_challenge_field': 'my-challenge',
                  'recaptcha_response_field': 'my-solution'})
        result1 = captcha.verify(request1)
        self.assertEqual(result1.is_valid, False)
        self.assertEqual(result1.error_code, 'invalid-request-cookie')
        return

    def test_display(self):
        # recaptchas provide the pieces to trigger the remote API
        captcha = self.factory()
        result = captcha.display()
        self.assertMatches(
            '<script type="text/javascript" '
            'src="..." async defer></script>'
            '<div class="g-recaptcha" data-sitekey="..."></div>',
            result)
        return

class CaptchaManagerTests(FunctionalTestCase):
    # These tests do not require a site setup
    # See testsuite below for insite tests.

    layer = FunctionalLayer

    def test_ifaces(self):
        # make sure we implement the promised interfaces
        obj = CaptchaManager()
        verify.verifyClass(ICaptchaManager, CaptchaManager)
        verify.verifyObject(ICaptchaManager, obj)
        return

    def test_utility(self):
        # the global captcha chooser is registered as a global utility
        result = getUtility(ICaptchaManager)
        self.assertTrue(isinstance(result, CaptchaManager))
        return

    def test_get_avail_captchas(self):
        # we can get a dict of available captchas.
        chooser = getUtility(ICaptchaManager)
        result = dict(chooser.getAvailCaptchas())
        no_captcha = result.get('No captcha', None)
        self.assertTrue(no_captcha is not None)
        default_captcha = result.get(u'', None)
        self.assertTrue(default_captcha is None)
        return

    def test_get_captcha_wo_site(self):
        # if there is no site set, we get the default captcha
        setSite(None)
        chooser = getUtility(ICaptchaManager)
        result = chooser.getCaptcha()
        default = getUtility(ICaptcha)
        self.assertTrue(result is default)
        return

class FakeSite(grok.Site, grok.Container):
    pass

class FakeConfiguration(object):
    captcha = None

    def __init__(self, captcha=None):
        self.captcha = captcha

class CaptchaManagerTestsWithSite(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(CaptchaManagerTestsWithSite, self).setUp()
        self.getRootFolder()['app'] = FakeSite()
        self.site = self.getRootFolder()['app']
        return

    def tearDown(self):
        super(CaptchaManagerTestsWithSite, self).tearDown()
        clearSite(self.site)
        return

    def test_get_captcha_no_captcha_in_config(self):
        # if a site has no configuration setting for captchas, we get
        # the default captcha
        setSite(self.site)
        chooser = getUtility(ICaptchaManager)
        result = chooser.getCaptcha()
        default = getUtility(ICaptcha)
        self.assertTrue(result is default)
        return

    def test_get_captcha_empty_captcha_in_config(self):
        # if a site has None as configuration setting for captchas, we get
        # the default captcha
        setSite(self.site)
        self.site['configuration'] = dict()
        chooser = getUtility(ICaptchaManager)
        result = chooser.getCaptcha()
        default = getUtility(ICaptcha)
        self.assertTrue(result is default)
        return

    def test_get_captcha_invalid_captcha_in_config(self):
        # if a site has None as configuration setting for captchas, we get
        # the default captcha
        setSite(self.site)
        self.site['configuration'] = FakeConfiguration(captcha='invalid name')
        chooser = getUtility(ICaptchaManager)
        result = chooser.getCaptcha()
        default = getUtility(ICaptcha)
        self.assertTrue(result is default)
        return

    def test_get_captcha_invalid_captcha_in_config(self):
        # if a site has None as configuration setting for captchas, we get
        # the default captcha
        setSite(self.site)
        self.site['configuration'] = FakeConfiguration(captcha='No captcha')
        chooser = getUtility(ICaptchaManager)
        result = chooser.getCaptcha()
        no_captcha = getUtility(ICaptcha, name='No captcha')
        default = getUtility(ICaptcha)
        self.assertTrue(result is not default)
        self.assertTrue(result is no_captcha)
        return
