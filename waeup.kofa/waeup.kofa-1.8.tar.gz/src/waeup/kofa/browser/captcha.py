## $Id: captcha.py 15012 2018-05-19 21:47:54Z uli $
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
"""Components to add captcha functionality in views/pages.

This is currently a playground, stuff still to be worked out more properly.
"""
import grok
import json
import urllib
import urllib2
from random import SystemRandom as random
from zope import schema
from zope.component import getUtilitiesFor, getUtility, queryUtility
from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest
from waeup.kofa.browser.layout import KofaPage
from waeup.kofa.browser.interfaces import (
    ICaptchaRequest, ICaptchaResponse, ICaptcha, ICaptchaConfig,
    ICaptchaManager)
from waeup.kofa.interfaces import IUniversity

#
# Global captcha manager
#
class CaptchaManager(grok.GlobalUtility):

    grok.implements(ICaptchaManager)

    def getAvailCaptchas(self):
        """Get all available captchas registered as utils for ICaptcha.

        The default captcha (as it most probably is a copy of another
        registered captcha) is left out of the result.

        Result will be a dict with registration names as keys and the
        specific captcha instances as values.
        """
        result = getUtilitiesFor(ICaptcha)
        return dict([(name,inst) for name,inst in result
                       if name != u''])

    def getCaptcha(self):
        """Get captcha chosen to be used.

        Sites can activate a specific captcha by setting
        ``site['configuration'].captcha``. The attribute should be a
        string under which the specific captcha is registered.

        If this attribute is not set or we are
        not 'in a site', the default captcha is returned.
        """
        site = grok.getSite()
        name = ''
        if site is None:
            return getUtility(ICaptcha)
        name = getattr(site.get('configuration', {}), 'captcha', u'')
        return queryUtility(ICaptcha, name=name,
                            default=getUtility(ICaptcha))

##
## Trivial default captcha
##
class CaptchaResponse(object):
    grok.implements(ICaptchaResponse)
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code
        return

class CaptchaRequest(object):
    grok.implements(ICaptchaRequest)
    def __init__(self, solution=None, challenge=None):
        self.solution = solution
        self.challenge = challenge
        return

class NullCaptcha(object):
    """A captcha that does not expect any input.

    Meant as a placeholder for sites that do not want captchas at all.

    NullCaptchas do not render any HTML/JavaScript and accept any
    request when asked for verification.

    They can be used in pages prepared for captchas where the site
    maintainer decides not to use it at all.
    """
    grok.implements(ICaptcha)

    def verify(self, request):
        return CaptchaResponse(True, None)

    def display(self, error_code=None):
        return u''


# This captcha is registered twice: one time as a 'no captcha' captcha
# and then also as the default captcha (with empty name)
grok.global_utility(NullCaptcha, name=u'No captcha')
grok.global_utility(NullCaptcha, name=u'')

##
## TestCaptcha
##
class StaticCaptcha(object):
    """The StaticCaptcha always has the same solution: 'the-solution'.

    It is of no use for real world but for tests. In tests we cannot
    easily solve really strong captchas. But we can use a captcha that
    works like a real one but is easy to solve even for machines.

    The HTML form piece generated is even prefilled with the correct
    solution. So in tests it is not necessary to always 'type' the
    solution string in the correct field.

    You can, however, fill in a wrong solution and it will be detected
    as such.
    """
    grok.implements(ICaptcha)

    #: name of solution field in HTTP request
    sol_field = 'solution'
    #: name of challenge field in HTTP request
    chal_field = 'challenge'

    def verify(self, request):
        """Verify that a solution sent equals the challenge.
        """
        form = getattr(request, 'form', {})
        solution=form.get(self.sol_field, None)
        challenge=form.get(self.chal_field, None)
        if solution == challenge and solution:
            return CaptchaResponse(is_valid=True)
        return CaptchaResponse(is_valid=False)

    def display(self, error_code=None):
        """Display challenge and input field for solution as HTML.
        """
        html = (
            u'<input type="hidden" name="challenge"'
            u'       value="the-solution" /><br />'
            u'Type: %s<br />'
            u'<input type="text" name="solution" value="the-solution"'
            u' /><br />')
        return html

grok.global_utility(StaticCaptcha, name=u'Testing captcha')


