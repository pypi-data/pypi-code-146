#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from tempfile import gettempdir

import pytest

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase
from roc.idb.models.idb import PacketHeader, ItemInfo, IdbRelease
from roc.idb.tools.db import clean_idb


class TestLoadIdbCommand(CommandTestCase):
    @pytest.mark.parametrize(
        'idb_source,idb_version',
        [('PALISADE', '4.3.5_MEB_PFM'), ('MIB', '20200131')],
    )
    def test_install_and_load_idb(self, idb_source, idb_version):

        # Initializing commands
        self.install_dir = os.path.join(gettempdir(),
                                        f'idb-{idb_source}-{idb_version}')

        # Run database migrations
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'ERROR']
        self.run_command(db_upgrade)

        # Loading IDB
        command = [
            'pop',
            'idb',
            'install',
            '--force',
            '--install-dir', self.install_dir,
            '-s',
            idb_source,
            '-v',
            idb_version,
            '--load',
            '-ll',
            'ERROR',
        ]

        # Make sure the idb was not already loaded
        if clean_idb(self.session, idb_source, idb_version):

            logger.debug(f'Installing IDB [{idb_source}-{idb_version}] ...')
            self.run_command(command)

            logger.debug(f'Querying IDB [{idb_source}-{idb_version}] ...')
            packet_header = (
                self.session.query(PacketHeader)
                .join(ItemInfo)
                .join(IdbRelease)
                .filter(ItemInfo.srdb_id == 'YIW00083',
                        IdbRelease.idb_version == idb_version,
                        IdbRelease.idb_source == idb_source)
                .one()
            )

            # make assertions
            assert packet_header.cat == 7
            assert packet_header.sid == 42122
        else:
            assert False

    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # Remove IDB folder
        shutil.rmtree(self.install_dir)
