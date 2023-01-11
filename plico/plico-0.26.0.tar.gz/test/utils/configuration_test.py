#!/usr/bin/env python
import unittest
import os
from plico.utils.configuration import Configuration

__version__ = "$Id: configuration_test.py 26 2018-01-26 19:06:25Z lbusoni $"


class ConfigurationTest(unittest.TestCase):


    def setUp(self):
        self._hackToRunTestSuiteFromTrunkDir()

    def _hackToRunTestSuiteFromTrunkDir(self):
        print((os.getcwd()))
        if os.path.basename(os.getcwd()) == 'utils':
            self.CONF_FILE= 'configExample.conf'
        else:
            self.CONF_FILE= 'test/utils/configExample.conf'


    def testGetEntry(self):
        cfg= Configuration()
        cfg.load(self.CONF_FILE)
        self.assertEqual('192.168.1.29',
                         cfg.getValue('camera', 'ip_address'))


    def testModelIsReported(self):
        cfg= Configuration()
        cfg.load(self.CONF_FILE)
        self.assertEqual('bar', cfg.deviceModel('foo'))


    def testRaisesIfConfigFileIsMissing(self):
        cfg= Configuration()
        self.assertRaises(Exception, cfg.load, 'foo')


    def testGetFloatValue(self):
        cfg= Configuration()
        cfg.load(self.CONF_FILE)
        self.assertEqual(
            1.23e-9,
            cfg.getValue('foo', 'a_float_value', getfloat=True))

    def testNumberedSectionList(self):
        cfg= Configuration()
        cfg.load(self.CONF_FILE)
        self.assertEqual(
            ['pippo1', 'pippo2'],
            cfg.numberedSectionList('pippo'))


if __name__ == "__main__":
    unittest.main()
