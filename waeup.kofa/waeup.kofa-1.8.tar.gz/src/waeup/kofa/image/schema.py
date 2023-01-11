## $Id: schema.py 7819 2012-03-08 22:28:46Z henrik $
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
"""Image file schemas.
"""
from zope.interface import implements
from zope.schema import MinMaxLen
from zope.schema.interfaces import TooBig, TooSmall
from hurry.file.schema import File
from waeup.kofa.image.interfaces import IImageFile
from waeup.kofa.image.image import KofaImageFile

class MinMaxSize(object):
    """Expresses constraints on the size of an object.

    The 'size' of an object is determined by its `size` method or
    attribute. If an object has no such 'size' then it cannot be
    validated by this mixin.

    Please do not confuse `MinMaxSize` with `MinMaxLen`, for instance
    supported by ordinary text fields. These test on ``len(obj)``
    which is not necessary possible for file-like objects.

    Therefore we distinguish 'size' from 'len' here.
    """
    min_size = None
    max_size = None

    def __init__(self, min_size=None, max_size=None, **kw):
        self.min_size = min_size
        self.max_size = max_size
        super(MinMaxSize, self).__init__(**kw)

    def _validate(self, value):
        super(MinMaxSize, self)._validate(value)
        if self.max_size is not None and value.size > self.max_size:
            raise TooBig(
                value.filename,
                "%s bytes (max: %s bytes)" % (value.size, self.max_size))

        if self.min_size is not None and value.size < self.min_size:
            raise TooSmall(
                value.filename,
                "%s bytes (min: %s bytes)" % (value.size, self.min_size))

    
class ImageFile(MinMaxSize, File):
    """An image file field.

    Suitable for interfaces that wish to store image files in an
    attribute.

    This field type supports `MinMaxSize` so that you can set
    `min_size` or `max_size` for all `ImageFile` fields in your
    interfaces like this:

      class MyInterface(Interface):
         image = ImageFile(
             title = u'The image',
             description = u'The nice image',
             max_size = 1024 * 10,
             )

    to restrict the file size of stored images to 10 KBytes.

    By default no such restriction is set.
    """
    implements(IImageFile)

    _type = KofaImageFile
