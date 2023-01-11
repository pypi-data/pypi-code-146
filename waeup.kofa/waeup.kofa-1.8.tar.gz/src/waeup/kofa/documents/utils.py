## $Id: utils.py 12438 2015-01-11 08:27:37Z henrik $
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
"""General helper functions and utilities for the documents.
"""
import grok
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.documents.workflow import (
    CREATED, PUBLISHED)
from waeup.kofa.documents.interfaces import IDocumentsUtils


class DocumentsUtils(grok.GlobalUtility):
    """A collection of methods subject to customization.
    """
    grok.implements(IDocumentsUtils)

    TRANSLATED_DOCUMENT_STATES = {
        CREATED: _('created'),
        PUBLISHED:_('published')
        }

    DOCTYPES_DICT = {
        'PDFDocument': _('PDF Document'),
        'HTMLDocument': _('HTML Document'),
        'RESTDocument': _('REST Document'),
        }

    SELECTABLE_DOCTYPES_DICT = DOCTYPES_DICT