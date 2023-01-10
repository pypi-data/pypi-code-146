#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import json

import pytest

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase

# Define temporary folder for test
from roc.idb.models.idb import PacketHeader, ItemInfo, IdbRelease

TEST_TEMP_DIR = tempfile.gettempdir()


class TestPacketsToJson(CommandTestCase):
    """
    Test the rpl pkt_to_json command.
    """

    @pytest.mark.parametrize(
        'idb_source,idb_version,output_json_file',
        [('MIB', '20200131',
          os.path.join(TEST_TEMP_DIR, 'test_packets_to_json.json'))],
    )
    def test_packets_to_json(self, idb_source, idb_version, output_json_file):
        from poppy.core.conf import Settings

        # initialize the IDB

        # apply database migrations
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'INFO']

        # IDB PALISADE loading
        idb_palisade_loading = [
            'pop',
            'idb',
            'install',
            '-i',
            os.environ.get('IDB_INSTALL_DIR', tempfile.gettempdir()),
            '-s',
            'PALISADE',
            '-v',
            '4.3.5_MEB_PFM',
            '--load',
            '-ll',
            'INFO',
        ]

        # IDB MIB loading
        idb_mib_loading = [
            'pop',
            'idb',
            'install',
            '-i',
            os.environ.get('IDB_INSTALL_DIR', tempfile.gettempdir()),
            '-s',
            idb_source,
            '-v',
            idb_version,
            '--load',
            '--current',
            '-ll',
            'INFO',
        ]

        # apply database migrations
        self.run_command(db_upgrade)

        # Apply IDB loading
        self.run_command(idb_palisade_loading)

        # Apply IDB loading
        self.run_command(idb_mib_loading)

        # Ensure IDB is loaded to continue
        if self.is_idb(idb_source, idb_version):

            # Build command to test
            binary = '0CB7D904000D100501002730B9A4E54FA6D20165'
            command_to_test = ['pop', 'rpl',
                            '--idb-version', idb_version,
                            '--idb-source', idb_source,
                            'pkt_to_json',
                            '--binary', binary,
                            '--output-json-file', output_json_file,
                            '-ll', 'WARNING']
            self.run_command(command_to_test)

            assert os.path.isfile(output_json_file)

            # Open expected output and test output JSON files and compare both
            test_data_path = os.path.abspath(os.path.dirname(__file__))
            expected_json_path = os.path.join(test_data_path , 'data', os.path.basename(output_json_file))
            with open(expected_json_path, 'r') as ejson:
                exp_json = json.load(ejson)

            with open(output_json_file, 'r') as ojson:
                out_json = json.load(ojson)

            assert exp_json == out_json

        else:
            logger.error(f'Loading IDB [{idb_source}-{idb_version} has failed!')
            assert False


    @pytest.mark.parametrize(
        'idb_source,idb_version,output_json_file',
        [('MIB', '20200131',
          os.path.join(TEST_TEMP_DIR, 'test_packets_to_json_header_only.json'))],
    )
    def test_packets_to_json_header_only(self, idb_source, idb_version, output_json_file):
        from poppy.core.conf import Settings

        # initialize the IDB

        # Db migration
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'INFO']

        # IDB PALISADE loading
        idb_palisade_loading = [
            'pop',
            'idb',
            'install',
            '-i',
            os.environ.get('IDB_INSTALL_DIR', tempfile.gettempdir()),
            '-s',
            'PALISADE',
            '-v',
            '4.3.5_MEB_PFM',
            '--load',
            '-ll',
            'INFO',
        ]

        # IDB MIB loading
        idb_mib_loading = [
            'pop',
            'idb',
            'install',
            '-i',
            os.environ.get('IDB_INSTALL_DIR', tempfile.gettempdir()),
            '-s',
            idb_source,
            '-v',
            idb_version,
            '--load',
            '--current',
            '-ll',
            'INFO',
        ]

        # apply database migrations
        self.run_command(db_upgrade)

        # Apply IDB loading
        self.run_command(idb_palisade_loading)

        # Apply IDB loading
        self.run_command(idb_mib_loading)

        # Ensure IDB is loaded to continue
        if self.is_idb(idb_source, idb_version):

            # Build command to test
            binary = '0CB7D904000D100501002730B9A4E54FA6D20165'
            command_to_test = ['pop', 'rpl',
                            '--idb-version', idb_version,
                            '--idb-source', idb_source,
                            'pkt_to_json',
                            '--binary', binary,
                            '--output-json-file', output_json_file,
                            '-ll', 'ERROR']
            self.run_command(command_to_test)

            assert os.path.isfile(output_json_file)

            # Open expected output and test output JSON files and compare both
            test_data_path = os.path.abspath(os.path.dirname(__file__))
            expected_json_path = os.path.join(test_data_path , 'data', os.path.basename(output_json_file))
            with open(expected_json_path, 'r') as ejson:
                exp_json = json.load(ejson)

            with open(output_json_file, 'r') as ojson:
                out_json = json.load(ojson)

            assert exp_json == out_json

        else:
            logger.error(f'Loading IDB [{idb_source}-{idb_version} has failed!')
            assert False

    def is_idb(self, idb_source, idb_version):

        logger.debug(f'Querying IDB [{idb_source}-{idb_version}] ...')
        try:
            packet_header = (
                self.session.query(PacketHeader)
                .join(ItemInfo)
                .join(IdbRelease)
                .filter(ItemInfo.srdb_id == 'YIW00083',
                        IdbRelease.idb_version == idb_version,
                        IdbRelease.idb_source == idb_source)
                .one()
            )
        except:
            return False
        else:
            return True
