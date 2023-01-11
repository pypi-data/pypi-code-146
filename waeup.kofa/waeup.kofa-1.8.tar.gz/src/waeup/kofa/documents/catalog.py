## $Id: catalog.py 13134 2015-07-03 10:19:55Z henrik $
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
"""Components to help cataloging and searching documents.
"""
import grok
from waeup.kofa.interfaces import IUniversity
from waeup.kofa.documents.interfaces import IDocument

class DocumentsCatalog(grok.Indexes):
    """A catalog for all documents.
    """
    grok.site(IUniversity)
    grok.name('documents_catalog')
    grok.context(IDocument)

    document_id = grok.index.Field(attribute='document_id')
    state = grok.index.Field(attribute='state')
