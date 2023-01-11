## $Id: document.py 13134 2015-07-03 10:19:55Z henrik $
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
These are the public documents.
"""
import os
import grok
from grok import index
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from zope.event import notify
from zope.component import getUtility
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from zope.i18n import translate

from waeup.kofa.image import KofaImageFile
from waeup.kofa.imagestorage import DefaultFileStoreHandler
from waeup.kofa.interfaces import (
    IKofaUtils, IObjectHistory,
    IFileStoreNameChooser, IFileStoreHandler, IExtFileStore)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.helpers import attrs_to_fields, get_current_principal
from waeup.kofa.documents.interfaces import (
    IDocument, IPublicDocument, IDocumentsUtils,
    IPDFDocument, IHTMLDocument, IRESTDocument)


@grok.subscribe(IDocument, grok.IObjectRemovedEvent)
def handle_document_removed(document, event):
    store = getUtility(IExtFileStore)
    for filename in document.filenames:
        store.deleteFileByContext(document, attr=filename)
    return


class Document(grok.Container):
    """This is a document.
    """
    grok.implements(IDocument)
    grok.provides(IDocument)
    grok.baseclass()

    form_fields_interface = None

    # Kofa can store any number of files per Document object.
    # However, we highly recommend to associate and store
    # only one file per Document object. Thus the following
    # tuple should contain only a single filename string.
    filenames = ()

    local_roles = [
        'waeup.local.DocumentManager',
        ]

    state = None
    translated_state = None
    translated_class_name = None

    @property
    def history(self):
        history = IObjectHistory(self)
        return history

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def formatted_transition_date(self):
        try:
            return self.history.messages[-1].split(' - ')[0]
        except IndexError:
            return

class PublicDocumentBase(Document):
    """This is a public document baseclass.
    """
    grok.implements(IPublicDocument)
    grok.provides(IPublicDocument)
    grok.baseclass()

    @property
    def state(self):
        state = IWorkflowState(self).getState()
        return state

    @property
    def translated_state(self):
        try:
            TRANSLATED_STATES = getUtility(
                IDocumentsUtils).TRANSLATED_DOCUMENT_STATES
            return TRANSLATED_STATES[self.state]
        except KeyError:
            return

    @property
    def translated_class_name(self):
        try:
            DOCTYPES_DICT = getUtility(IDocumentsUtils).DOCTYPES_DICT
            return DOCTYPES_DICT[self.class_name]
        except KeyError:
            return

    def writeLogMessage(self, view, message):
        ob_class = view.__implemented__.__name__.replace('waeup.kofa.','')
        self.__parent__.__parent__.logger.info(
            '%s - %s - %s' % (ob_class, self.__name__, message))
        return


class PDFDocument(PublicDocumentBase):
    """This is a  document for a single pdf upload file.
    """
    grok.implements(IPDFDocument)
    grok.provides(IPDFDocument)

    filenames = ('file.pdf',)

    form_fields_interface = IPDFDocument

PDFDocument = attrs_to_fields(PDFDocument)


class HTMLDocument(PublicDocumentBase):
    """This is a  document to render html-coded text.
    """
    grok.implements(IHTMLDocument)
    grok.provides(IHTMLDocument)

    form_fields_interface = IHTMLDocument

    def __init__(self, *args, **kw):
        super(HTMLDocument, self).__init__(*args, **kw)
        self.html_dict = {}

HTMLDocument = attrs_to_fields(HTMLDocument)


class RESTDocument(PublicDocumentBase):
    """This is a  document to render html-coded text.
    """
    grok.implements(IRESTDocument)
    grok.provides(IRESTDocument)

    form_fields_interface = IRESTDocument

    def __init__(self, *args, **kw):
        super(RESTDocument, self).__init__(*args, **kw)
        self.html_dict = {}

RESTDocument = attrs_to_fields(RESTDocument)


class PDFDocumentFactory(grok.GlobalUtility):
    """A factory for documents.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.PDFDocument')
    title = u"Create a new PDF document.",
    description = u"This factory instantiates new PDF documents."

    def __call__(self, *args, **kw):
        return PDFDocument(*args, **kw)

    def getInterfaces(self):
        return implementedBy(PDFDocument)


