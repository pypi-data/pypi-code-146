## $Id: authentication.py 15302 2019-01-18 09:46:41Z henrik $
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
"""Authentication for Kofa.
"""
import grok
import time
import re
from zope.i18n import translate
from zope.event import notify
from zope.component import getUtility, getUtilitiesFor
from zope.component.interfaces import IFactory
from zope.interface import Interface, implementedBy
from zope.schema import getFields
from zope.securitypolicy.interfaces import (
    IPrincipalRoleMap, IPrincipalRoleManager)
from zope.pluggableauth.factories import Principal
from zope.pluggableauth.plugins.session import SessionCredentialsPlugin
from zope.pluggableauth.plugins.httpplugins import (
    HTTPBasicAuthCredentialsPlugin)
from zope.pluggableauth.interfaces import (
    ICredentialsPlugin, IAuthenticatorPlugin, IAuthenticatedPrincipalFactory,
    AuthenticatedPrincipalCreated)
from zope.publisher.interfaces import IRequest
from zope.password.interfaces import IPasswordManager
from zope.securitypolicy.principalrole import principalRoleManager
from waeup.kofa.interfaces import (
    ILocalRoleSetEvent, IUserAccount, IAuthPluginUtility, IPasswordValidator,
    IKofaPrincipal, IKofaPrincipalInfo, IKofaPluggable, IBatchProcessor,
    IGNORE_MARKER, IFailedLoginInfo)
from waeup.kofa.utils.batching import BatchProcessor
from waeup.kofa.permissions import get_all_roles
from waeup.kofa.interfaces import MessageFactory as _


def setup_authentication(pau):
    """Set up plugguble authentication utility.

    Sets up an IAuthenticatorPlugin and
    ICredentialsPlugin (for the authentication mechanism)

    Then looks for any external utilities that want to modify the PAU.
    """
    pau.credentialsPlugins = (
        'No Challenge if Authenticated',
        'xmlrpc-credentials',
        'credentials')
    pau.authenticatorPlugins = ('users',)

    # Give any third-party code and subpackages a chance to modify the PAU
    auth_plugin_utilities = getUtilitiesFor(IAuthPluginUtility)
    for name, util in auth_plugin_utilities:
        util.register(pau)


def get_principal_role_manager():
    """Get a role manager for principals.

    If we are currently 'in a site', return the role manager for the
    portal or the global rolemanager else.
    """
    portal = grok.getSite()
    if portal is not None:
        return IPrincipalRoleManager(portal)
    return principalRoleManager


class KofaSessionCredentialsPlugin(
        grok.GlobalUtility, SessionCredentialsPlugin):
    """Session plugin that picks usernames/passwords from fields in webforms.
    """
    grok.provides(ICredentialsPlugin)
    grok.name('credentials')

    loginpagename = 'login'
    loginfield = 'form.login'
    passwordfield = 'form.password'


class KofaXMLRPCCredentialsPlugin(
        grok.GlobalUtility, HTTPBasicAuthCredentialsPlugin):
    """Plugin that picks useranams/passwords from basic-auth headers.

    As XMLRPC requests send/post their authentication credentials in HTTP
    basic-auth headers, we need a plugin that can handle this.

    This plugin, however, does no challenging. If a user does not provide
    basic-auth infos, we will not ask for some. This is correct as we plan to
    communicate with machines.

    This plugin is planned to be used in "PluggableAuthenitications" registered
    with `University` instances.
    """
    grok.provides(ICredentialsPlugin)
    grok.name('xmlrpc-credentials')

    def challenge(self, request):
        """XMLRPC is for machines. No need to challenge.
        """
        return False

    def logout(self, request):
        """Basic auth does not provide any logout possibility.
        """
        return False


