## $Id: test_facultiescontainer.py 7819 2012-03-08 22:28:46Z henrik $
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

# Tests for FacultiesContainer.
import logging
import unittest
from StringIO import StringIO
from zope.interface.verify import verifyObject, verifyClass
from waeup.kofa.testing import FunctionalTestCase, FunctionalLayer
from waeup.kofa.university.interfaces import IFacultiesContainer
from waeup.kofa.university import FacultiesContainer
from waeup.kofa.university.facultiescontainer import AcademicsPlugin

class FakeLogger(object):

    _stream = None

    def get_logger(self):
        logger = logging.getLogger('test')
        logger.propagate = False
        self._stream = StringIO()
        self.handler = logging.StreamHandler(self._stream)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.handler)
        return logger

    def close(self, logger):
        # Remove handler from logger
        handler = self.handler
        if handler not in logger.handlers:
            return
        del logger.handlers[logger.handlers.index(handler)]
        return

    def get_messages(self):
        self._stream.seek(0)
        result = self._stream.read()
        self._stream.seek(0, 2) # Seek to end of stream
        return result

class FacultiesContainerTests(unittest.TestCase):

    def test_ifaces(self):
        container = FacultiesContainer()
        self.assertTrue(verifyClass(IFacultiesContainer, FacultiesContainer))
        self.assertTrue(verifyObject(IFacultiesContainer, container))

class AcademicsPluginTests(unittest.TestCase):

    def setUp(self):
        self._logger_factory = FakeLogger()
        self.logger = self._logger_factory.get_logger()

    def tearDown(self):
        self._logger_factory.close(self.logger)

    def test_setup(self):
        site = dict()
        logger = self.logger
        plugin = AcademicsPlugin()
        plugin.setup(site, 'testsite', logger)
        self.assertTrue('faculties' in site.keys())
        self.assertTrue(isinstance(site['faculties'], FacultiesContainer))
        self.assertEqual(
            self._logger_factory.get_messages(),
            'Container for faculties created\n'
            )

    def test_setup_already_set_up(self):
        site = dict(faculties=object())
        logger = self.logger
        plugin = AcademicsPlugin()
        plugin.setup(site, 'testsite', logger)
        self.assertTrue('faculties' in site.keys())
        self.assertEqual(
            self._logger_factory.get_messages(),
            'Could not create container for faculties in Kofa.\n'
            )

    def test_update(self):
        site = dict()
        logger = self.logger
        plugin = AcademicsPlugin()
        plugin.update(site, 'testsite', logger)
        self.assertTrue('faculties' in site.keys())
        self.assertTrue(isinstance(site['faculties'], FacultiesContainer))
        self.assertEqual(
            self._logger_factory.get_messages(),
            'Container for faculties created\n'
            )

    def test_update_already_set_up(self):
        site = dict(faculties=object())
        logger = self.logger
        plugin = AcademicsPlugin()
        plugin.update(site, 'testsite', logger)
        self.assertTrue('faculties' in site.keys())
        self.assertEqual(
            self._logger_factory.get_messages(), '')
