# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
This module contains tests for the OpenLP song importer.
"""
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from openlp.core.common.registry import Registry
from openlp.plugins.songs.lib.importers.openlp import OpenLPSongImport


class TestOpenLPImport(TestCase):
    """
    Test the functions in the :mod:`openlp` importer module.
    """
    def setUp(self):
        """
        Create the registry
        """
        Registry.create()

    def test_create_importer(self):
        """
        Test creating an instance of the OpenLP database importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.importers.openlp.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = OpenLPSongImport(mocked_manager, file_paths=[])

            # THEN: The importer object should not be None
            assert importer is not None, 'Import should not be none'

    def test_invalid_import_source(self):
        """
        Test OpenLPSongImport.do_import handles different invalid import_source values
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.importers.openlp.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = OpenLPSongImport(mocked_manager, file_paths=[])
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is not a list
            importer.import_source = Path()

            # THEN: do_import should return none and the progress bar maximum should not be set.
            assert importer.do_import() is None, 'do_import should return None when import_source is not a list'
            assert mocked_import_wizard.progress_bar.setMaximum.called is False, \
                'setMaximum on import_wizard.progress_bar should not have been called'
