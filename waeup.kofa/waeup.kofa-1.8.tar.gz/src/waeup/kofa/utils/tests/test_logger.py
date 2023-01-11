## $Id: test_logger.py 13776 2016-03-11 11:45:01Z henrik $
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

# Tests for waeup.kofa.utils.logger
import logging
import os
import shutil
import tempfile
from zope.component import queryUtility
from zope.component.hooks import setSite, clearSite
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.app import University
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

from waeup.kofa.utils.logger import (
    Logger, ILoggerCollector, LoggerCollector,
    ILogger)

class FakeComponent(object):
    # A component that can use the Logger mixin-class
    def do_something(self):
        self.logger.info('msg from do_something')

class LoggingComponent(FakeComponent, Logger):
    # A component that supports logging by mixing in Logger
    logger_name = 'sample.${sitename}'
    logger_filename = 'sample.log'

class LoggersTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(LoggersTests, self).setUp()
        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        self.dc_root2 = None
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.workdir = tempfile.mkdtemp()
        return

    def tearDown(self):
        super(LoggersTests, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def clear_logger(self, logger):
        del_list = [x for x in logger.handlers]
        for handler in del_list:
            logger.removeHandler(handler)
        return

    def test_iface(self):
        setSite(self.app)
        logger = LoggingComponent()
        verifyClass(ILogger, Logger)
        verifyObject(ILogger, logger)
        return

    def test_logger_prop_no_site(self):
        # If not in a site, we will get a logger without handlers
        logger = Logger().logger
        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(len(logger.handlers), 0)
        return

    def test_site_no_site_name(self):
        # If a site has not name we will get a logger anyway
        setSite(self.app)
        del self.app.__name__
        logger = Logger().logger
        self.assertTrue(logger is not None)
        return

    def test_get_logdir(self):
        # We can get a logdir
        setSite(self.app)
        logger = Logger()
        logdir = logger.logger_get_logdir()
        expected_logdir = os.path.join(
            self.app['datacenter'].storage, 'logs')
        self.assertEqual(logdir, expected_logdir)
        return

    def test_get_logdir_no_site(self):
        # We cannot get a logdir without a site
        logger = Logger()
        logdir = logger.logger_get_logdir()
        self.assertTrue(logdir is None)
        return

    def test_get_logdir_no_datacenter(self):
        # Having a site, is not enough. We also need a datacenter in it.
        setSite(self.app)
        del self.app['datacenter']
        logger = Logger()
        logdir = logger.logger_get_logdir()
        self.assertTrue(logdir is None)
        return

    def test_get_logdir_create_dir(self):
        # If the logdirectory does not exist, we will create it
        setSite(self.app)
        logger = Logger()
        expected_logdir = os.path.join(
            self.app['datacenter'].storage, 'logs')
        if os.path.exists(expected_logdir):
            shutil.rmtree(expected_logdir)
        logdir = logger.logger_get_logdir()
        exists_after = os.path.exists(expected_logdir)
        self.assertEqual(logdir, expected_logdir)
        self.assertTrue(exists_after is True)
        return

    def test_get_logfile(self):
        # We can get a logfile
        setSite(self.app)
        logger = Logger()
        expected_filepath = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        path = logger.logger_get_logfile_path()
        self.assertEqual(expected_filepath, path)
        return

    def test_get_logfile_no_dir(self):
        # We cannot get a logfilepath if there is no dir for it
        setSite(self.app)
        logger = Logger()
        del self.app['datacenter']
        path = logger.logger_get_logfile_path()
        self.assertTrue(path is None)
        return

    def test_setup(self):
        # We can setup a logger.
        mylogger = logging.getLogger('test.sample')
        setSite(self.app)
        logger = Logger()
        result = logger.logger_setup(mylogger)
        self.assertEqual(len(result.handlers), 1)
        handler = result.handlers[0]
        self.assertTrue(result.propagate is False)
        return

    def test_setup_no_site(self):
        # Without a site we get no logger from setup
        mylogger = logging.getLogger('test.sample')
        logger = Logger()
        result = logger.logger_setup(mylogger)
        self.assertTrue(result is None)
        return

    def test_logfile_change(self):
        # When the logfile location changes, logger_logfile_changed can react
        setSite(self.app)
        logger = Logger()
        logger.logger.warn('Warning 1')  # Log something to old logfile
        filename1 = logger.logger.handlers[0].baseFilename
        content1 = open(filename1, 'r').read()
        # Now move the logfile
        self.dc_root2 = tempfile.mkdtemp()
        self.app['datacenter'].setStoragePath(self.dc_root2)
        logger.logger_logfile_changed()
        logger.logger.warn('Warning 2')  # Log something to new logfile
        filename2 = logger.logger.handlers[0].baseFilename
        content2 = open(filename2, 'r').read()
        self.assertTrue('Warning 1' in content1)
        self.assertTrue('Warning 2' in content2)
        self.assertTrue('Warning 1' not in content2)
        self.assertTrue('Warning 2' not in content1)
        self.assertTrue(filename1 != filename2)
        shutil.rmtree(self.dc_root2)
        return

    def test_logger_additional_handlers(self):
        # When we detect additional handlers in a logger, setup anew.
        setSite(self.app)
        logger = Logger()
        old_py_logger = logger.logger
        handler = logging.StreamHandler()
        logger.logger.addHandler(handler)
        old_handler_num = len(old_py_logger.handlers)
        new_py_logger = logger.logger  # This should detect new handler
        new_handler_num = len(new_py_logger.handlers)
        self.assertEqual(new_handler_num, 1)
        self.assertTrue(isinstance(
            new_py_logger.handlers[0],
            logging.handlers.WatchedFileHandler))

class LoggersFunctionalTests(FunctionalTestCase):
    # Check loggers with real components using them

    layer = FunctionalLayer

    def setUp(self):
        super(LoggersFunctionalTests, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.workdir = tempfile.mkdtemp()

        self.app['mycomponent'] = LoggingComponent()
        self.component = self.app['mycomponent']
        setSite(self.app)
        return

    def tearDown(self):
        super(LoggersFunctionalTests, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def test_component_can_get_logger(self):
        # Components can get a logger
        logger = self.component.logger
        self.assertTrue(logger is not None)
        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.name, 'sample.app')
        return

    def test_component_handler_setup(self):
        # handlers of components are setup
        handler = self.component.logger.handlers[0]
        self.assertTrue(isinstance(
                handler, logging.handlers.WatchedFileHandler))
        if hasattr(handler, 'maxBytes'):
            self.assertEqual(handler.maxBytes, MAX_BYTES)
        if hasattr(handler, 'backupCount'):
            self.assertEqual(handler.backupCount, BACKUP_COUNT)
        self.assertTrue(handler.baseFilename.endswith('logs/sample.log'))
        return

    def test_component_can_log(self):
        # a method of some 'loggerized' instance can log like this.
        self.component.logger.setLevel(logging.INFO)
        self.component.do_something()
        handler = logging.getLogger('sample.app').handlers[0]
        logfile = handler.baseFilename
        content = open(logfile, 'rb').read()
        self.assertTrue(content.endswith(' - INFO - system - msg from do_something\n'))
        return

class LoggerCollectorTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(LoggerCollectorTests, self).setUp()
        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.workdir = tempfile.mkdtemp()

        self.app['mycomponent'] = LoggingComponent()
        self.component = self.app['mycomponent']
        setSite(self.app)

        self.component = LoggingComponent()


        return

    def tearDown(self):
        super(LoggerCollectorTests, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def test_ifaces(self):
        collector = LoggerCollector()
        verifyClass(ILoggerCollector, LoggerCollector)
        verifyObject(ILoggerCollector, collector)
        return

    def test_get_utility(self):
        # We can get a logger collector via utility lookup
        util1 = queryUtility(ILoggerCollector, default=None)
        util2 = queryUtility(ILoggerCollector, default=None)
        self.assertTrue(util1 is util2)
        self.assertTrue(isinstance(util1, LoggerCollector))
        return

    def test_get_loggers(self):
        # We can get loggers from a logger collector
        collector = LoggerCollector()
        result0 = collector.getLoggers(None)
        result1 = collector.getLoggers('not-a-site')
        result2 = collector.getLoggers(self.app)
        collector.registerLogger(self.app, self.component)
        result3 = collector.getLoggers(self.app)
        self.assertEqual(result0, [])
        self.assertEqual(result1, [])
        self.assertEqual(result2, [])
        self.assertEqual(result3, [self.component])
        self.assertTrue(result3[0] is self.component)
        return

    def test_register_logger(self):
        # We can register loggers by name
        collector = LoggerCollector()
        collector.registerLogger(None, self.component) # Should have no effect
        collector.registerLogger(object(), self.component) # Same here
        collector.registerLogger(self.app, self.component)
        self.assertEqual(['app'], collector.keys())
        return

    def test_register_logger_double(self):
        # Registering the same component twice gives one entry, not two
        collector = LoggerCollector()
        collector.registerLogger(self.app, self.component)
        collector.registerLogger(self.app, self.component)
        self.assertEqual(len(collector['app']), 1)
        return

    def test_unregister_logger(self):
        # We can also unregister loggers
        collector = LoggerCollector()
        collector.registerLogger(self.app, self.component)
        collector.unregisterLogger(self.app, self.component)
        result = collector.getLoggers(self.app)
        self.assertEqual(result, [])
        return

    def test_unregister_logger_invalid(self):
        # We can cope with unregistration of non-existing entries.
        collector = LoggerCollector()
        collector.registerLogger(self.app, self.component)
        collector.unregisterLogger(None, self.component)
        collector.unregisterLogger(self.app, 'nonsense')
        self.assertEqual(len(collector), 1)
        return

class LogfileChangeTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(LogfileChangeTests, self).setUp()
        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        self.dc_root_new = None
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.workdir = tempfile.mkdtemp()

        self.app['mycomponent'] = LoggingComponent()
        self.component = self.app['mycomponent']
        setSite(self.app)
        self.component = LoggingComponent()
        return

    def tearDown(self):
        super(LogfileChangeTests, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        if self.dc_root_new is not None:
            shutil.rmtree(self.dc_root_new)
        clearSite()
        return

    def test_storage_move(self):
        # When a datacenter storage (its path) changes, we have to
        # move the logfiles as well.
        filename1 = self.component.logger.handlers[0].baseFilename
        self.dc_root_new = tempfile.mkdtemp()
        self.app['datacenter'].setStoragePath(self.dc_root_new)
        filename2 = self.component.logger.handlers[0].baseFilename
        self.assertTrue(filename1 != filename2)
        self.assertTrue(filename2.startswith(self.dc_root_new))
        return

    def test_storage_deletion(self):
        # When a site is deleted, the loggers should go away as well
        self.dc_root_new = tempfile.mkdtemp()
        logger1 = self.component.logger.handlers # create entry in collector
        collector = queryUtility(ILoggerCollector)
        loggers1 = collector.keys()
        root = self.app.__parent__
        del root['app']
        loggers2 = collector.keys()
        self.assertEqual(loggers1, ['app'])
        self.assertEqual(loggers2, [])
        return