class KofaPrincipalInfo(object):
    """An implementation of IKofaPrincipalInfo.

    A Kofa principal info is created with id, login, title, description,
    phone, email, public_name and user_type.
    """
    grok.implements(IKofaPrincipalInfo)

    def __init__(self, id, title, description, email, phone, public_name,
                 user_type):
        self.id = id
        self.title = title
        self.description = description
        self.email = email
        self.phone = phone
        self.public_name = public_name
        self.user_type = user_type
        self.credentialsPlugin = None
        self.authenticatorPlugin = None

    def __eq__(self, obj):
        default = object()
        result = []
        for name in ('id', 'title', 'description', 'email', 'phone',
                     'public_name', 'user_type', 'credentialsPlugin',
                     'authenticatorPlugin'):
            result.append(
                getattr(self, name) == getattr(obj, name, default))
        return False not in result


class KofaPrincipal(Principal):
    """A portal principal.

    Kofa principals provide an extra `email`, `phone`, `public_name`
    and `user_type` attribute extending ordinary principals.
    """

    grok.implements(IKofaPrincipal)

    def __init__(self, id, title=u'', description=u'', email=u'',
                 phone=None, public_name=u'', user_type=u'', prefix=None):
        self.id = id
        if prefix is not None:
            self.id = '%s.%s' % (prefix, self.id)
        self.title = title
        self.description = description
        self.groups = []
        self.email = email
        self.phone = phone
        self.public_name = public_name
        self.user_type = user_type

    def __repr__(self):
        return 'KofaPrincipal(%r)' % self.id


class AuthenticatedKofaPrincipalFactory(grok.MultiAdapter):
    """Creates 'authenticated' Kofa principals.

    Adapts (principal info, request) to a KofaPrincipal instance.

    This adapter is used by the standard PAU to transform
    KofaPrincipalInfos into KofaPrincipal instances.
    """
    grok.adapts(IKofaPrincipalInfo, IRequest)
    grok.implements(IAuthenticatedPrincipalFactory)

    def __init__(self, info, request):
        self.info = info
        self.request = request

    def __call__(self, authentication):
        principal = KofaPrincipal(
            self.info.id,
            self.info.title,
            self.info.description,
            self.info.email,
            self.info.phone,
            self.info.public_name,
            self.info.user_type,
            authentication.prefix,
            )
        notify(
            AuthenticatedPrincipalCreated(
                authentication, principal, self.info, self.request))
        return principal


class FailedLoginInfo(grok.Model):
    grok.implements(IFailedLoginInfo)

    def __init__(self, num=0, last=None):
        self.num = num
        self.last = last
        return

    def as_tuple(self):
        return (self.num, self.last)

    def set_values(self, num=0, last=None):
        self.num, self.last = num, last
        self._p_changed = True
        pass

    def increase(self):
        self.set_values(num=self.num + 1, last=time.time())
        pass

    def reset(self):
        self.set_values(num=0, last=None)
        pass


