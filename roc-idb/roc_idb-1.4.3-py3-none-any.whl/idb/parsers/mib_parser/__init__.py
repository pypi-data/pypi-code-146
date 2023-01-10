#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

import numpy
from poppy.core.logger import logger

from .parse_sequence_mixin import ParseSequenceMixin
from roc.idb.parsers.srdb_parser import SRDBParser

__all__ = ['MIBParser']


class MIBParser(SRDBParser, ParseSequenceMixin):
    """
    Class used for the parsing of the .dat files of the IDB to get information on the
    IDB and MIB.
    """

    def setup_source_dir(self, dir_path):
        self._source = 'MIB'

        # MIB files path
        self.dir_path = dir_path

    def __init__(self, dir_path, mapping_file_path):
        """
        Store the mib_parser path of the .dat files containing the IDB.
        """

        if mapping_file_path is not None:
            super().__init__(dir_path, mapping_file_path)
        else:
            self.setup_source_dir(dir_path)
            logger.warning('No mapping file supplied, IDB parsing is disabled')
            logger.info(
                'Note: the mapping file is not needed to load sequences'
            )

    def version(self):
        """
        Return the version of the IDB defined in the dat file.
        """

        vdf_filepath = os.path.join(self.dir_path, 'vdf.dat')

        vdf_dtype = numpy.dtype(
            [
                ('NAME', 'U8'),  # short version name (8 char)
                ('COMMENT', 'U32'),
                ('DOMAINID', int),
                ('RELEASE', int),
                ('ISSUE', int),
            ]
        )
        vdf_table = numpy.loadtxt(
            vdf_filepath, delimiter='\t', dtype=vdf_dtype
        )

        # read the mib_version directly in the file
        with open(vdf_filepath) as f:
            self.mib_version = f.readline()

        try:
            # read the release note to compute the human readable version from the release date
            release_note_filepath = os.path.join(
                self.dir_path, '..', 'release_notes.json'
            )

            with open(release_note_filepath) as json_file:
                release_note = json.load(json_file)
                version = release_note['mib_release_date'].replace('-', '')
        except Exception as e:
            # compute the default version
            logger.warning('Error during release note loading')
            logger.warning(e)
            version = f'{vdf_table["NAME"]}_{vdf_table["COMMENT"]}'

        return version

    def compute_global_param_group_size(self, global_parameter_srdb_id):
        """
        Compute the global and sub-parameters block contribution to the group size.

        # packet structure:
        # =======================
        # param 1
        # param 2
        # ------ global param 3 -
        # > sub-parm 3.1           |
        # > sub-pram 3.2           | sub_param_list_len
        # > sub-pram 3.3           |
        # -----------------------
        # param 4
        # param 5
        # =======================

        :param global_parameter_srdb_id:
        :return:
        """
        sub_param_list_len = len(
            self.global_parameters[global_parameter_srdb_id]
        )

        return sub_param_list_len - 2

    def parse_and_load_sequences(self, session):
        mib_tables = self.parse_sequences()
        self.load_from_MIB(session, *mib_tables)
