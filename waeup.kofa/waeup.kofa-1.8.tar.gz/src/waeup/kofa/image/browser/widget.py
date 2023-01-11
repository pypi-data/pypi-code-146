## $Id: widget.py 7819 2012-03-08 22:28:46Z henrik $
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
"""Image file widgets.
"""
import os
from waeup.kofa.image import KofaImageFile
from hurry.file.browser.widget import (
    EncodingFileWidget, DownloadWidget, FakeFieldStorage)
from hurry.file.interfaces import IFileRetrieval
from zope.app.form.browser.textwidgets import escape
from zope.app.form.browser.widget import renderElement
from zope.app.form.interfaces import ConversionError
from zope.component import queryUtility
from zope.publisher.browser import FileUpload


class EncodingImageFileWidget(EncodingFileWidget):
    """A hurry.file widget that stores images.

    This is an upload widget suitable for edit forms and the like.
    """
    #: We can set a basename for the image to be rendered.
    #: This will result in <img> links like <img src='.../<basename>.jpg' />
    image_basename = None

    def _toFieldValue(self, (input, file_id)):
        # we got no file upload input
        if not input:
            # if we got a file_id, then retrieve file and return it
            if file_id:
                return self._retrieveFile(file_id)
            # no file upload input nor file id, so return missing value
            return self.context.missing_value
        # read in file from input
        try:
            seek = input.seek
            read = input.read
        except AttributeError, e:
            raise ConversionError('Form input is not a file object', e)

        seek(0)
        data = read()

        if data:
            retrieval = queryUtility(IFileRetrieval)
            if retrieval is not None:
                seek(0)
                return retrieval.createFile(input.filename, input)
            return KofaImageFile(input.filename, data)
        else:
            return self.context.missing_value

    def _toFormValue(self, value):
        if value == self.context.missing_value:
            return self._missing
        data = value.file.read()
        return FileUpload(FakeFieldStorage(
                value.filename.encode('UTF-8'), data))

    def __call__(self):
        value = self._getFormValue()
        if value:
            file_id = self._setFile(value)
        else:
            file_id = None
        result = u''
        options = dict(
            type=self.type,
            name=self.name,
            id=self.name,
            cssClass=self.cssClass,
            size=self.displayWidth,
            extra=self.extra,)
        if self.displayMaxWidth:
            options.update(maxlength=self.displayMaxWidth)
        if value:
            filename = value.filename
            if self.image_basename is not None:
                filename = self.image_basename + os.path.splitext(filename)[-1]
            result = renderElement(
                'img',
                src=filename,
                )
            result += renderElement('br')
        result += renderElement(self.tag, **options)
        if file_id is not None:
            if value:
                result += ' (%s)' % value.filename
            result += renderElement(
                'input',
                type='hidden',
                name=self.name + '.file_id',
                id=self.name + '.file_id',
                value=file_id,
                )
        return result

    def _setFile(self, file):
        """Store away uploaded file (FileUpload object).

        Returns file_id identifying file.
        """
        # if there was no file input and there was a file_id already in the
        # input, reuse this for next request
        if not self.request.get(self.name):
            file_id = self.request.get(self.name + '.file_id')
            if file_id is not None:
                return file_id
        # otherwise, stuff filedata away in session, making a new file_id
        if file == self.context.missing_value:
            return None
        return self._storeFile(file)

    def _storeFile(self, file_upload):
        # filenames are normally in unicode encoding, while the contents
        # are byte streams. We turn the filename into a bytestream.
        retrieval = queryUtility(IFileRetrieval)
        if retrieval is not None:
            file_upload.seek(0)
            file_obj = retrieval.createFile(file_upload.filename, file_upload)
            data = file_obj.data
        else:
            data = file_upload.read()
        data = '%s\n%s' % (str(file_upload.filename), data)
        return data.encode('base64')[:-1]

    def _retrieveFile(self, file_id):
        data = file_id.decode('base64')
        filename, filedata = data.split('\n', 1)
        return KofaImageFile(filename, filedata)

class ThumbnailWidget(DownloadWidget):
    """An image file widget that displays the data as thumbnail.

    XXX: give some reason to name this a _thumbnail_ widget.
    """

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return renderElement(
                u'div',
                contents=u'Download not available')
        filename = escape(value.filename)
        return renderElement(
            u'img',
            src=filename,
            contents=None)