class Account(grok.Model):
    """Kofa user accounts store infos about a user.

    Beside the usual data and an (encrypted) password, accounts also
    have a persistent attribute `failed_logins` which is an instance
    of `waeup.kofa.authentication.FailedLoginInfo`.

    This attribute can be manipulated directly (set new value,
    increase values, or reset).
    """
    grok.implements(IUserAccount)

    def __init__(self, name, password, title=None, description=None,
                 email=None, phone=None, public_name=None, roles=[]):
        self.name = name
        if title is None:
            title = name
        self.title = title
        self.description = description
        self.email = email
        self.phone = phone
        self.public_name = public_name
        self.suspended = False
        self.setPassword(password)
        self.setSiteRolesForPrincipal(roles)

        # We don't want to share this dict with other accounts
        self._local_roles = dict()
        self.failed_logins = FailedLoginInfo()

    def setPassword(self, password):
        passwordmanager = getUtility(IPasswordManager, 'SSHA')
        self.password = passwordmanager.encodePassword(password)

    def checkPassword(self, password):
        try:
            blocker = grok.getSite()['configuration'].maintmode_enabled_by
            if blocker and blocker != self.name:
                return False
        except (TypeError, KeyError):  # in unit tests
            pass
        if not isinstance(password, basestring):
            return False
        if not self.password:
            # unset/empty passwords do never match
            return False
        # Do not accept password if password is insecure.
        validator = getUtility(IPasswordValidator)
        if validator.validate_secure_password(password, password):
            return False
        if self.suspended:
            return False
        passwordmanager = getUtility(IPasswordManager, 'SSHA')
        return passwordmanager.checkPassword(self.password, password)

    def getSiteRolesForPrincipal(self):
        prm = get_principal_role_manager()
        roles = [x[0] for x in prm.getRolesForPrincipal(self.name)
                 if x[0].startswith('waeup.')]
        return roles

    def setSiteRolesForPrincipal(self, roles):
        prm = get_principal_role_manager()
        old_roles = self.getSiteRolesForPrincipal()
        if sorted(old_roles) == sorted(roles):
            return
        for role in old_roles:
            # Remove old roles, not to be set now...
            if role.startswith('waeup.') and role not in roles:
                prm.unsetRoleForPrincipal(role, self.name)
        for role in roles:
            # Convert role to ASCII string to be in line with the
            # event handler
            prm.assignRoleToPrincipal(str(role), self.name)
        return

    roles = property(getSiteRolesForPrincipal, setSiteRolesForPrincipal)

    def getLocalRoles(self):
        return self._local_roles

    def notifyLocalRoleChanged(self, obj, role_id, granted=True):
        objects = self._local_roles.get(role_id, [])
        if granted and obj not in objects:
            objects.append(obj)
        if not granted and obj in objects:
            objects.remove(obj)
        self._local_roles[role_id] = objects
        if len(objects) == 0:
            del self._local_roles[role_id]
        self._p_changed = True
        return


class UserAuthenticatorPlugin(grok.GlobalUtility):
    grok.implements(IAuthenticatorPlugin)
    grok.provides(IAuthenticatorPlugin)
    grok.name('users')

    def authenticateCredentials(self, credentials):
        if not isinstance(credentials, dict):
            return None
        if not ('login' in credentials and 'password' in credentials):
            return None
        account = self.getAccount(credentials['login'])
        if account is None:
            return None
        # The following shows how 'time penalties' could be enforced
        # on failed logins. First three failed logins are 'for
        # free'. After that the user has to wait for 1, 2, 4, 8, 16,
        # 32, ... seconds before a login can succeed.
        # There are, however, some problems to discuss, before we
        # really use this in all authenticators.

        #num, last = account.failed_logins.as_tuple()
        #if (num > 2) and (time.time() < (last + 2**(num-3))):
        #    # tried login while account still blocked due to previous
        #    # login errors.
        #    return None
        if not account.checkPassword(credentials['password']):
            #account.failed_logins.increase()
            return None
        return KofaPrincipalInfo(
            id=account.name,
            title=account.title,
            description=account.description,
            email=account.email,
            phone=account.phone,
            public_name=account.public_name,
            user_type=u'user')

    def principalInfo(self, id):
        account = self.getAccount(id)
        if account is None:
            return None
        return KofaPrincipalInfo(
            id=account.name,
            title=account.title,
            description=account.description,
            email=account.email,
            phone=account.phone,
            public_name=account.public_name,
            user_type=u'user')

    def getAccount(self, login):
        # ... look up the account object and return it ...
        userscontainer = self.getUsersContainer()
        if userscontainer is None:
            return
        return userscontainer.get(login, None)

    def addAccount(self, account):
        userscontainer = self.getUsersContainer()
        if userscontainer is None:
            return
        # XXX: complain if name already exists...
        userscontainer.addAccount(account)

    def addUser(self, name, password, title=None, description=None):
        userscontainer = self.getUsersContainer()
        if userscontainer is None:
            return
        userscontainer.addUser(name, password, title, description)

    def getUsersContainer(self):
        site = grok.getSite()
        return site['users']


