## $Id: views.py 7196 2011-11-25 07:44:52Z henrik $
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
"""Views for images and the like.
"""
import mimetypes
import grok
from hurry.file.interfaces import IHurryFile

class HurryFileView(grok.View):
    """A view for hurry files stored in the ZODB.

    Normally these files cannot be 'browsed' but with a view we can
    stream them to the browser. We only have to set the appropriate
    MIME type, which happens in the `render` method.
    """

    grok.name('index.html')
    grok.context(IHurryFile)

    def render(self):
        """Output the data of context.

        Beside this we set the output MIME type according to the
        context's filename.
        """
        content_type, encoding = mimetypes.guess_type(
            self.context.filename.lower())
        if content_type is not None:
            self.response.setHeader('Content-Type', content_type)
        fd = self.context.file
        contents = fd.read()
        fd.close()
        return contents
