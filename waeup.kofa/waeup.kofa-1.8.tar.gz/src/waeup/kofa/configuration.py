## $Id: configuration.py 13118 2015-06-30 07:14:17Z henrik $
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
Components for portal configuration.
"""
import grok
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from waeup.kofa.interfaces import (
    ISessionConfiguration, IConfigurationContainer, ISessionConfigurationAdd,
    academic_sessions_vocab)
from waeup.kofa.utils.helpers import attrs_to_fields

class ConfigurationContainer(grok.Container):
    """
    The node containing the session configuration models
    """

    grok.implements(IConfigurationContainer)

    def addSessionConfiguration(self, sessionconfiguration):
        """Add a session configuration object.
        """
        if not ISessionConfiguration.providedBy(sessionconfiguration):
            raise TypeError(
                'ConfigurationContainers contain only '
                'ISessionConfiguration instances')
        code = unicode(sessionconfiguration.academic_session)
        self[code] = sessionconfiguration
        return

ConfigurationContainer = attrs_to_fields(ConfigurationContainer)

class SessionConfiguration(grok.Model):
    """
    Session configuration model
    """

    grok.implements(ISessionConfiguration, ISessionConfigurationAdd)

    def getSessionString(self):
        """Return the session string from the vocabulary.
        """
        return academic_sessions_vocab.getTerm(self.academic_session).title

SessionConfiguration = attrs_to_fields(SessionConfiguration)

class SessionConfigurationFactory(grok.GlobalUtility):
    """A factory for session configuration objects.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.SessionConfiguration')
    title = u"Create a new session configuration object.",
    description = u"This factory instantiates new session configurations."

    def __call__(self, *args, **kw):
        return SessionConfiguration(*args, **kw)

    def getInterfaces(self):
        return implementedBy(SessionConfiguration)