class PasswordValidator(grok.GlobalUtility):

    grok.implements(IPasswordValidator)

    def validate_password(self, pw, pw_repeat):
        errors = []
        if len(pw) < 6:
            errors.append(translate(_(
                'Password must have at least 6 characters.')))
        if pw != pw_repeat:
            errors.append(translate(_('Passwords do not match.')))
        return errors

    def validate_secure_password(self, pw, pw_repeat):
        """
        ^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$

        ^              Start anchor
        (?=.*[A-Z])    Ensure password has one uppercase letters.
        (?=.*[0-9])    Ensure password has one digit.
        (?=.*[a-z])    Ensure password has one lowercase letter.
        .{8,}          Ensure password is of length 8.
        $              End anchor
        """
        check_pw = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$").match
        errors = []
        if not check_pw(pw):
            errors.append(translate(_(
                'Passwords must be at least 8 characters long, '
                'must contain at least one uppercase letter, '
                'one lowercase letter and one digit.')))
        if pw != pw_repeat:
            errors.append(translate(_('Passwords do not match.')))
        return errors


class LocalRoleSetEvent(object):

    grok.implements(ILocalRoleSetEvent)

    def __init__(self, object, role_id, principal_id, granted=True):
        self.object = object
        self.role_id = role_id
        self.principal_id = principal_id
        self.granted = granted


@grok.subscribe(IUserAccount, grok.IObjectRemovedEvent)
def handle_account_removed(account, event):
    """When an account is removed, local and global roles might
    have to be deleted.
    """
    local_roles = account.getLocalRoles()
    principal = account.name

    for role_id, object_list in local_roles.items():
        for object in object_list:
            try:
                role_manager = IPrincipalRoleManager(object)
            except TypeError:
                # No Account object, no role manager, no local roles to remove
                continue
            role_manager.unsetRoleForPrincipal(role_id, principal)
    role_manager = IPrincipalRoleManager(grok.getSite())
    roles = account.getSiteRolesForPrincipal()
    for role_id in roles:
        role_manager.unsetRoleForPrincipal(role_id, principal)
    return


@grok.subscribe(IUserAccount, grok.IObjectAddedEvent)
def handle_account_added(account, event):
    """When an account is added, the local owner role and the global
    AcademicsOfficer role must be set.
    """
    # We set the local Owner role
    role_manager_account = IPrincipalRoleManager(account)
    role_manager_account.assignRoleToPrincipal(
        'waeup.local.Owner', account.name)
    # We set the global AcademicsOfficer role
    site = grok.getSite()
    role_manager_site = IPrincipalRoleManager(site)
    role_manager_site.assignRoleToPrincipal(
        'waeup.AcademicsOfficer', account.name)
    # Finally we have to notify the user account that the local role
    # of the same object has changed
    notify(LocalRoleSetEvent(
        account, 'waeup.local.Owner', account.name, granted=True))
    return


@grok.subscribe(Interface, ILocalRoleSetEvent)
def handle_local_role_changed(obj, event):
    site = grok.getSite()
    if site is None:
        return
    users = site.get('users', None)
    if users is None:
        return
    if event.principal_id not in users.keys():
        return
    user = users[event.principal_id]
    user.notifyLocalRoleChanged(event.object, event.role_id, event.granted)
    return


@grok.subscribe(Interface, grok.IObjectRemovedEvent)
def handle_local_roles_on_obj_removed(obj, event):
    try:
        role_map = IPrincipalRoleMap(obj)
    except TypeError:
        # no map, no roles to remove
        return
    for local_role, user_name, setting in role_map.getPrincipalsAndRoles():
        notify(LocalRoleSetEvent(
            obj, local_role, user_name, granted=False))
    return


