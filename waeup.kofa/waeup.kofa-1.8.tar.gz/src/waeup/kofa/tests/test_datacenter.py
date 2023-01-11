# -*- coding: utf-8 -*-
## Tests for datacenter
##
## XXX: Most tests for datacenter are still in doctest datacenter.txt
##
import os
import shutil
import tempfile
import unittest
from zope.component import getUtility, getGlobalSiteManager
from zope.interface.verify import verifyObject, verifyClass
from waeup.kofa.datacenter import DataCenter
from waeup.kofa.interfaces import (
    IDataCenter, IDataCenterConfig, IExportJobContainer)

class DataCenterLogQueryTests(unittest.TestCase):
    # Tests for querying logfiles via datacenter.

    def setUp(self):
        # create a temporary place to store files
        self.workdir = tempfile.mkdtemp()
        self.storage = os.path.join(self.workdir, 'storage')
        os.mkdir(self.storage)
        self.logpath = os.path.join(self.storage, 'logs', 'myapp.log')
        # register a datacenter config that provides the set up location
        self.config = {'path': self.storage,}
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(self.config, IDataCenterConfig)
        pass

    def tearDown(self):
        self.gsm.unregisterUtility(self.config, IDataCenterConfig)
        shutil.rmtree(self.workdir)
        return

    def fill_logfile(self, num=1):
        # write 100 messages into logfile, with 50 containing 'Msg'
        path = self.logpath
        for m in range(num-1,-1,-1):
            # write messages in order: lowest message in oldest file
            fp = open(path, 'wb')
            for n in range(50*m, 50*m+50):
                fp.write('Msg %d\n' % (n + 1))
                fp.write('Other Line %d\n' % (n + 1))
            fp.write('A Message with Ümläüt')
            fp.close()
            path = self.logpath + '.%d' % m
        return

    def test_util_available(self):
        # a self-test
        config = getUtility(IDataCenterConfig)
        self.assertTrue(config is not None)
        return

    def test_query_logfiles(self):
        # We can find entries in logfiles
        datacenter = DataCenter()
        open(self.logpath, 'wb').write('Message 1\n')
        result = list(datacenter.queryLogfiles('myapp.log', 'Message'))
        self.assertEqual(result, [u'Message 1\n'])
        return

    def test_query_logfiles_multi_logs(self):
        # We can find entries in multiple logfiles (backups)
        datacenter = DataCenter()
        open(self.logpath, 'wb').write('Msg 3\n')
        open(self.logpath + '.2', 'wb').write('Msg 2\n')
        open(self.logpath + '.10', 'wb').write('Msg 1\n')
        result = list(datacenter.queryLogfiles('myapp.log', 'Msg'))
        # entry of logfile .10 comes after entry of logfile .2
        self.assertEqual(result, [u'Msg 1\n', u'Msg 2\n', u'Msg 3\n'])
        return

    def test_query_logfiles_ignores_other_logs(self):
        # We look only for the basename specified
        datacenter = DataCenter()
        open(self.logpath, 'wb').write('Msg 1\n')
        open(self.logpath + '-not-a-real-log', 'wb').write('Msg 2\n')
        open(self.logpath + '-not-a-real-log.1', 'wb').write('Msg 3\n')
        result = list(datacenter.queryLogfiles('myapp.log', 'Msg'))
        # Msg 2 and 3 won't show up in results.
        self.assertEqual(result, [u'Msg 1\n'])
        return

    def test_query_logfiles_not_existant(self):
        # We make sure only existing logs are searched
        datacenter = DataCenter()
        open(self.logpath + '.1', 'wb').write('Msg 1\n')
        result = list(datacenter.queryLogfiles('myapp.log', 'Msg'))
        # works, although there is no myapp.log, only myapp.log.1
        self.assertEqual(result, ['Msg 1\n'])
        return

    def test_query_logfiles_invalid_regexp(self):
        # Invalid regular expressions give a ValueError
        datacenter = DataCenter()
        open(self.logpath, 'wb').write('Msg 1\n')
        result = datacenter.queryLogfiles('myapp.log', '(a')
        self.assertRaises(ValueError, list, result)
        return

    def test_query_logfiles_batching_limit(self):
        # we can use `limit` for batching
        datacenter = DataCenter()
        self.fill_logfile()
        result = list(datacenter.queryLogfiles(
            'myapp.log', 'Msg', limit=10))
        self.assertEqual(len(result), 10)
        self.assertEqual(result[-1], 'Msg 10\n')
        return

    def test_query_logfiles_batching_start(self):
        # `start` is respected when batching
        datacenter = DataCenter()
        self.fill_logfile()
        result = list(datacenter.queryLogfiles(
            'myapp.log', 'Msg', start=25))
        self.assertEqual(len(result), 25)
        self.assertEqual(result[0], u'Msg 26\n')
        return

    def test_query_logfiles_batching_limit_and_start(self):
        # we can use `start` and `limit` simultanously
        datacenter = DataCenter()
        self.fill_logfile()
        result = list(datacenter.queryLogfiles(
            'myapp.log', 'Msg', start=25, limit=10))
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0], u'Msg 26\n')
        self.assertEqual(result[-1], u'Msg 35\n')
        return

    def test_query_logfiles_batching_edge_cases(self):
        # we can find last matches if found num < limit.
        datacenter = DataCenter()
        self.fill_logfile()
        result = list(datacenter.queryLogfiles(
            'myapp.log', 'Msg', start=45, limit=10))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], u'Msg 46\n')
        self.assertEqual(result[-1], u'Msg 50\n')
        return

    def test_query_logfiles_batching_multiple_files(self):
        # batching works also with multiple log files
        datacenter = DataCenter()
        self.fill_logfile(num=2)
        result = list(datacenter.queryLogfiles(
            'myapp.log', 'Msg', start=45, limit=10))
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0], u'Msg 46\n')
        self.assertEqual(result[-1], u'Msg 55\n')
        return

    def test_query_logfiles_regex_match_inner(self):
        # we also find lines that match at some inner part
        datacenter = DataCenter()
        self.fill_logfile()
        result = list(datacenter.queryLogfiles('myapp.log', 'sg 1\n'))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], u'Msg 1\n')
        return

    def test_query_logfiles_umlauts(self):
        # we return results as unicode decoded from utf-8
        datacenter = DataCenter()
        self.fill_logfile()
        result = list(datacenter.queryLogfiles(
            'myapp.log', u'Ümläüt'))
        self.assertTrue(isinstance(result[0], unicode))
        self.assertEqual(result, [u'A Message with Ümläüt'])
        return

