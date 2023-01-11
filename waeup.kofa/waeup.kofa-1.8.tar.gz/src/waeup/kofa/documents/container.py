## $Id: container.py 12438 2015-01-11 08:27:37Z henrik $
##
## Copyright (C) 2014 Uli Fouquet & Henrik Bettermann
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
Containers which contain document objects.
"""
import grok
from grok import index
from waeup.kofa.interfaces import IKofaPluggable
from waeup.kofa.documents.interfaces import IDocumentsContainer, IDocument
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.utils.logger import Logger

class DocumentsContainer(grok.Container, Logger):
    """This is a container for all kind of documents.
    """
    grok.implements(IDocumentsContainer)
    grok.provides(IDocumentsContainer)


    def addDocument(self, document):
        if not IDocument.providedBy(document):
            raise TypeError(
                'DocumentsContainers contain only IDocument instances')
        self[document.document_id] = document
        return

DocumentsContainer = attrs_to_fields(DocumentsContainer)

class DocumentsPlugin(grok.GlobalUtility):
    """A plugin that creates container for documents inside a company.
    """
    grok.implements(IKofaPluggable)
    grok.name('documents')

    def setup(self, site, name, logger):
        if 'documents' in site.keys():
            logger.warn('Could not create container for documents.')
            return
        site['documents'] = DocumentsContainer()
        logger.info('Container for documents created')
        return

    def update(self, site, name, logger):
        if not 'documents' in site.keys():
            self.setup(site, name, logger)
