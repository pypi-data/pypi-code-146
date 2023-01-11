## $Id: facultiescontainer.py 14511 2017-02-07 08:33:05Z henrik $
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
import zope.location.location
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from waeup.kofa.interfaces import IKofaPluggable
from waeup.kofa.university.interfaces import IFacultiesContainer, IFaculty
from waeup.kofa.utils.batching import VirtualExportJobContainer

class VirtualFacultiesExportJobContainer(VirtualExportJobContainer):
    """A virtual export job container for the faculties container.
    """

class FacultiesContainer(grok.Container):
    """See interfaces for description.
    """
    grok.implements(IFacultiesContainer)

    def traverse(self, name):
        if name == 'exports':
            # create a virtual exports container and return it
            container = VirtualFacultiesExportJobContainer()
            zope.location.location.located(container, self, 'exports')
            return container
        return None

    def addFaculty(self, faculty):
        if not IFaculty.providedBy(faculty):
            raise TypeError(
                'FacultiesContainers contain only IFaculty instances')
        self[faculty.code] = faculty
        return

class FacultiesContainerFactory(grok.GlobalUtility):
    """A factory for faculty containers.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.FacultiesContainer')
    title = u"Create a new facultiescontainer.",
    description = u"This factory instantiates new containers for faculties."

    def __call__(self, *args, **kw):
        return FacultiesContainer(*args, **kw)

    def getInterfaces(self):
        return implementedBy(FacultiesContainer)

class AcademicsPlugin(grok.GlobalUtility):
    """A plugin that creates container for faculties inside a university.
    """
    grok.implements(IKofaPluggable)
    grok.name('academics')

    def setup(self, site, name, logger):
        if 'faculties' in site.keys():
            logger.warn('Could not create container for faculties in Kofa.')
            return
        site['faculties'] = FacultiesContainer()
        logger.info('Container for faculties created')
        return

    def update(self, site, name, logger):
        if not 'faculties' in site.keys():
            self.setup(site, name, logger)