class DataCenterTests(unittest.TestCase):
    # General datacenter tests.

    def setUp(self):
        # create a temporary place to store files
        self.workdir = tempfile.mkdtemp()
        self.storage = os.path.join(self.workdir, 'storage')
        os.mkdir(self.storage)
        self.logpath = os.path.join(self.storage, 'logs', 'myapp.log')
        # register a datacenter config that provides the set up location
        self.config = {'path': self.storage,}
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(self.config, IDataCenterConfig)
        pass

    def tearDown(self):
        self.gsm.unregisterUtility(self.config, IDataCenterConfig)
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # we comply with interfaces
        obj = DataCenter()
        verifyClass(IDataCenter, DataCenter)
        verifyClass(IExportJobContainer, DataCenter)
        verifyObject(IDataCenter, obj)
        verifyObject(IExportJobContainer, obj)
        return

    def test_get_log_files(self):
        # We can get lists of logfiles available.
        # By default, backups are skipped.
        datacenter = DataCenter()
        logpath2 = self.logpath + '.1'
        logpath3 = self.logpath + '.2'
        for path in self.logpath, logpath2, logpath3:
            open(path, 'wb').write('some contents')
        result = datacenter.getLogFiles()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, os.path.basename(self.logpath))
        return

    def test_get_log_files_incl_backups(self):
        # We can get lists of logfiles including backup logs.
        datacenter = DataCenter()
        logpath2 = self.logpath + '.1'
        logpath3 = self.logpath + '.2'
        for path in self.logpath, logpath2, logpath3:
            open(path, 'wb').write('some contents')
        result = datacenter.getLogFiles(exclude_backups=False)
        self.assertEqual(len(result), 3)
        names = [x.name for x in result]
        expected = [os.path.basename(x) for x in [
            self.logpath, logpath2, logpath3]]
        self.assertEqual(names, expected)
        return

    def test_append_csv_file(self):
        # we can append CSV files to others
        datacenter = DataCenter()
        csv_file1 = os.path.join(self.workdir, 'foo.csv')
        csv_file2 = os.path.join(self.workdir, 'bar.csv')
        open(csv_file1, 'wb').write('name,age\nBarney,28')
        open(csv_file2, 'wb').write('name,age\nManfred,28')
        datacenter._appendCSVFile(csv_file2, csv_file1)
        result = open(csv_file1, 'rb').read()
        self.assertEqual(result, 'age,name\r\n28,Barney\r\n28,Manfred\r\n')
        # The source is deleted afterwards
        self.assertEqual(os.path.exists(csv_file2), False)
        return

    def test_append_csv_file_no_dest(self):
        # a non-existing dest CSV file will result in a simple move
        datacenter = DataCenter()
        csv_file1 = os.path.join(self.workdir, 'foo.csv')
        csv_file2 = os.path.join(self.workdir, 'bar.csv')
        # csv_file1 does not exist
        open(csv_file2, 'wb').write('name,age\nManfred,28\n')
        datacenter._appendCSVFile(csv_file2, csv_file1)
        result = open(csv_file1, 'rb').read()
        # raw input, no CSV mangling
        self.assertEqual(result, 'name,age\nManfred,28\n')
        # The source is deleted afterwards
        self.assertEqual(os.path.exists(csv_file2), False)
        return

    def test_append_csv_file_no_source(self):
        # a non existing source file will mean no changes at all
        datacenter = DataCenter()
        csv_file1 = os.path.join(self.workdir, 'foo.csv')
        csv_file2 = os.path.join(self.workdir, 'bar.csv')
        open(csv_file1, 'wb').write('name,age\nManfred,28\n')
        # csv_file2 does not exist
        datacenter._appendCSVFile(csv_file2, csv_file1)
        result = open(csv_file1, 'rb').read()
        # csv_file1 is the same as before
        self.assertEqual(result, 'name,age\nManfred,28\n')
        return

    def test_append_csv_file_same_src_and_dest(self):
        # if both csv files are the same file, nothing will be changed
        datacenter = DataCenter()
        csv_file1 = os.path.join(self.workdir, 'foo.csv')
        csv_file2 = csv_file1
        open(csv_file1, 'wb').write('name,age\nManfred,28\n')
        # csv_file2 does not exist
        datacenter._appendCSVFile(csv_file2, csv_file1)
        result = open(csv_file1, 'rb').read()
        # csv_file1 is the same as before
        self.assertEqual(result, 'name,age\nManfred,28\n')
        self.assertEqual(os.path.exists(csv_file2), True)
        return
