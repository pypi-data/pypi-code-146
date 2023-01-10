#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to insert EFECS event data into the ROC database."""
import json
import os
from datetime import datetime

import sqlalchemy.exc
import xmltodict

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import FileTarget, PyObjectTarget

from roc.dingo.constants import PIPELINE_DATABASE, TRYOUTS, TIME_WAIT_SEC, TIME_EFECS_STRFORMAT
from roc.dingo.models.data import EfecsEvents
from roc.dingo.tools import get_columns, insert_in_db, query_db, delete_in_db, glob_paths

__all__ = ['EfecsToDb']


class EfecsToDb(Task):
    """
    Insert EFECS event data
    into the ROC database
    """
    plugin_name = 'roc.dingo'
    name = 'efecs_to_db'

    def add_targets(self):
        self.add_input(identifier='efecs_files',
                       many=True,
                       filepath=EfecsToDb.get_efecs_files,
                       target_class=FileTarget)

    @staticmethod
    def get_efecs_files(pipeline):
        try:
            efecs_files = pipeline.args.efecs_files
            if not isinstance(efecs_files, list):
                efecs_files = [efecs_files]
            return efecs_files
        except:
            # If not defined as input argument, then assume that it is already
            # defined as target input
            pass

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):
        # get the input files
        self.efecs_files = glob_paths(self.inputs['efecs_files'].filepath)

        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get(
            'tryouts', default=[TRYOUTS], create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get(
            'wait', default=[TIME_WAIT_SEC], create=True)[0]

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get table class
        self.model = EfecsEvents

        # Get table columns (remove primary key)
        self.columns = get_columns(self.model, remove=['id'])

    def run(self):

        logger.debug('Task EfecsToDb is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                'Initializing inputs for task EfecsToDb has failed!')
            self.pipeline.exit()
            return

        # Number of EFECS files
        n_files = len(self.efecs_files)
        logger.info(f'{n_files} EFECS files to process')

        # loop over each input E-FECS file
        new_insert_count = 0
        already_insert_count = 0
        failed_insert_count = 0
        for i, current_file in enumerate(self.efecs_files):
            self.current_file = current_file
            logger.info(f'Processing {current_file}   ({n_files - i - 1} remaining)')
            # Parse file
            try:
                efecs_data = parse_efecs(current_file)

                # Make sure to always use list for EFECS events
                # And get total number of events in the EFECS file
                event_count = 0
                for key, val in efecs_data['events'].items():
                    if not isinstance(val, list):
                        efecs_data['events'][key] = [val]
                    event_count += len(efecs_data['events'][key])
            except:
                logger.exception(f'Parsing {current_file} has failed!')
                continue
            else:
                # GET LTP counter from input filename (e.g., "EFECS_M05.xml")
                ltp_count = int(efecs_data['header2']['@SPKT_ltp_number'])

                # Get EFECS file generation time
                gen_time = datetime.strptime(efecs_data['header']['@gen_time'],
                                             TIME_EFECS_STRFORMAT)

            # Check database content against EFECS file info
            if self.is_uptodate(ltp_count, gen_time, event_count):
                logger.info(f'{event_count} EFECS events from {current_file} already inserted, skip it')
                continue
            else:
                logger.info(f'{event_count} EFECS events will be inserted from {current_file}')

            # Loops over each EFECS event found in the input file
            for key, val in efecs_data['events'].items():
                for current_entry in val:
                    data_to_insert = {'name': key}
                    data_to_insert['utc_time'] = datetime.strptime(current_entry.pop('@time'),
                                                                   TIME_EFECS_STRFORMAT)

                    data_to_insert['attributes'] = {
                        attr_key.replace("@", ""): attr_val
                        for attr_key, attr_val in current_entry.items()
                    }
                    data_to_insert['ltp_count'] = ltp_count
                    data_to_insert['gen_time'] = gen_time

                    # Define columns to check in case of update
                    update_fields_kwargs = {col_name:col_val
                                            for col_name, col_val in data_to_insert.items()
                                            if col_name in ['name', 'utc_time']}

                    # Insert / update efecs data into the database
                    status = insert_in_db(self.session, self.model, data_to_insert,
                                          update_fields=data_to_insert,
                                          update_fields_kwargs=update_fields_kwargs,
                                          tryouts=self.tryouts,
                                          wait=self.wait)
                    if status < 0:
                        logger.error(f'Cannot insert {data_to_insert} from {current_file}!')
                        failed_insert_count += 1
                    elif status == 0:
                        new_insert_count += 1
                        logger.debug(f'{data_to_insert} inserted')
                    else:
                        already_insert_count += 1
                        logger.debug(f'{data_to_insert} already inserted (updated)')

        if new_insert_count > 0:
            logger.info(f'{new_insert_count} EFECS events inserted')
        if already_insert_count > 0:
            logger.info(f'{already_insert_count} EFECS events updated')
        if failed_insert_count > 0:
            logger.warning(f'{failed_insert_count} EFECS events insertion have failed!')

    def is_uptodate(self, ltp_count, gen_time, event_count):
        """
        Compare content of the pipeline.efecs_events table with
        input input EFECS file ltp count, generation time and number of events.
        Return True if the database and file content are the same.

        :param ltp_count: EFECS file LTP count (integer)
        :param gen_time: EFECS file generation time (datetime.datetime object)
        :param event_count: Number of EFECS events in the file
        :return: True if EFECS file events are already found in the database, False otherwise
        """
        is_found = False
        try:
            # Query database to get EFECS events with
            # input values for ltp_count and gen_time
            filters = (EfecsEvents.ltp_count == ltp_count)
            rows = query_db(self.session, EfecsEvents.gen_time,
                            filters=filters,
                            tryouts=self.tryouts,
                            wait=self.wait,
                            to_dict='records')

            row_count = len(rows)
            if row_count == 0:
                logger.debug('No entry found for {ltp_count} in the database')
            else:
                is_found = (all(current_event['gen_time'] == gen_time for current_event in rows) and
                        row_count == event_count)

            if not is_found and row_count > 0 and gen_time < rows[0]['gen_time']:
                logger.warning(f'Input EFECS file generation time ({gen_time}) for {self.current_file}'
                               f' is older than in database ({rows[0]["gen_time"]})!')
        except:
            # If cannot compare, assume is_found=False by default
            logger.exception('Database content cannot be compared!')

        return is_found


def parse_efecs(efecs_file):
    """
    Parse EFECS XML input file.

    :param efecs_file: Path to EFECS file to parse
    :return: Content of input XML as a dictionary
    """
    with open(efecs_file, 'r') as xml:
        xml_dict = xmltodict.parse(xml.read())

    return xml_dict['eventfile']