##
## ReCaptcha (v2)
##
class ReCaptcha(StaticCaptcha):
    """ReCaptcha - strong captchas with images, sound, etc.

    This is the Kofa implementation to support captchas as provided by
    http://www.google.com/recaptcha (v2).

    ReCaptcha is widely used and adopted in web applications. See the
    above web page to learn more about recaptcha.

    Basically, it generates a captcha box in a page loaded by a
    client. The client can then enter a solution for a challenge
    picture (or audio file) and send the solution back to our server
    along with the challenge string generated locally on the client.

    This component then verifies the entered solution deploying the
    private key set by asking a verification server. The result (valid
    or invalid solution) is then returned to any calling component.

    As any captcha-component, :class:`ReCaptcha` can be used by any
    other component that wants to display/verify captchas.

    To incorporate captcha usage in a view, page, or viewlet, the
    following steps have to be performed:

    * get the currently site-wide selected captcha type by doing::

        mycaptcha = getUtility(ICaptchaManager).getCaptcha()

    * if you want a specific captcha type (like ReCaptcha)::

        mycaptcha = getUtility(ICaptcha, name='ReCaptcha')

    Now, as you have a captcha, you can verify sent data by doing::

        result = mycaptcha.verify(self.request)

    where ``self.request`` should be the sent HTTP request and
    ``result`` will be an instance of class:``CaptchaResponse``. The
    response will contain an error code (``result.error_code``) that
    might be ``None`` but can (and should) be passed to the
    :meth:``display`` method to display error messages in the captcha
    box. The error code is most probably not a human readable string
    but some code you shouldn't rely upon.

    All this could be done in the ``update()`` method of a view, page,
    or viewlet.

    To render the needed HTML code, you can deploy the
    :meth:`display`` method of ``mycaptcha``.

    This captcha is available at runtime as a global utility named
    ``'ReCaptcha'``.

    Shortcomings:
        - no support for selecting theme
        - no support for selecting box layout (normal, compact)
        - no support for non-javascript users
        - Google will get the data of our clients
        - Google will track all activity of our clients
    """

    grok.implements(ICaptcha)

    #: name of response token field in HTTP request
    token_field = 'g-recaptcha-response'

    # Do not use the following keys in productive environments!  As
    # they are both made publicly available, they are not secure any
    # more!  Use them for testing and evaluating only!
    PUBLIC_KEY = "6Lc0y8oSAAAAAHwdojrqPtcKn7Rww5qGprb0rrSk"
    PRIVATE_KEY = "6Lc0y8oSAAAAAMHVbMrGWLLjw2pm8v2Uprwm9AbR"

    VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

    def verify(self, request):
        """Grab challenge/solution from HTTP request and verify it.

        Verification happens against recaptcha remote API servers. It
        only happens, when a repsonse token was sent with the
        request.

        Returns a :class:`CaptchaResponse` indicating that the
        verification failed or succeeded.
        """
        form = getattr(request, 'form', {})
        token = form.get(self.token_field, None)
        if not token:
            # on first-time display, we won't get a token
            return CaptchaResponse(is_valid=False)
        params = urllib.urlencode(
            {
                'secret': self.PRIVATE_KEY,
                'response': token,
                'remoteip': '127.0.0.1',
                })
        request = urllib2.Request(
            url = self.VERIFY_URL,
            data = params,
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "User-agent": "reCAPTCHA Python Kofa",
                }
            )
        conn = urllib2.urlopen(request)
        ret_vals = json.loads(conn.read())
        conn.close()
        if ret_vals.get('success', False) is True:
            return CaptchaResponse(is_valid=True)
        return CaptchaResponse(
            is_valid=False, error_code="%s" % ret_vals['error-codes'])

    def display(self, error_code=None):
        """Display captcha widget snippet.

        Returns the HTML code to be placed inside an existing ``<form>``
        of your page. You can add other fields and should add a submit
        button to send the form.

        The ``error_code`` can be taken from a previously fetched
        :class:`CaptchaResponse` instance (as returned by
        :meth:`verify`). If it is not ``None``, it might be
        displayed inside the generated captcha box (in human readable
        form).
        """
        error_param = ''
        if error_code:
            error_param = '&error=%s' % error_code

        html = (
            u'<script type="text/javascript" '
            u'src="%(ApiServer)s" async defer>'
            u'</script>'
            u'<div class="g-recaptcha" data-sitekey="%(SiteKey)s"></div>' % {
                'ApiServer': "https://www.google.com/recaptcha/api.js",
                'SiteKey': self.PUBLIC_KEY,
                }
        )
        return html


grok.global_utility(ReCaptcha, name=u'ReCaptcha')


class CaptchaTestPage(KofaPage):
    # A test page to see a captcha in action
    grok.name('captcha')
    grok.context(IUniversity)
    grok.require('waeup.Public')
    title = 'Captcha Test'
    label = title

    def update(self, recaptcha_challenge_field=None,
               recaptcha_response_field=None):
        self.captcha = getUtility(ICaptcha, name='ReCaptcha')
        result = self.captcha.verify(self.request)
        self.captcha_error = result.error_code
        print "VERIFY: ", result.is_valid, result.error_code
        return

    def render(self):
        return """
  <form method="POST" action="">
    %s
    <input type="submit" name="SUBMIT" />
  </form>
  """ % (self.captcha.display(self.captcha_error),)
