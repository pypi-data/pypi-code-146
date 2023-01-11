## $Id: test_objecthistory.py 9126 2012-08-30 08:11:58Z henrik $
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
"""Test object history.
"""
import grok
import shutil
import tempfile
from persistent.list import PersistentList
from zope.interface.verify import verifyObject, verifyClass
from zope.security.management import newInteraction, endInteraction
from zope.security.testing import Principal, Participation
from waeup.kofa.app import University
from waeup.kofa.interfaces import IObjectHistory, IKofaObject
from waeup.kofa.testing import FunctionalTestCase, FunctionalLayer
from waeup.kofa.objecthistory import ObjectHistory

class SampleObject(grok.Model):
    grok.implements(IKofaObject)
    pass

class ObjectHistoryTests(FunctionalTestCase):
    # Tests for helpers like get_access_code, disable_accesscode, ...

    layer = FunctionalLayer

    def setUp(self):
        super(ObjectHistoryTests, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.obj = SampleObject()

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(ObjectHistoryTests, self).tearDown()
        endInteraction() # Just in case, one is still lingering around

    def test_iface(self):
        # ObjectHistory class and instances provide the promised ifaces
        hist = IObjectHistory(self.obj)
        assert verifyObject(IObjectHistory, hist)
        assert verifyClass(IObjectHistory, ObjectHistory)

    def test_adapter(self):
        # We can get a history by adapting to IObjectHistory
        result = IObjectHistory(self.obj)
        assert isinstance(result, ObjectHistory)

    def test_add_messages(self):
        # We can add a message
        hist = IObjectHistory(self.obj)
        assert hist.messages == []
        hist.addMessage('blah')
        assert 'blah' in ''.join(hist.messages)

    def test_add_messages_timestamp_and_user(self):
        # Messages added get a timestamp and the current user
        hist = IObjectHistory(self.obj)
        hist.addMessage('blah')
        result = ''.join(hist.messages)
        self.assertMatches('<YYYY-MM-DD hh:mm:ss> UTC - blah by system', result)

    def test_add_messages_existing_principal(self):
        principal = Principal('bob')
        principal.title = 'Bob'
        newInteraction(Participation(principal)) # set current user
        hist = IObjectHistory(self.obj)
        hist.addMessage('blah')
        result = ''.join(hist.messages)
        self.assertMatches('<YYYY-MM-DD hh:mm:ss> UTC - blah by Bob', result)

    def test_modify_messages(self):
        principal = Principal('bob')
        principal.title = 'Bob'
        newInteraction(Participation(principal)) # set current user
        hist = IObjectHistory(self.obj)
        hist.addMessage('blah')
        hist.modifyMessages('blah', 'blow')
        result = ''.join(hist.messages)
        self.assertMatches('<YYYY-MM-DD hh:mm:ss> UTC - blow by Bob', result)

    def test_remove_message(self):
        principal = Principal('bob')
        principal.title = 'Bob'
        newInteraction(Participation(principal)) # set current user
        hist = IObjectHistory(self.obj)
        hist.addMessage('blah')
        hist.addMessage('blow')
        self.assertEqual(len(hist._getMessages()), 2)
        result = ' '.join(hist.messages)
        self.assertTrue('blah by Bob' in result)
        self.assertTrue('blow by Bob' in result)
        success, text = hist.removeMessage('xyz')
        self.assertFalse(success)
        self.assertEqual(text, 'Not a number')
        success, text = hist.removeMessage(100)
        self.assertFalse(success)
        self.assertEqual(text, 'Number out of range')
        success, text = hist.removeMessage(1)
        self.assertTrue(success)
        self.assertMatches('<YYYY-MM-DD hh:mm:ss> UTC - blow by Bob', text)
        self.assertEqual(len(hist.messages), 1)
        result = ' '.join(hist.messages)
        self.assertFalse('blow by Bob' in result)

    def test_messages(self):
        # we get messages as a persistent list of strings
        hist = IObjectHistory(self.obj)
        hist.addMessage('foo')
        hist.addMessage('bar')
        assert isinstance(hist.messages, PersistentList)
        assert 'foo' in hist.messages[0]
        assert 'bar' in hist.messages[1]
