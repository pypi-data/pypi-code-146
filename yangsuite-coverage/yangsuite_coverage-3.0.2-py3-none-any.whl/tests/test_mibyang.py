# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Test MIB YANG mapping."""

import os
import subprocess
import unittest2 as unittest
from unittest import mock
from subprocess import Popen
from pathlib import PosixPath
from pandas import DataFrame

from yangsuite.paths import set_base_path
from yscoverage.mibyang import MIBYANGpath, YANGpath


class MockDevProfile:
    class Base:
        profile_name = 'cat9k'
        address = '192.168.0.2'
        username = 'test'
        password = 'lab'

    def __init__(self):
        self.base = self.Base()


class Testmy(MIBYANGpath):
    def __init__(self, a, b, c, d):
        super().__init__(a, b, c, d)


class TestMibYang(unittest.TestCase):
    """Tests for MIB YANG mapping object."""
    @classmethod
    def setUpClass(cls):
        """Function that will be called before tests are run."""
        cls.testdir = os.path.join(os.path.dirname(__file__), 'data')
        set_base_path(cls.testdir)
        cls.dev_profile = MockDevProfile()
        cls.stdoutdir = os.path.join(cls.testdir, 'stdout')
        cls.mibs = os.path.join(os.path.dirname(__file__), 'fixtures', 'mibs')
        cls.wsdir = os.path.join(cls.testdir, 'ws')
        cls.modelfile = os.path.join(cls.wsdir, 'modelfiles')
        cls.modelfile_num = 1
        cls.device_reply = '''
            <?xml version="1.0" ?>
            <rpc-reply
                message-id="urn:uuid:d41f81b1-8cd5-4d50-8560-30a6a35fadcf"
                xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
                xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"
            >
            <data>
                <aaa-data
                    xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-aaa-oper"
                >
                <aaa-users>
                    <username>admin</username>
                    <aaa-sessions>
                    <aaa-uid>11</aaa-uid>
                    <session-id>4001</session-id>
                    <ip-addr>0.0.0.0</ip-addr>
                    <protocol>aaa-sess-proto-type-none</protocol>
                    <login-time>2021-10-06T04:22:42+00:00</login-time>
                    </aaa-sessions>
                </aaa-users>
                </aaa-data>
            </data>
            </rpc-reply>
        '''

    def test_mib_yang_path(self):
        """Instantiate MIBYANGpath class and check attributes."""
        class Testmy(MIBYANGpath):
            def __init__(self, a, b, c, d):
                super().__init__(a, b, c, d)

            def get_filename(self):
                return 'iosxe.experimental.17.8.20211130'

        mibyang_path = Testmy(
            'openconfig-interfaces', 'test',
            self.dev_profile, "test+ocif-alpha"
        )
        rpc = mibyang_path.build_rpc(
            mibyang_path.yobj.xpaths[0].split('/')[1],
            mibyang_path.yobj.yang_df
        )
        self.assertEqual(rpc[0][0], 'get')
        self.assertEqual(rpc[0][1]['filter'].tag, 'filter')
        self.assertEqual(rpc[0][1]['filter'][0].tag, 'interfaces')
        self.assertEqual(len(mibyang_path.yobj.xpaths), 60)
        self.assertEqual(len(mibyang_path.yobj.yang_df), 61)

    def test_yang_get_readable(self):
        """Instatiate YANGpath class and check readable content."""
        yobj = YANGpath('openconfig-interfaces', 'test+ocif-alpha')
        yobj.get_readable()
        self.assertEqual(len(yobj.xpaths), 60)
        self.assertEqual(len(yobj.yang_df), 61)
        self.assertEqual(yobj.xpaths[0], '/interfaces/interface/name')
        self.assertEqual(
            yobj.xpaths[-1],
            '/interfaces/interface/subinterfaces/subinterface/state/counters/last-clear' # noqa
        )
        self.assertEqual(
            yobj.yang_df['/interfaces/interface/config/name'],
            {
                'namespace': 'http://openconfig.net/yang/interfaces',
                'tokens': [
                    'interfaces',
                    'interface',
                    'config',
                    'name'
                ]
            }
        )

    @mock.patch('subprocess.Popen')
    def test_get_image_version(self, popen_mock):
        class TestPopen(Popen):
            def __init__(
                self, cmd, stdout=None, stderr=None
            ):
                self.cmd = cmd
                self.stdout = stdout
                self.stderr = stderr

            def communicate(self):
                # snmpwalk cmd output must be numeric OIDs mapped to values
                return ('''.iso.org.dod.internet.mgmt
                    .mib-2.system.sysDescr.0 = STRING: Cisco
                    IOS Software [Cupertino], Catalyst L3
                    Switch Software (CAT9K_IOSXE),
                    Experimental Version 17.8.20211130:
                    143720 [CSCvy28712.polaris_dev-
                    /nobackup/petervh/GIT_workspace7
                    /polaris 101]\r\nCopyright (c)
                    1986-2021 by Cisco Systems, Inc.
                    \r\nCompiled Tue 30-Nov\n'''.encode(), None)

        popen_mock.return_value = TestPopen(
            ['mock', 'cmd'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        mibyang_path = Testmy(
            'openconfig-interfaces', 'test',
            self.dev_profile, "test+ocif-alpha"
        )

        # Expect no values to OIDs mapped and subprocess cmd sucessfully ran
        self.assertEqual(
            mibyang_path.get_oids_to_values_from_device(
                'mock cmd',
                '.mock.oid'
            )[0],
            {'.mib-2.system.sysDescr.0': 'Cisco'}
        )

    @mock.patch('yscoverage.mibyang.YANGpath.get_readable')
    def test_load_walk_file_exact_ver_match(self, get_readable_mock):
        """Positive test for load_walk_file with exact ver. match"""
        walk_ver = 'iosxe.experimental.17.8.20211130'
        get_readable_mock.return_value = {}

        class Testmy(MIBYANGpath):
            def __init__(self, a, b, c, d):
                super().__init__(a, b, c, d)

            def get_filename(self):
                return walk_ver

        values_to_oids, walk_file = Testmy.load_walk_file(
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings'
            ),
            walk_ver
        )

        self.assertIsNotNone(values_to_oids)
        self.assertEqual(
            walk_file,
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings',
                f'{walk_ver}.walk'
            ))

    @mock.patch('yscoverage.mibyang.YANGpath.get_readable')
    def test_load_walk_file_higher_ver_match(self, get_readable_mock):
        """ Positive test for load_walk_file with matching
            with higher minor ver. .walk file"""
        walk_ver = 'iosxe.experimental.17.7.20211130'
        expected_walk_ver = 'iosxe.experimental.17.8.20211130'
        get_readable_mock.return_value = {}

        class Testmy(MIBYANGpath):
            def __init__(self, a, b, c, d):
                super().__init__(a, b, c, d)

            def get_filename(self):
                return walk_ver

        values_to_oids, walk_file = Testmy.load_walk_file(
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings'
            ),
            walk_ver
        )

        self.assertIsNotNone(values_to_oids)
        self.assertEqual(
            walk_file,
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings',
                f'{expected_walk_ver}.walk'
            ))

    @mock.patch('yscoverage.mibyang.YANGpath.get_readable')
    def test_load_walk_file_negative_match(self, get_readable_mock):
        """ Negative test for load_walk_file with no match,
            because desired minor ver. is higher"""
        walk_ver = 'iosxe.experimental.17.9.20211130'
        get_readable_mock.return_value = {}

        class Testmy(MIBYANGpath):
            def __init__(self, a, b, c, d):
                super().__init__(a, b, c, d)

            def get_filename(self):
                return walk_ver

        oids_to_values, walk_file = Testmy.load_walk_file(
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings'
            ),
            walk_ver
        )

        self.assertEqual(oids_to_values, {})
        self.assertEqual(
            walk_file,
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings',
                f'{walk_ver}.walk'
            ))

    @mock.patch('yscoverage.mibyang.YANGpath.get_readable')
    def test_load_walk_file_negative_os_match(self, get_readable_mock):
        """ Negative test for load_walk_file with no match,
            because major/minor ver. are the same, but OS are different"""
        walk_ver = 'iosxr.17.8.20211130'
        get_readable_mock.return_value = {}

        class Testmy(MIBYANGpath):
            def __init__(self, a, b, c, d):
                super().__init__(a, b, c, d)

            def get_filename(self):
                return walk_ver

        oids_to_values, walk_file = Testmy.load_walk_file(
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings'
            ),
            walk_ver
        )

        self.assertEqual(oids_to_values, {})
        self.assertEqual(
            walk_file,
            os.path.join(
                PosixPath(__file__).parent.resolve(),
                self.testdir,
                'users',
                'test',
                'mibyang_mappings',
                f'{walk_ver}.walk'
            ))

    @mock.patch('subprocess.Popen')
    def test_get_values_to_oids_valid_snmpwalk(self, popen_mock):
        """Positive test for get_values_to_oids"""
        class TestPopen(Popen):
            def __init__(
                self, cmd, stdoutdir, stdout=None, stderr=None
            ):
                self.cmd = cmd
                self.stdout = stdout
                self.stderr = stderr

            def communicate(self):
                # Valid snmpwalk output, numeric OIDs mapped to values
                return (
                    '''
                        .1.3.4.5.4.2.9.9.715.1.1.5.0 = INTEGER: 1
                        .1.3.4.5.4.3.9.9.720.1.1.8.0 = Gauge32: 120
                        .1.3.4.5.4.4.9.9.720.1.1.17.0 = Gauge32: 2887515926
                        .1.3.4.5.4.5.9.9.720.1.1.18.0 = Gauge32: 120
                        .1.3.4.5.4.6.9.9.720.1.1.19.0 = Gauge32: 90
                        .1.3.4.5.4.7.9.9.720.1.1.20.0 = Gauge32: 180
                        .1.3.4.5.4.8.9.9.720.1.1.21.0 = INTEGER: 6
                        .1.3.4.5.4.933.9.9.730.1.1.1.0 = INTEGER: 2
                    '''.encode(),
                    None
                )

        popen_mock.return_value = TestPopen(
            ['mock', 'cmd'],
            self.stdoutdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        mibyang_path = Testmy(
            'openconfig-interfaces', 'test',
            self.dev_profile, "test+ocif-alpha"
        )
        self.assertEqual(
            mibyang_path.get_oids_to_values_from_device(
                'mock cmd',
                '.mock.oid'
            )[0], {
                '.1.3.4.5.4.2.9.9.715.1.1.5.0': '1',
                '.1.3.4.5.4.3.9.9.720.1.1.8.0': '120',
                '.1.3.4.5.4.4.9.9.720.1.1.17.0': '2887515926',
                '.1.3.4.5.4.5.9.9.720.1.1.18.0': '120',
                '.1.3.4.5.4.6.9.9.720.1.1.19.0': '90',
                '.1.3.4.5.4.7.9.9.720.1.1.20.0': '180',
                '.1.3.4.5.4.8.9.9.720.1.1.21.0': '6',
                '.1.3.4.5.4.933.9.9.730.1.1.1.0': '2'
            }
        )

    def test_match_to_existing_mapping_file_positive(self):
        """Postive test case for matching to existing mapping file"""
        class Testmy(MIBYANGpath):
            def __init__(self, a, b, c, d, map_filename=''):
                super().__init__(
                    a, b, c, d, map_filename=map_filename
                )
                self.values_to_oids = {'testvalue': '.test.oid'}
                self.mapped_df = DataFrame([{
                    'OID': '.csv.oid',
                    'YANG Xpath': '/csv/xpath',
                }])

            def get_filename(self):
                return 'iosxe.experimental.17.8.20211130'

            def get_values_to_xpaths_from_device(self):
                pass

            def get_oids_to_values_from_device(self, cmd, options=[]):
                pass

            def oids_to_xpaths_map(self, a, b):
                return {'.test.oid': '/test/xpath'}

        mibyang = Testmy(
            'openconfig-interfaces', 'test',
            self.dev_profile, 'test+ocif-alpha',
            map_filename='iosxe.experimental.17.8.20211130'
        )
        oids_to_xpaths = mibyang.get_device_oids_to_xpaths_map()
        self.assertEqual(
            oids_to_xpaths, {
                '.test.oid': '/test/xpath',
                '.csv.oid': ['/csv/xpath'],
            })

    def test_load_walk_file_negative(self):
        """Negative cases with diff. parameters to test load_walk_file"""
        cases = [
            '.experimental',
            '',
            'experimental.17.1.1',
            '.experimental.17.1.1'
        ]

        for filename in cases:
            self.assertEqual(
                ({}, f'{filename}.walk'),
                MIBYANGpath.load_walk_file('', filename)
            )

    def test_get_device_oids_to_xpaths_map(self):
        class Testmy(MIBYANGpath):
            def __init__(self, a, b, c, d, map_filename='', starting_oids=''):
                super().__init__(
                    a, b, c, d,
                    map_filename=map_filename,
                    starting_oids=starting_oids
                )
                self.oids_to_values = {
                    '.test.oid': 'testvalue',
                    '.negative.test.oid': 'negativetestvalue'
                }
                self.mapped_df = DataFrame([{
                    'OID': '.test.oid',
                    'YANG Xpath': '/test/xpath',
                }, {
                    'OID': '.negative.test.oid',
                    'YANG Xpath': '/test/other/xpath',
                }])
                self.starting_oids = starting_oids

            def get_filename(self):
                return 'iosxe.experimental.17.8.20211130'

            def translate_oids(self, starting_oids):
                return starting_oids

            def get_oids_to_values_from_device(self, cmd, options):
                pass

            def get_values_to_xpaths_from_device(self):
                pass

        mibyang = Testmy(
            'openconfig-interfaces', 'test',
            self.dev_profile, 'test+ocif-alpha',
            map_filename='iosxe.experimental.17.8.20211130',
            starting_oids=['.test']
        )

        oids_to_xpaths = mibyang.get_device_oids_to_xpaths_map()
        self.assertEqual(oids_to_xpaths, {'.test.oid': ['/test/xpath']})


if __name__ == "__main__":
    unittest.main()
