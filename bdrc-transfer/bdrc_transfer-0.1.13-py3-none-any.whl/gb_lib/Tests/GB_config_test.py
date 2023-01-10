"""
Created on Mar 14, 2018

@author: jsk
"""
import tempfile
import unittest
from pathlib import Path

import os

from gb_lib import GbLib as lib


def brackets(contents):
    return '[' + str(contents) + ']'


class TestHappyPath(unittest.TestCase):
    __config_file = str(Path(tempfile.gettempdir(), "GbConfigTest.config"))
    # Doesnt have to be a valid file.
    __default_section: str = "default"
    __section1_expected = 'section1'
    __section2_expected = 'section2'
    __expected_section1_value = 'somethingOrOther'
    __default_expected_values: {} = {'host': 'host0', 'user': 'user0', 'keyFile': 'key0', 'port': 0}
    __section1_expected_values: {} = {'host': 'host1', 'user': 'user1', 'keyFile': 'key1', 'port': 1}
    __section2_expected_values: {} = {'host': 'host2', 'user': 'user2', 'keyFile': 'key2', 'port': 2}

    __s3_exp_val: {} = dict(__section1_expected_values)

    def setUp(self) -> None:
        Path(self.__config_file).touch(exist_ok=True)

    # region Set up test cases
    def put_all_keys_in_default(self):
        """
        Put all keys into default section
        """

        with open(self.__config_file, "w") as cfg:
            cfg.write("# Shouldn't matter\n")
            cfg.write(f"[{self.__default_section}]\n")

            # populate the config file__section1_expected_values
            for k, v in self.__default_expected_values.items():
                cfg.write(f"{k} = {v}\n")

    def put_no_keys_in_default(self):
        """
        Create empty default section, full section 1
        """

        with open(self.__config_file, "w") as cfg:
            # empty default section
            cfg.write(f"[{self.__default_section}]\n")
            #
            # Section
            cfg.write(f"[{self.__section1_expected}]\n")

            # populate the section
            for k, v in self.__section1_expected_values.items():
                cfg.write(f"{k} = {v}\n")

    def put_same_keys_in_two_sections_no_default(self):
        """
        Create the same keys in two sections: section1 and section2
        """

        with open(self.__config_file, "w") as cfg:

            cfg.write(f"[{self.__section1_expected}]\n")

            # populate the config file
            for k, v in self.__section1_expected_values.items():
                cfg.write(f"{k} = {v}\n")

            cfg.write(f"\n[{self.__section2_expected}]\n")

            # populate the config file
            for k, v in self.__section2_expected_values.items():
                cfg.write(f"{k} = {v}\n")

    def put_some_keys_in_one_section_no_default(self):
        """
        Create a few keys in one section: host and keyFile
        """
        with open(self.__config_file, "w") as cfg:
            cfg.write(f"[{self.__section1_expected}]\n")

            # populate the config file
            ev = self.__section1_expected_values['host']
            cfg.write(f"host = {ev}\n")

            ev = self.__section1_expected_values['keyFile']
            cfg.write(f"keyFile = {ev}\n")

    def put_some_keys_in_both_sections_no_default(self):
        """
        Create a few keys in two sections: host and keyFile
        """
        with open(self.__config_file, "w") as cfg:
            # Put host and keyFile in section1
            cfg.write(f"[{self.__section1_expected}]\n")

            ev = self.__section1_expected_values['host']
            cfg.write(f"host = {ev}\n")

            ev = self.__section1_expected_values['keyFile']
            cfg.write(f"keyFile = {ev}\n")

            # Put host and keyFile in section2
            cfg.write(f"[{self.__section2_expected}]\n")

            ev = self.__section2_expected_values['host']
            cfg.write(f"host = {ev}\n")

            ev = self.__section2_expected_values['keyFile']
            cfg.write(f"keyFile = {ev}\n")

    def put_different_keys_in_two_sections_no_default(self):
        """
        Create a host and keyFile in section 1
        user and port in section 2
        """
        with open(self.__config_file, "w") as cfg:
            # Put host and keyFile in section1
            cfg.write(f"[{self.__section1_expected}]\n")

            ev = self.__section1_expected_values['host']
            cfg.write(f"host = {ev}\n")

            ev = self.__section1_expected_values['keyFile']
            cfg.write(f"keyFile = {ev}\n")

            # Put user and port in section2
            cfg.write(f"[{self.__section2_expected}]\n")

            ev = self.__section2_expected_values['user']
            cfg.write(f"user = {ev}\n")

            ev = self.__section2_expected_values['port']
            cfg.write(f"port = {ev}\n")

    def sparse_defaults_no_overrides(self):
        """
        Put host and port in default, user in section 1, key in section 2
        :return:
        """
        with open(self.__config_file, "w") as cfg:
            cfg.write(f"[{self.__default_section}]\n")
            cfg.write(f"host = {self.__default_expected_values['host']}\n")
            cfg.write(f"port = {self.__default_expected_values['port']}\n")

            cfg.write(f"[{self.__section1_expected}]\n")
            cfg.write(f"user = {self.__section1_expected_values['user']}\n")

            cfg.write(f"[{self.__section2_expected}]\n")
            cfg.write(f"keyFile = {self.__section2_expected_values['keyFile']}\n")

    def sparse_defaults_overrides(self):
        """
        Put host and port in default, user and port in section 1, host and key in section 2

        """
        with open(self.__config_file, "w") as cfg:
            cfg.write(f"[{self.__default_section}]\n")

            # populate the config file__default_expected_values
            cfg.write(f"host = {self.__default_expected_values['host']}\n")
            cfg.write(f"port = {self.__default_expected_values['port']}\n")

            cfg.write(f"[{self.__section1_expected}]\n")
            cfg.write(f"user = {self.__section1_expected_values['user']}\n")
            cfg.write(f"port = {self.__section1_expected_values['port']}\n")

            cfg.write(f"[{self.__section2_expected}]\n")
            cfg.write(f"host = {self.__section2_expected_values['host']}\n")
            cfg.write(f"keyFile = {self.__section2_expected_values['keyFile']}\n")

    def tearDown(self):
        # Pack it in, pack it out
        os.unlink(self.__config_file)

    # region Constructor tests
    def testCtorNoParams(self):
        # Arrange

        x = lib.GbSftpConfig()
        x.config_file_name = self.__config_file

        # Act
        # Assert
        self.assertEqual(x.config_file_name, self.__config_file)

    def testCtorOneParams(self):
        x = lib.GbSftpConfig(config_file_name=self.__config_file)
        # Act
        # Assert
        self.assertEqual(x.config_file_name, self.__config_file)
        self.assertEqual(x.op_section, None)

        ex_op_section = "expected op section"
        x.op_section = ex_op_section
        self.assertEqual(x.op_section, ex_op_section)

    def testCtorAllParams(self):
        ex_op_section = "expected op section"
        x = lib.GbSftpConfig(type_section=ex_op_section, config_file_name=self.__config_file)
        # Assert
        self.assertEqual(x.config_file_name, self.__config_file)
        self.assertEqual(x.op_section, ex_op_section)

    # endregion

    # region scope tests
    def test_put_all_keys_in_default(self):

        self.put_all_keys_in_default()

        gb_conf = lib.GbSftpConfig(type_section='default', config_file_name=self.__config_file)

        self.assertEqual(gb_conf.op_section, 'default')
        self.assert_all(gb_conf, self.__default_expected_values)

    def test_put_no_keys_in_default(self):
        self.put_no_keys_in_default()
        gb_conf = lib.GbSftpConfig(type_section=self.__section1_expected, config_file_name=self.__config_file)

        self.assertEqual(gb_conf.op_section, self.__section1_expected)
        self.assert_all(gb_conf, self.__section1_expected_values)

    def test_put_same_keys_in_two_sections_no_default(self):
        self.put_same_keys_in_two_sections_no_default()

        gb_conf = lib.GbSftpConfig(type_section=self.__section1_expected, config_file_name=self.__config_file)
        self.assertEqual(gb_conf.op_section, self.__section1_expected)
        self.assert_all(gb_conf, self.__section1_expected_values)

        gb_conf.op_section = self.__section2_expected
        self.assertEqual(gb_conf.op_section, self.__section2_expected)
        self.assert_all(gb_conf, self.__section2_expected_values)

    def test_put_some_keys_in_one_section_no_default(self):
        self.put_some_keys_in_one_section_no_default()

        gb_conf = lib.GbSftpConfig(type_section=self.__section1_expected, config_file_name=self.__config_file)
        self.assertEqual(gb_conf.key_path, self.__section1_expected_values['keyFile'])
        self.assertEqual(gb_conf.host, self.__section1_expected_values['host'])
        self.assertEqual(gb_conf.user, "")  # should be returned when not found
        self.assertEqual(gb_conf.port, -1)

    def test_put_some_keys_in_both_sections_no_default(self):
        self.put_some_keys_in_both_sections_no_default()

        gb_conf = lib.GbSftpConfig(type_section=self.__section1_expected, config_file_name=self.__config_file)
        self.assertEqual(gb_conf.key_path, self.__section1_expected_values['keyFile'])
        self.assertEqual(gb_conf.host, self.__section1_expected_values['host'])
        self.assertEqual(gb_conf.user, "")  # should be returned when not found
        self.assertEqual(gb_conf.port, -1)

        gb_conf.op_section = self.__section2_expected
        self.assertEqual(gb_conf.key_path, self.__section2_expected_values['keyFile'])
        self.assertEqual(gb_conf.host, self.__section2_expected_values['host'])
        self.assertEqual(gb_conf.user, "")  # should be returned when not found
        self.assertEqual(gb_conf.port, -1)

    pass

    def test_put_different_keys_in_two_sections_no_default(self):
        self.put_different_keys_in_two_sections_no_default()

        gb_conf = lib.GbSftpConfig(type_section=self.__section1_expected, config_file_name=self.__config_file)

        self.assertEqual(gb_conf.key_path, self.__section1_expected_values['keyFile'])
        self.assertEqual(gb_conf.host, self.__section1_expected_values['host'])
        self.assertEqual(gb_conf.user, "")  # should be returned when not found
        self.assertEqual(gb_conf.port, -1)

        gb_conf.op_section = self.__section2_expected
        self.assertEqual(gb_conf.key_path, "")
        self.assertEqual(gb_conf.host, "")
        self.assertEqual(gb_conf.user, self.__section2_expected_values['user'])
        self.assertEqual(gb_conf.port, self.__section2_expected_values['port'])

    def test_sparse_defaults_no_overrides(self):
        """
        Expected return:
            scope == section 1:
                host: host0
                user: user1
                port: port0
                keyFile: ""
            scope == section 2:
                host: host0
                user: ""
                port: port0
                keyFile: key2

        :return:
        """
        self.sparse_defaults_no_overrides()

        gb_conf = lib.GbSftpConfig(type_section=self.__section1_expected, config_file_name=self.__config_file)
        self.assertEqual(gb_conf.host, self.__default_expected_values['host'])
        self.assertEqual(gb_conf.port, self.__default_expected_values['port'])
        self.assertEqual(gb_conf.user, self.__section1_expected_values['user'])
        self.assertEqual(gb_conf.key_path, "")

        gb_conf.op_section = self.__section2_expected
        self.assertEqual(gb_conf.host, self.__default_expected_values['host'])
        self.assertEqual(gb_conf.port, self.__default_expected_values['port'])
        self.assertEqual(gb_conf.user, "")
        self.assertEqual(gb_conf.key_path, self.__section2_expected_values['keyFile'])

    def test_sparse_defaults_overrides(self):
        """
        Expected return:
            scope section 1:
                host: host0
                port: port1
                user: user1
                keyFile: ""
            scope section 2:
                host: host2
                port: port0
                user: ""
                keyFile: key2


        :return:
        """
        self.sparse_defaults_overrides()

        gb_conf = lib.GbSftpConfig(type_section=self.__section1_expected, config_file_name=self.__config_file)
        self.assertEqual(gb_conf.host, self.__default_expected_values['host'])
        self.assertEqual(gb_conf.port, self.__section1_expected_values['port'])
        self.assertEqual(gb_conf.user, self.__section1_expected_values['user'])
        self.assertEqual(gb_conf.key_path, "")

        gb_conf.op_section = self.__section2_expected
        self.assertEqual(gb_conf.host, self.__section2_expected_values['host'])
        self.assertEqual(gb_conf.port, self.__default_expected_values['port'])
        self.assertEqual(gb_conf.user, "")
        self.assertEqual(gb_conf.key_path, self.__section2_expected_values['keyFile'])

    def assert_all(self, gb_conf: lib.GbSftpConfig, values: dict):
        """
        Tests all the values in a section
        :param gb_conf:
        :param values:
        :return:
        """
        self.assertEqual(gb_conf.user, values['user'])
        self.assertEqual(gb_conf.port, values['port'])
        self.assertEqual(gb_conf.key_path, values['keyFile'])
        self.assertEqual(gb_conf.host, values['host'])

    # end region


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
