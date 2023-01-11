## $Id: authentication.py 13394 2015-11-06 05:43:37Z henrik $
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
Authenticate applicants.
"""
import grok
from zope.component import getUtility
from zope.password.interfaces import IPasswordManager
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from waeup.kofa.interfaces import IAuthPluginUtility, IUserAccount
from waeup.kofa.applicants.interfaces import IApplicant
from waeup.kofa.students.authentication import (
    StudentAccount, StudentsAuthenticatorPlugin)

class ApplicantAccount(StudentAccount):
    """An adapter to turn applicant objects into accounts on-the-fly.
    """
    grok.context(IApplicant)
    grok.implements(IUserAccount)

    @property
    def name(self):
        return self.context.applicant_id

    @property
    def title(self):
        return self.context.display_fullname

    @property
    def user_type(self):
        return u'applicant'

    def checkPassword(self, password):
        """Check whether the given `password` matches the one stored by
        students. We additionally check if applicant account has been suspended
        or if the portal is blocked.
        """
        try:
            blocker = grok.getSite()['configuration'].maintmode_enabled_by
            if blocker:
                return False
        except TypeError:  # in unit tests
            pass
        if not isinstance(password, basestring):
            return False
        passwordmanager = getUtility(IPasswordManager, 'SSHA')
        if not getattr(self.context, 'password', None):
            # unset/empty passwords do never match
            return False
        if self.context.suspended == True:
            return False
        return passwordmanager.checkPassword(self.context.password, password)

class ApplicantsAuthenticatorPlugin(StudentsAuthenticatorPlugin):
    grok.implements(IAuthenticatorPlugin)
    grok.provides(IAuthenticatorPlugin)
    grok.name('applicants')

    def getAccount(self, login):
        """Look up a applicant identified by `login`. Returns an account.

        First we split the login name into the container part and
        the application number part. Then we simply look up the key under which
        the applicant is stored in the respective applicants cointainer of
        the portal.

        Returns not an applicant but an account object adapted from any
        applicant found.

        If no such applicant exists, ``None`` is returned.
        """
        site = grok.getSite()
        if site is None:
            return None
        applicantsroot = site.get('applicants', None)
        if applicantsroot is None:
            return None
        try:
            container, application_number = login.split('_')
        except ValueError:
            return None
        applicantscontainer = applicantsroot.get(container,None)
        if applicantscontainer is None:
            return None
        applicant = applicantscontainer.get(application_number, None)
        if applicant is None:
            return None
        return IUserAccount(applicant)

class ApplicantsAuthenticatorSetup(grok.GlobalUtility):
    """Register or unregister applicant authentication for a PAU.

    This piece is called when a new site is created.
    """
    grok.implements(IAuthPluginUtility)
    grok.name('applicants_auth_setup')

    def register(self, pau):
        plugins = list(pau.authenticatorPlugins)
        plugins.append('applicants')
        pau.authenticatorPlugins = tuple(plugins)
        return pau

    def unregister(self, pau):
        plugins = [x for x in pau.authenticatorPlugins
                   if x != 'applicants']
        pau.authenticatorPlugins = tuple(plugins)
        return pau