class UserAccountFactory(grok.GlobalUtility):
    """A factory for user accounts.

    This factory is only needed for imports.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.UserAccount')
    title = u"Create a user.",
    description = u"This factory instantiates new user account instances."

    def __call__(self, *args, **kw):
        return Account(name=None, password='')

    def getInterfaces(self):
        return implementedBy(Account)


class UserProcessor(BatchProcessor):
    """The User Processor processes user accounts, i.e. `Account` objects in
    the ``users`` container.

    The `roles` columns must contain Python list
    expressions like ``['waeup.PortalManager', 'waeup.ImportManager']``.

    The processor does not import local roles. These can be imported
    by means of batch processors in the academic section.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'userprocessor'
    grok.name(util_name)

    name = u'User Processor'
    iface = IUserAccount

    location_fields = ['name', ]
    factory_name = 'waeup.UserAccount'

    mode = None

    def parentsExist(self, row, site):
        return 'users' in site.keys()

    def entryExists(self, row, site):
        return row['name'] in site['users'].keys()

    def getParent(self, row, site):
        return site['users']

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        parent = self.getParent(row, site)
        return parent.get(row['name'])

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent.addAccount(obj)
        return

    def delEntry(self, row, site):
        user = self.getEntry(row, site)
        if user is not None:
            parent = self.getParent(row, site)
            grok.getSite().logger.info(
                '%s - %s - User removed' % (self.name, row['name']))
            del parent[user.name]
        pass

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        changed = []
        for key, value in row.items():
            if key == 'roles':
                # We cannot simply set the roles attribute here because
                # we can't assure that the name attribute is set before
                # the roles attribute is set.
                continue
            # Skip fields to be ignored.
            if value == IGNORE_MARKER:
                continue
            if not hasattr(obj, key):
                continue
            setattr(obj, key, value)
            changed.append('%s=%s' % (key, value))
        roles = row.get('roles', IGNORE_MARKER)
        if roles not in ('', IGNORE_MARKER):
            evalvalue = eval(roles)
            if isinstance(evalvalue, list):
                setattr(obj, 'roles', evalvalue)
                changed.append('roles=%s' % roles)
        # Log actions...
        items_changed = ', '.join(changed)
        grok.getSite().logger.info(
            '%s - %s - %s - updated: %s' % (
                self.name, filename, row['name'], items_changed))
        return

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        errs, inv_errs, conv_dict = super(
            UserProcessor, self).checkConversion(row, mode=mode)
        # We need to check if roles exist.
        roles = row.get('roles', IGNORE_MARKER)
        all_roles = [i[0] for i in get_all_roles()]
        if roles not in ('', IGNORE_MARKER):
            evalvalue = eval(roles)
            for role in evalvalue:
                if role not in all_roles:
                    errs.append(('roles', 'invalid role'))
        return errs, inv_errs, conv_dict


class UsersPlugin(grok.GlobalUtility):
    """A plugin that updates users.
    """
    grok.implements(IKofaPluggable)
    grok.name('users')

    deprecated_attributes = []

    def setup(self, site, name, logger):
        return

    def update(self, site, name, logger):
        users = site['users']
        items = getFields(IUserAccount).items()
        for user in users.values():
            # Add new attributes
            for i in items:
                if not hasattr(user, i[0]):
                    setattr(user, i[0], i[1].missing_value)
                    logger.info(
                        'UsersPlugin: %s attribute %s added.' % (
                            user.name, i[0]))
            if not hasattr(user, 'failed_logins'):
                # add attribute `failed_logins`...
                user.failed_logins = FailedLoginInfo()
                logger.info(
                    'UsersPlugin: attribute failed_logins added.')
            # Remove deprecated attributes
            for i in self.deprecated_attributes:
                try:
                    delattr(user, i)
                    logger.info(
                        'UsersPlugin: %s attribute %s deleted.' % (
                            user.name, i))
                except AttributeError:
                    pass
        return


class UpdatePAUPlugin(grok.GlobalUtility):
    """A plugin that updates a local PAU.

    We insert an 'xmlrpc-credentials' PAU-plugin into a sites PAU if it is not
    present already. There must be 'credentials' plugin registered already.

    XXX: This Plugin fixes a shortcoming of waeup.kofa 1.5. Sites created or
         updated afterwards do not need this plugin and it should be removed.
    """
    grok.implements(IKofaPluggable)
    grok.name('site-pluggable-auth')

    def setup(self, site, name, logger):
        return

    def update(self, site, name, logger):
        pau = site.getSiteManager()['PluggableAuthentication']
        if 'xmlrpc-credentials' in pau.credentialsPlugins:
            return
        plugins = list(pau.credentialsPlugins)
        plugins.insert(plugins.index('credentials'), 'xmlrpc-credentials')
        pau.credentialsPlugins = tuple(plugins)
