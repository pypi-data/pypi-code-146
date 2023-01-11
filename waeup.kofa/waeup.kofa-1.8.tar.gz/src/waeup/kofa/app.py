## $Id: app.py 15708 2019-10-28 22:37:30Z henrik $
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
from zope.authentication.interfaces import IAuthentication
from zope.component import getUtility, getUtilitiesFor
from zope.component.interfaces import ObjectEvent
from zope.pluggableauth import PluggableAuthentication
from waeup.kofa.authentication import setup_authentication
from waeup.kofa.datacenter import DataCenter
from waeup.kofa.mandates.container import MandatesContainer
from waeup.kofa.interfaces import (
    IUniversity, IKofaPluggable, IObjectUpgradeEvent, IJobManager,
    VIRT_JOBS_CONTAINER_NAME)
from waeup.kofa.userscontainer import UsersContainer
from waeup.kofa.utils.logger import Logger
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.configuration import ConfigurationContainer


class University(grok.Application, grok.Container, Logger):
    """A university.
    """
    grok.implements(IUniversity)

    # Setup authentication for this app. Note: this is only
    # initialized, when a new instance of this app is created.
    grok.local_utility(
        PluggableAuthentication, provides=IAuthentication,
        setup=setup_authentication,)

    def __init__(self, *args, **kw):
        super(University, self).__init__(*args, **kw)
        self.setup()
        return

    def setup(self):
        """Setup some hard-wired components.

        Create local datacenter, containers for users, students and
        the like.
        """
        from waeup.kofa.students.container import StudentsContainer
        from waeup.kofa.hostels.container import HostelsContainer

        self['users'] = UsersContainer()
        self['datacenter'] = DataCenter()
        self['students'] = StudentsContainer()
        self['configuration'] = ConfigurationContainer()
        self['hostels'] = HostelsContainer()
        self['mandates'] = MandatesContainer()
        self._createPlugins()

    def _createPlugins(self):
        """Create instances of all plugins defined somewhere.
        """
        for name, plugin in getUtilitiesFor(IKofaPluggable):
            plugin.setup(self, name, self.logger)
        return

    def traverse(self, name):
        if name == VIRT_JOBS_CONTAINER_NAME:
            return getUtility(IJobManager)
        return None

    def updatePlugins(self):
        """Lookup an arbitrarily selected set of plugins and call their
        `update()` method to upgrade Kofa's database since software version 1.4
        (2016-01-14).

        XXX: This method does not run all plugins registered.

        XXX: Tests for this method were disabled.
        """
        for name in ['faculties', 'departments', 'certificates',
                     'certcourses', 'courses', 'hostels',
                     'site-pluggable-auth']:
            getUtility(IKofaPluggable, name=name).update(
                self, name, self.logger)
        return
attrs_to_fields(University)


class ObjectUpgradeEvent(ObjectEvent):
    """An event fired, when datacenter storage moves.
    """
    grok.implements(IObjectUpgradeEvent)


@grok.subscribe(University, grok.IObjectAddedEvent)
def handle_university_added(app, event):
    """If a university is added, a message is logged.
    """
    app.logger.info('University `%s` added.' % getattr(app, '__name__', None))
    return
