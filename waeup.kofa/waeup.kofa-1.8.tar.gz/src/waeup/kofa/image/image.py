## $Id: image.py 7819 2012-03-08 22:28:46Z henrik $
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
"""
Components for handling image files.
"""
from hurry.file import HurryFile
from hurry.file.interfaces import IFileRetrieval
from zope.component import getUtility
from zope.interface import implements
from waeup.kofa.image.interfaces import IKofaImageFile

class KofaImageFile(HurryFile):
    """A file prepared for storing image files.

    This file type is built upon :class:`hurry.file.HurryFile` but
    implements a derived marker interface to distuingish it from
    regular hurry files.

    To create a :class:`KofaImageFile` you should use
    :func:`createKofaImageFile`.
    """
    implements(IKofaImageFile)

    def __ne__(self, other):
        # This was wrongly implemented in the base class
        try:
            return (self.filename != other.filename or
                    self.data != other.data)
        except AttributeError:
            return True

def createKofaImageFile(filename, f):
    retrieval = getUtility(IFileRetrieval)
    return retrieval.createFile(filename, f)
