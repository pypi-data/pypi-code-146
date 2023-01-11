## $Id: authentication.py 15606 2019-09-24 17:21:28Z henrik $
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
Authenticate students.
"""
import grok
import time
from zope.component import getUtility
from zope.password.interfaces import IPasswordManager
from zope.pluggableauth.interfaces import (
    IAuthenticatorPlugin, ICredentialsPlugin)
from zope.pluggableauth.plugins.session import (
    SessionCredentialsPlugin, SessionCredentials)
from zope.publisher.interfaces.http import IHTTPRequest
from zope.session.interfaces import ISession
from waeup.kofa.authentication import (
    KofaPrincipalInfo, get_principal_role_manager, FailedLoginInfo)
from waeup.kofa.interfaces import (
    IAuthPluginUtility, IUserAccount, IPasswordValidator)
from waeup.kofa.students.interfaces import IStudent

class StudentAccount(grok.Adapter):
    """An adapter to turn student objects into accounts on-the-fly.
    """
    grok.context(IStudent)
    grok.implements(IUserAccount)

    public_name = None

    @property
    def name(self):
        return self.context.student_id

    @property
    def password(self):
        return getattr(self.context, 'password', None)

    @property
    def title(self):
        return self.context.display_fullname

    @property
    def email(self):
        return self.context.email

    @property
    def phone(self):
        return self.context.phone

    @property
    def user_type(self):
        return u'student'

    @property
    def description(self):
        return self.title

    def suspended(self):
        return self.context.suspended

    @property
    def failed_logins(self):
        if not hasattr(self.context, 'failed_logins'):
            self.context.failed_logins = FailedLoginInfo()
        return self.context.failed_logins

    def _get_roles(self):
        prm = get_principal_role_manager()
        roles = [x[0] for x in prm.getRolesForPrincipal(self.name)
                 if x[0].startswith('waeup.')]
        return roles

    def _set_roles(self, roles):
        """Set roles for principal denoted by this account.
        """
        prm = get_principal_role_manager()
        old_roles = self.roles
        for role in old_roles:
            # Remove old roles, not to be set now...
            if role.startswith('waeup.') and role not in roles:
                prm.unsetRoleForPrincipal(role, self.name)
        for role in roles:
            prm.assignRoleToPrincipal(role, self.name)
        return

    roles = property(_get_roles, _set_roles)

    def setPassword(self, password):
        """Set a password (LDAP-compatible) SSHA encoded.

        We do not store passwords in plaintext. Encrypted password is
        stored as unicode string.
        """
        passwordmanager = getUtility(IPasswordManager, 'SSHA')
        self.context.password = passwordmanager.encodePassword(password)

    def checkPassword(self, password):
        """Check whether the given `password` matches the one stored by
        students, the temporary password was set by officers or
        the parents_password was set by parents.
        We additionally check if student account has been suspended
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
        temp_password = self.context.getTempPassword()
        if temp_password:
            return passwordmanager.checkPassword(temp_password, password)
        parents_password = self.context.getParentsPassword()
        if parents_password:
            return passwordmanager.checkPassword(parents_password, password)
        if not getattr(self.context, 'password', None):
            # unset/empty passwords do never match
            return False
        if self.context.suspended == True:
            return False
        return passwordmanager.checkPassword(self.context.password, password)

class StudentsAuthenticatorPlugin(grok.GlobalUtility):
    grok.implements(IAuthenticatorPlugin)
    grok.provides(IAuthenticatorPlugin)
    grok.name('students')

    def authenticateCredentials(self, credentials):
        """Authenticate `credentials`.

        `credentials` is a tuple (login, password).

        We look up students to find out whether a respective student
        exists, then check the password and return the resulting
        `PrincipalInfo` or ``None`` if no such student can be found.
        """
        if not isinstance(credentials, dict):
            return None
        if not ('login' in credentials and 'password' in credentials):
            return None
        account = self.getAccount(credentials['login'])
        if account is None:
            return None
        if not account.checkPassword(credentials['password']):
            return None
        return KofaPrincipalInfo(id=account.name,
                             title=account.title,
                             description=account.description,
                             email=account.email,
                             phone=account.phone,
                             public_name=account.public_name,
                             user_type=account.user_type)

    def principalInfo(self, id):
        """Get a principal identified by `id`.

        This one is required by IAuthenticatorPlugin but not needed here
        (see respective docstring in applicants package).
        """
        return None

    def getAccount(self, login):
        """Look up a student identified by `login`. Returns an account.

        Currently, we simply look up the key under which the student
        is stored in the portal. That means we hit if login name and
        name under which the student is stored match.

        Returns not a student but an account object adapted from any
        student found.

        If no such student exists, ``None`` is returned.
        """
        site = grok.getSite()
        if site is None:
            return None
        studentscontainer = site.get('students', None)
        if studentscontainer is None:
            return None
        student = studentscontainer.get(login, None)
        if student is None:
            return None
        return IUserAccount(student)

