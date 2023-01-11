## $Id: userscontainer.py 12915 2015-05-08 07:09:08Z henrik $
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
"""Users container for the Kofa portal.
"""
import grok
from zope.event import notify
from waeup.kofa.authentication import Account
from waeup.kofa.interfaces import IUsersContainer
from waeup.kofa.utils.logger import Logger
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.interfaces import MessageFactory as _


class UsersContainer(grok.Container, Logger):
    """A container for officers.

    See interfaces.py and users.txt for extensive description.
    """
    grok.implements(IUsersContainer)
    grok.require('waeup.manageUsers')

    def addUser(self, name, password, title=None,
                description=None, email=None, phone=None,
                public_name= None, roles=[]):
        """Add a new Account instance, created from parameters.
        """
        if title is None:
            title = name
        self[name] = Account(name=name, password=password, title=title,
                             description=description, public_name=public_name,
                             email=email, phone=phone, roles=roles)

    def addAccount(self, account):
        """Add the account passed.
        """
        self[account.name] = account

    def delUser(self, name):
        """Delete user, if an account with the given name exists.

        Do not complain, if the name does not exist.
        """
        if name in self.keys():
            del self[name]


class UserExporter(grok.GlobalUtility, ExporterBase):
    """The User Exporter exports all user accounts. It iterates over all
    objects of the ``users`` container.
    """
    grok.implements(ICSVExporter)
    grok.name('users')

    fields = ('name', 'title', 'public_name', 'description',
              'email', 'phone', 'roles', 'local_roles', 'password')
    title = _(u'Users')

    def mangle_value(self, value, name, context=None):
        """The mangler determines the local roles each user has and computes
        a Python expression like:

        ``{u'waeup.local.ClearanceOfficer': [u'faculties/ABC/', u'faculties/DEF/']}``
        """
        if name == 'local_roles' and context is not None:
            local_roles = context.getLocalRoles()
            value = {}
            for role in local_roles.keys():
                objects = local_roles[role]
                object_list = []
                for object in objects:
                    obj= object
                    path = ''
                    while obj.__class__.__name__ != 'University':
                        path = '%s/' % obj.__name__ + path
                        obj = obj.__parent__
                    object_list.append(path)
                value[role] = object_list
        return super(
            UserExporter, self).mangle_value(
            value, name, context=context)

    def export(self, users, filepath=None):
        """Export `users`, an iterable, as CSV file.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for user in users:
            self.write_item(user, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export users into filepath as CSV data.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        users = site.get('users', {})
        return self.export(users.values(), filepath)
