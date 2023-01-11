##
## test_views.py
## Login : <uli@pu.smp.net>
## Started on  Mon Apr 11 22:45:10 2011 Uli Fouquet
## $Id: test_views.py 7811 2012-03-08 19:00:51Z uli $
## 
## Copyright (C) 2011 Uli Fouquet
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
Test image file views.
"""
import grok
import os
import unittest
from tempfile import mkstemp
from hurry.file import HurryFile
from hurry.file.file import IdFileRetrieval
from hurry.file.interfaces import IFileRetrieval
from waeup.kofa.image.browser.views import HurryFileView
from zope.component import getMultiAdapter, provideUtility
from zope.publisher.browser import TestRequest

# List of expected input-ouput: (name, expected-mimetype)
CONTENT_TYPES = (
    ('jpg', 'image/jpeg'),
    )

class ImageBrowserViewsLayer(object):
    """A layer that registers all components in
       `waeup.kofa.image.browser.views` module.
    """
    @classmethod
    def setUp(cls):
        grok.testing.grok('waeup.kofa.image.browser.views')

    @classmethod
    def tearDown(cls):
        pass

class HurryFileViewTestCase(unittest.TestCase):

    layer = ImageBrowserViewsLayer

    def setUp(self):
        # Create a bunch of files and `HurryFile` objects pointing to
        # them.  Also create a dict of content types expected. Each of
        # the dicts indexed by the name of the above CONTENT_TYPES.
        self.filenames = dict()
        self.files = dict()
        self.content_types = dict()
        for name, content_type in CONTENT_TYPES:
            fd, filename = mkstemp(suffix='.%s' % name)
            self.filenames[name] = filename
            self.files[name] = HurryFile(os.path.basename(filename), fd)
            self.content_types[name] = content_type
        self.request = TestRequest()
        # Now create the most simple fileretrieval possible
        retrieval = IdFileRetrieval()
        provideUtility(retrieval, IFileRetrieval)
        return

    def tearDown(self):
        # Remove all temporary files.
        for filename in self.filenames.values():
            os.unlink(filename)
        return

    def test_mimetype_jpeg(self):
        # Create a view of some JPEG file, call that view and see what
        # mimetype we get.
        view = getMultiAdapter(
            (self.files['jpg'], self.request), name='index.html'
            )
        view() # Call the view in order to set the headers...
        response = self.request.response
        content_type = response.getHeader('Content-Type')
        self.assertEqual(
            content_type, self.content_types['jpg']
            )
