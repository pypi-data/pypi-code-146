## $Id: container.py 13962 2016-06-21 06:07:30Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
Containers which contain mandate objects.
"""
import grok
from datetime import datetime
from grok import index
from waeup.kofa.interfaces import IKofaPluggable
from waeup.kofa.mandates.interfaces import IMandatesContainer, IMandate

class MandatesContainer(grok.Container):
    """This is a container for all kind of mandates.
    """
    grok.implements(IMandatesContainer)
    grok.provides(IMandatesContainer)

    @property
    def count(self):
        """Count active and expired mandates.
        """
        now = datetime.utcnow()
        total = len(self)
        expired = len([i for i in self.values() if i.expires < now])
        active = total - expired
        return active, expired, total

    def addMandate(self, mandate):
        if not IMandate.providedBy(mandate):
            raise TypeError(
                'MandateContainers contain only IMandate instances')
        self[mandate.mandate_id] = mandate
        return

    def removeExpired(self):
        """Remove all expired mandates.
        """
        num_deleted = 0
        keys = list(self.keys())
        for mandate in keys:
            if self[mandate].expires < datetime.utcnow():
                del self[mandate]
                num_deleted += 1
        grok.getSite().logger.info('%s mandates purged' % num_deleted)
        return num_deleted

class MandatesPlugin(grok.GlobalUtility):
    """A plugin that creates container for mandates inside a university.
    """
    grok.implements(IKofaPluggable)
    grok.name('mandates')

    def setup(self, site, name, logger):
        if 'mandates' in site.keys():
            logger.warn('Could not create container for mandates in Kofa.')
            return
        site['mandates'] = MandatesContainer()
        logger.info('Container for mandates created')
        return

    def update(self, site, name, logger):
        if not 'mandates' in site.keys():
            self.setup(site, name, logger)