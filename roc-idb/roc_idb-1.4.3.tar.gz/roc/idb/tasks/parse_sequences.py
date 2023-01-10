#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import glob
import os

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.target import FileTarget, PyObjectTarget
from poppy.core.task import Task
from roc.idb.parsers import MIBParser

__all__ = [
    'ParseSequencesTask',
]


def parse_tc_duration_table(file_target):
    # open the duration table and load the data
    with file_target.open() as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        # skip the headers
        for _ in range(6):
            next(csv_reader)

        table = {}

        for row in csv_reader:
            # get the srdb id of the TC
            srdb_id, palisade_id, duration, comment = row

            table[srdb_id] = {
                'palisade_id': palisade_id,
                'duration': int(duration),
                'comment': comment,
            }

        return table


def parse_sequence_description_table(file_target):
    # open the sequence description table and load the data
    with file_target.open() as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        # skip the headers
        for _ in range(1):
            next(csv_reader)

        table = {}

        for row in csv_reader:
            # get the srdb id of the TC
            sequence_name, long_description, short_description = row

            table[sequence_name] = {
                'long_description': long_description,
                'description': short_description,
            }

        return table


def load_rpw_states(rpw_state_description_directory_path):

    state_description = {}

    for json_filepath in glob.glob(
        os.path.join(rpw_state_description_directory_path, '*.json')
    ):

        key = os.path.splitext(os.path.basename(json_filepath))[0]
        with open(json_filepath) as json_file:
            state_description[key] = json_file.read()

    return state_description


class ParseSequencesTask(Task):
    plugin_name = 'roc.idb'
    name = 'idb_parse_sequences'

    def get_tc_duration_table_filepath(self, pipeline):
        return os.path.join(pipeline.args.mib_dir_path, 'tc_duration.csv')

    def get_sequence_description_table_filepath(self, pipeline):
        return os.path.join(
            pipeline.args.mib_dir_path, 'sequence_description_table.csv'
        )

    def add_targets(self):
        self.add_input(
            target_class=FileTarget,
            identifier='tc_duration_table_filepath',
            filepath=self.get_tc_duration_table_filepath,
        )

        self.add_input(
            target_class=FileTarget,
            identifier='sequence_description_table_filepath',
            filepath=self.get_sequence_description_table_filepath,
        )

        self.add_output(target_class=PyObjectTarget, identifier='sequences')

        self.add_output(
            target_class=PyObjectTarget, identifier='tc_duration_table'
        )

        self.add_output(
            target_class=PyObjectTarget,
            identifier='sequence_description_table',
        )

        self.add_output(target_class=PyObjectTarget, identifier='rpw_states')

        self.add_output(target_class=PyObjectTarget, identifier='idb_version')

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):
        """
        Load MIB sequences into the ROC database
        """

        # get the database session
        self.session = self.pipeline.db.session

        # instantiate the MIB parser

        self.parser = MIBParser(
            os.path.join(self.pipeline.args.mib_dir_path, 'data'),
            None,  # no mapping file needed to load sequences
        )

        # parse the sequences
        sequences_data = self.parser.parse_sequences()

        # read the TC duration table
        self.outputs['tc_duration_table'].value = parse_tc_duration_table(
            self.inputs['tc_duration_table_filepath']
        )

        # read the sequence duration table
        self.outputs[
            'sequence_description_table'
        ].value = parse_sequence_description_table(
            self.inputs['sequence_description_table_filepath']
        )

        self.outputs['rpw_states'].value = load_rpw_states(
            os.path.join(self.pipeline.args.mib_dir_path, 'rpw_states')
        )

        self.outputs['sequences'].value = sequences_data
        self.outputs['idb_version'].value = self.parser.version()
