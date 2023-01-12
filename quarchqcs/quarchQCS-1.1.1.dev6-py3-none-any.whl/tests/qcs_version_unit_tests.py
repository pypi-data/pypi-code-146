import unittest
import subprocess
from unittest.mock import Mock
from QuarchpyQCS.dtsComms import isVersionCompat
from QuarchpyQCS.dtsGlobals import dtsGlobals

class TestFioClass(unittest.TestCase):

    def test_equal_versions(self):
        dtsGlobals.minQCSVersion = "1.1.1"
        test_string = "1.1.1"

        self.assertTrue(isVersionCompat(test_string))

    def test_valid_version(self):
        dtsGlobals.minQCSVersion = "1.1.1"
        test_string = "1.1.2"

        self.assertTrue(isVersionCompat(test_string))

    def test_valid_versionv2(self):
        dtsGlobals.minQCSVersion = "1.1.1"
        test_string = "1.1.1.1"

        self.assertTrue(isVersionCompat(test_string))

    def test_valid_versionv3(self):
        dtsGlobals.minQCSVersion = "1.1.1"
        test_string = "3"

        self.assertTrue(isVersionCompat(test_string))

    def test_invalid_version(self):
        dtsGlobals.minQCSVersion = "1.1.2"
        test_string = "1.1.1"

        self.assertFalse(isVersionCompat(test_string))

    def test_invalid_versionv2(self):
        dtsGlobals.minQCSVersion = "1.1.2"
        test_string = "1.1"

        self.assertFalse(isVersionCompat(test_string))

    def test_invalid_versionv3(self):
        dtsGlobals.minQCSVersion = "3"
        test_string = "1.1.1"

        self.assertFalse(isVersionCompat(test_string))

    # @unittest.mock.patch('subprocess.call')
    # def test_no_parameters(self, os_system):
    #     # Testing only passing end callback
    #
    #     x = FioPerformance()
    #     self.assertTrue(x.start_workload())