class HTMLDocumentFactory(grok.GlobalUtility):
    """A factory for HTML documents.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.HTMLDocument')
    title = u"Create a new HTML document.",
    description = u"This factory instantiates new HTML documents."

    def __call__(self, *args, **kw):
        return HTMLDocument(*args, **kw)

    def getInterfaces(self):
        return implementedBy(HTMLDocument)


class RESTDocumentFactory(grok.GlobalUtility):
    """A factory for REST documents.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.RESTDocument')
    title = u"Create a new REST document.",
    description = u"This factory instantiates new REST documents."

    def __call__(self, *args, **kw):
        return RESTDocument(*args, **kw)

    def getInterfaces(self):
        return implementedBy(RESTDocument)


#: The file id marker for files
DOCUMENT_FILE_STORE_NAME = 'file-document'


class DocumentFileNameChooser(grok.Adapter):
    """A file id chooser for :class:`Document` objects.

    `context` is a :class:`Document` instance.

    The delivered file_id contains the file id marker for
    :class:`Document` objects in the central :class:`DocumentsContainer`.

    This chooser is registered as an adapter providing
    :class:`waeup.kofa.interfaces.IFileStoreNameChooser`.

    File store name choosers like this one are only convenience
    components to ease the task of creating file ids for customer document
    objects. You are nevertheless encouraged to use them instead of
    manually setting up filenames for customer documents.

    .. seealso:: :mod:`waeup.kofa.imagestorage`

    """

    grok.context(IDocument)
    grok.implements(IFileStoreNameChooser)

    def checkName(self, name=None, attr=None):
        """Check whether the given name is a valid file id for the context.

        Returns ``True`` only if `name` equals the result of
        :meth:`chooseName`.

        """
        return name == self.chooseName()

    def chooseName(self, attr, name=None):
        """Get a valid file id for customer document context.

        *Example:*

        For document with id ``d123`` and
        with attr ``nice_image.jpeg`` this chooser would create:

          ``__file-document__nice_image_d123.jpeg``

        meaning that the nice image of this document would be
        stored in the site-wide file storage in path:

          ``nice_image_d123.jpeg``

        """
        basename, ext = os.path.splitext(attr)
        doc_id = self.context.document_id
        marked_filename = '__%s__%s_%s%s' % (
            DOCUMENT_FILE_STORE_NAME,
            basename, doc_id, ext)
        return marked_filename


class DocumentFileStoreHandler(DefaultFileStoreHandler, grok.GlobalUtility):
    """ Document specific file handling.

    This handler knows in which path in a filestore to store document
    files and how to turn this kind of data into some (browsable)
    file object.

    It is called from the global file storage, when it wants to
    get/store a file with a file id starting with
    ``__file-document__`` (the marker string for customer files).

    Like each other file store handler it does not handle the files
    really (this is done by the global file store) but only computes
    paths and things like this.
    """
    grok.implements(IFileStoreHandler)
    grok.name(DOCUMENT_FILE_STORE_NAME)

    def pathFromFileID(self, store, root, file_id):
        """All document files are put in directory ``documents``.
        """
        marker, filename, basename, ext = store.extractMarker(file_id)
        sub_root = os.path.join(root, 'documents')
        return super(DocumentFileStoreHandler, self).pathFromFileID(
            store, sub_root, basename)

    def createFile(self, store, root, filename, file_id, file):
        """Create a browsable file-like object.
        """
        # call super method to ensure that any old files with
        # different filename extension are deleted.
        file, path, file_obj = super(
            DocumentFileStoreHandler, self).createFile(
            store, root,  filename, file_id, file)
        return file, path, KofaImageFile(
            file_obj.filename, file_obj.data)


@grok.subscribe(IDocument, grok.IObjectAddedEvent)
def handle_document_added(document, event):
    """If a document is added the transition create is fired.
    The latter produces a logging message.
    """
    if IWorkflowState(document).getState() is None:
        IWorkflowInfo(document).fireTransition('create')
    return