class PasswordChangeCredentialsPlugin(grok.GlobalUtility,
                                      SessionCredentialsPlugin):
    """A session credentials plugin that handles the case of a user
    changing his/her own password.

    When users change their own password they might find themselves
    logged out on next request.

    To avoid this, we support to use a 'change password' page a bit
    like a regular login page. That means, on each request we lookup
    the sent data for a login field called 'student_id' and a
    password.

    If both exist, this means someone sent new credentials.

    We then look for the old credentials stored in the user session.
    If the new credentials' login (the student_id) matches the old
    one's, we set the new credentials in session _but_ we return the
    old credentials for the authentication plugins to check as for the
    current request (and for the last time) the old credentials apply.

    No valid credentials are returned by this plugin if one of the
    follwing circumstances is true

    - the sent request is not a regular IHTTPRequest

    - the credentials to set do not match the old ones

    - no credentials are sent with the request

    - no credentials were set before (i.e. the user has no session
      with credentials set before)

    - no session exists already

    - password and repeated password do not match

    Therefore it is mandatory to put this plugin in the line of all
    credentials plugins _before_ other plugins, so that the regular
    credentials plugins can drop in as a 'fallback'.

    This plugin was designed for students to change their passwords,
    but might be used to allow password resets for other types of
    accounts as well.
    """
    grok.provides(ICredentialsPlugin)
    grok.name('student_pw_change')

    loginpagename = 'login'
    loginfield = 'student_id'
    passwordfield = 'change_password'
    repeatfield = 'change_password_repeat'

    def extractCredentials(self, request):
        if not IHTTPRequest.providedBy(request):
            return None
        login = request.get(self.loginfield, None)
        password = request.get(self.passwordfield, None)
        password_repeat = request.get(self.repeatfield, None)

        if not login or not password:
            return None

        validator = getUtility(IPasswordValidator)
        errors = validator.validate_password(password, password_repeat)
        if errors:
            return None

        session = ISession(request)
        sessionData = session.get(
            'zope.pluggableauth.browserplugins')
        if not sessionData:
            return None

        old_credentials = sessionData.get('credentials', None)
        if old_credentials is None:
            # Password changes for already authenticated users only!
            return None
        if old_credentials.getLogin() != login:
            # Special treatment only for users that change their own pw.
            return None
        old_credentials = {
            'login': old_credentials.getLogin(),
            'password': old_credentials.getPassword()}

        # Set new credentials in session. These will be active on next request
        new_credentials = SessionCredentials(login, password)
        sessionData['credentials'] = new_credentials

        # Return old credentials for this one request only
        return old_credentials

class StudentsAuthenticatorSetup(grok.GlobalUtility):
    """Register or unregister student authentication for a PAU.

    This piece is called when a new site is created.
    """
    grok.implements(IAuthPluginUtility)
    grok.name('students_auth_setup')

    def register(self, pau):
        plugins = list(pau.credentialsPlugins)
        # this plugin must come before the regular credentials plugins
        plugins.insert(0, 'student_pw_change')
        pau.credentialsPlugins = tuple(plugins)
        plugins = list(pau.authenticatorPlugins)
        plugins.append('students')
        pau.authenticatorPlugins = tuple(plugins)
        return pau

    def unregister(self, pau):
        plugins = [x for x in pau.authenticatorPlugins
                   if x != 'students']
        pau.authenticatorPlugins = tuple(plugins)
        return pau
