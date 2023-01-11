## $Id: interfaces.py 13235 2015-08-28 07:49:07Z henrik $
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
from zope.interface import Attribute, Interface
from zope import schema
from waeup.kofa.interfaces import (
    IKofaObject, validate_id, validate_html,
    ContextualDictSourceFactoryBase)
from waeup.kofa.interfaces import MessageFactory as _


class IDocumentsContainer(IKofaObject):
    """A container for all kind of document objects.
    """

    def addDocument(document):
        """Add a document.
        """


class IDocument(IKofaObject):
    """A base representation of documents.
    """
    history = Attribute('Object history, a list of messages')
    state = Attribute('Workflow state of a document')
    class_name = Attribute('Name of the document class')
    local_roles = Attribute('List of local role names')
    translated_class_name = Attribute('Translatable class name of a document')
    translated_state = Attribute('Translatable workflow state of a document')
    formatted_transition_date = Attribute(
        'Last transition formatted date string')
    form_fields_interface = Attribute(
        'Interface which is used in forms for grok.AutoFields')

    document_id = schema.TextLine(
        title = _(u'Document Id'),
        required = True,
        constraint=validate_id,
        )

    title = schema.TextLine(
        title = _(u'Document Title'),
        required = True,
        )

class IPublicDocument(IDocument):
    """A base representation of public documents.
    """

    def writeLogMessage(view, message):
        """Add an INFO message to main.log.
        """

class IPDFDocument(IPublicDocument):
    """A base representation of PDF documents.
    """

    filenames = Attribute('Tuple of filenames; only one filename recommended')

class IHTMLDocument(IPublicDocument):
    """A base representation of HTML documents.
    """

    html_dict = Attribute(
        'Content as language dictionary with values in HTML format')

    html_multilingual = schema.Text(
        title = _(u'Multilingual content in HTML format'),
        required = False,
        constraint=validate_html,
        )

class IRESTDocument(IPublicDocument):
    """A base representation of REST documents.
    """

    html_dict = Attribute(
        'Content as language dictionary with values in HTML format')

    rest_multilingual = schema.Text(
        title = _(u'Multilingual content in REST (reStructuredText) format'),
        required = False,
        )


class IDocumentsUtils(Interface):
    """A collection of methods which are subject to customization.
    """

