## $Id: fileviewlets.py 12448 2015-01-12 11:00:55Z henrik $
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

import os
import grok
from zope.component import getUtility
from zope.interface import Interface
from waeup.kofa.interfaces import (
    IKofaObject, IExtFileStore, IFileStoreNameChooser)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.browser import DEFAULT_IMAGE_PATH
from waeup.kofa.utils.helpers import (
    string_from_bytes, file_size, get_fileformat)
from waeup.kofa.browser.layout import (
    default_filedisplay_template,
    default_fileupload_template)

ALLOWED_FILE_EXTENSIONS = ('jpg', 'png', 'pdf', 'tif', 'fpm')

grok.context(IKofaObject)  # Make IKofaObject the default context

def handle_file_delete(context, view, download_name):
    """Handle deletion of file.

    """
    store = getUtility(IExtFileStore)
    store.deleteFileByContext(context, attr=download_name)
    context.writeLogMessage(view, 'deleted: %s' % download_name)
    view.flash(_('${a} deleted.', mapping={'a': download_name}))
    return


def handle_file_upload(upload, context, view, max_size, download_name=None):
    """Handle upload of file.

    Returns `True` in case of success or `False`.

    Please note that file pointer passed in (`upload`) most probably
    points to end of file when leaving this function.
    """
    # Check some file requirements first
    size = file_size(upload)
    if size > max_size:
        view.flash(_('Uploaded file is too big.'), type="danger")
        return False
    upload.seek(0)  # file pointer moved when determining size
    dummy,ext = os.path.splitext(upload.filename)
    # fpm files are expected to be fingerprint minutiae, file
    # format is not yet checked
    if ext == '.fpm':
        file_format = 'fpm'
    else:
        file_format = get_fileformat(None, upload.read(512))
        upload.seek(0)  # same here
    if file_format is None:
        view.flash(_('Could not determine file type.'), type="danger")
        return False
    basename, expected_ext = os.path.splitext(download_name)
    if expected_ext:
        if '.' + file_format != expected_ext:
            view.flash(_('${a} file format expected.',
                mapping={'a': expected_ext[1:]}), type="danger")
            return False
    else:
        if not file_format in ALLOWED_FILE_EXTENSIONS:
            view.flash(
                _('Only the following extensions are allowed: ${a}',
                mapping={'a': ', '.join(ALLOWED_FILE_EXTENSIONS)}),
                type="danger")
            return False
        download_name += '.' + file_format
    store = getUtility(IExtFileStore)
    file_id = IFileStoreNameChooser(context).chooseName(attr=download_name)
    store.createFile(file_id, upload)
    context.writeLogMessage(view, 'uploaded: %s (%s)' % (
        download_name,upload.filename))
    view.flash(_('File ${a} uploaded.', mapping={'a': download_name}))
    return True


class FileManager(grok.ViewletManager):
    """Viewlet manager for uploading files, preferably scanned images.
    """
    grok.name('files')


class FileDisplay(grok.Viewlet):
    """Base file display viewlet.
    """
    grok.baseclass()
    grok.viewletmanager(FileManager)
    template = default_filedisplay_template
    label = _(u'File')
    title = _(u'Scan')

    @property
    def download_filename(self):
        return self.download_name

    @property
    def file_exists(self):
        image = getUtility(IExtFileStore).getFileByContext(
            self.context, attr=self.download_name)
        if image:
            return True
        else:
            return False


class FileUpload(FileDisplay):
    """Base upload viewlet.
    """
    grok.baseclass()
    grok.viewletmanager(FileManager)
    template = default_fileupload_template
    tab_redirect = '#tab2-top'
    mus = 1024 * 150
    upload_button =_('Upload selected file')
    delete_button = _('Delete')

    @property
    def show_viewlet(self):
        return True

    @property
    def input_name(self):
        return "%s" % self.__name__

    def update(self):
        self.max_upload_size = string_from_bytes(self.mus)
        delete_button = self.request.form.get(
            'delete_%s' % self.input_name, None)
        upload_button = self.request.form.get(
            'upload_%s' % self.input_name, None)
        if delete_button:
            handle_file_delete(
                context=self.context, view=self.view,
                download_name=self.download_name)
            self.view.redirect(
                self.view.url(
                    self.context, self.view.__name__) + self.tab_redirect)
            return
        if upload_button:
            upload = self.request.form.get(self.input_name, None)
            if upload:
                # We got a fresh upload
                handle_file_upload(upload,
                    self.context, self.view, self.mus, self.download_name)
                self.view.redirect(
                    self.view.url(
                        self.context, self.view.__name__) + self.tab_redirect)
            else:
                self.view.flash(_('No local file selected.'), type="danger")
                self.view.redirect(
                    self.view.url(
                        self.context, self.view.__name__) + self.tab_redirect)
        return


class Image(grok.View):
    """Renders images.
    """
    grok.baseclass()

    @property
    def download_filename(self):
        return self.download_name

    def render(self):
        # A filename chooser turns a context into a filename suitable
        # for file storage.
        image = getUtility(IExtFileStore).getFileByContext(
            self.context, attr=self.download_name)
        if image is None:
            # show placeholder image
            self.response.setHeader('Content-Type', 'image/jpeg')
            return open(DEFAULT_IMAGE_PATH, 'rb').read()
        dummy,ext = os.path.splitext(image.name)
        if ext == '.jpg':
            self.response.setHeader('Content-Type', 'image/jpeg')
        elif ext == '.fpm':
            self.response.setHeader('Content-Type', 'application/binary')
        elif ext == '.png':
            self.response.setHeader('Content-Type', 'image/png')
        elif ext == '.tif':
            self.response.setHeader('Content-Type', 'image/tiff')
        elif ext == '.pdf':
            self.response.setHeader('Content-Type', 'application/pdf')
            self.response.setHeader('Content-Disposition',
                'attachment; filename="%s.pdf' % self.download_filename)
        return image
