#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to insert SOLO HK EDDS data into the ROC database."""

import time
from datetime import datetime, timedelta
import hashlib

import pandas as pd
from sqlalchemy import and_
import xmltodict

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import FileTarget
from sqlalchemy.exc import IntegrityError

from roc.dingo.constants import PIPELINE_DATABASE, TIME_SQL_STRFORMAT, TRYOUTS, TIME_WAIT_SEC, SQL_LIMIT
from roc.dingo.models.data import SoloHkParam, ProcessQueue
from roc.dingo.tools import query_db, get_columns, get_or_create_in_db, bulk_insert, glob_paths

__all__ = ["SoloHkToDb"]


class SoloHkToDb(Task):
    """
    Insert the content of input SOLO HK EDDS data files into the ROC database
    """
    plugin_name = 'roc.dingo'
    name = 'solohk_to_db'

    def add_targets(self):
        self.add_input(identifier='solo_hk_files',
                       many=True,
                       filepath=SoloHkToDb.get_solohk_files,
                       target_class=FileTarget)

    @staticmethod
    def get_solohk_files(pipeline):
        try:
            solo_hk_files = pipeline.args.solo_hk_files
            if not isinstance(solo_hk_files, list):
                solo_hk_files = [solo_hk_files]
            return solo_hk_files
        except:
            # If not defined as input argument, then assume that it is already
            # defined as target input
            pass

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        # get the input SOLO HK files
        self.solo_hk_files = glob_paths(self.inputs['solo_hk_files'].filepath)

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get(
            'tryouts', default=[TRYOUTS], create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get(
            'wait', default=[TIME_WAIT_SEC], create=True)[0]

        # Retrieve --limit keyword value
        self.limit = self.pipeline.get('limit',
                                       default=[SQL_LIMIT],
                                       args=True)[0]

        # Get --to-queue keyword
        self.to_queue = self.pipeline.get(
            'to_queue', default=False, create=True)

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get columns of the table
        self.model = SoloHkParam
        self.columns = get_columns(self.model, remove=['id'])

        # Get today date time
        self.today = datetime.today()

        # Initialize task counters
        self.inserted_counter = 0
        self.invalid_counter = 0

    def run(self):
        logger.debug('[SoloHkToDb]: Task is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                '[SoloHkToDb]: Initializing inputs has failed!')
            self.pipeline.exit()
            return

        n_files = len(self.solo_hk_files)
        logger.info(f'{n_files} input solo_hk_files to process')
        if n_files == 0:
            return

        # Loop over each input file in the input list
        for i, current_file in enumerate(self.solo_hk_files):
            logger.info(f'Processing {current_file}  ({n_files - i -1} remaining)')

            # Parse input file
            try:
                current_data = self.parse_solohk_xml(current_file)
            except:
                logger.exception(f'Parsing {current_file} has failed!')
                self.failed_files.append(current_file)
                continue

            n_element = current_data.shape[0]
            logger.info(f'{n_element} <ParamSampleListElement> elements found in {current_file}')
            if n_element == 0:
                logger.info(f'{current_file} is empty, skip it')
                self.processed_files.append(current_file)
                continue

            # Get list of pre-existing elements in the database
            try:
                # First convert input XML fields into
                # expected table column names
                # and compute extra values (SHA, utc_time)
                current_data = self.xml_to_solohkparam(current_data)
            except:
                logger.exception(f'Preprocessing data from {current_file} has failed!')
                self.failed_files.append(current_file)
                continue
            else:
                n_data_to_insert = current_data.shape[0]

            logger.info(f'Inserting {n_data_to_insert} elements from {current_file}')
            if n_data_to_insert == 0:
                self.processed_files.append(current_file)
                continue
            else:
                data_to_insert = current_data[self.columns].to_dict('records')

            try:
                bulk_insert(self.session, self.model, data_to_insert)
            except IntegrityError:
                logger.debug(f'Some data already found in the database for '
                             f'{current_file}, attempting to insert new data only')
                # Entries already found in the database, try to insert only new data
                # First query existing data (only SHA is required)
                # Define time range of request
                start_time = current_data['utc_time'].min()
                end_time = current_data['utc_time'].max()
                existing_data = pd.DataFrame.from_records(self._get_existing_data(self.model, self.model.sha,
                                                                                  start_time=start_time,
                                                                                  end_time=end_time))

                # Only keep unique SHA elements
                current_data = current_data[
                    ~current_data.sha.isin(existing_data.sha)]

                n_data_to_insert = current_data.shape[0]
                if n_data_to_insert == 0:
                    logger.info(f'No new data to insert for {current_file}')
                    self.processed_files.append(current_file)
                    continue
                else:
                    # Re-insert only new elements
                    data_to_insert = current_data[
                        self.columns].to_dict('records')
                    bulk_insert(self.session, self.model, data_to_insert)
                    logger.debug(
                        f'{n_data_to_insert} new elements inserted for {current_file}')
            except:
                logger.exception(f'Inserting new data from {current_file} has failed!')
                self.failed_files.append(current_file)
                continue
            else:
                self.processed_files.append(current_file)
                # Increment number of elements inserted
                self.inserted_counter += n_data_to_insert

            # Add current element days to process_queue table
            if self.to_queue:
                # Only add to process_queue table
                # new days to insert
                days_to_process = list(set(
                    [datetime.combine(current_date, datetime.min.time())
                     for current_date in
                     current_data['utc_time'].to_list()]))

                for current_day in days_to_process:
                    current_entry = self._as_process_queue(current_day)
                    job, done, created = get_or_create_in_db(self.session, ProcessQueue, current_entry)
                    if done:
                        logger.debug(f'{current_entry} inserted in process_queue table')
                    else:
                        logger.error(f'{current_entry} cannot be inserted in process_queue table')

        n_processed = len(self.processed_files)
        n_failed = len(self.failed_files)
        if n_processed > 0:
            logger.info(f'{self.inserted_counter} new elements inserted from {n_processed} files')
        if n_failed > 0:
            logger.error(f'Insertion has failed for {n_failed} files!')

    def _get_existing_data(self, model, fields,
                           start_time=None,
                           end_time=None):
        """
        Query database to return existing data for a given table

        :param model: class of the table
        :param fields: fields to query
        :return: returned rows (as a list of dictionaries)
        """

        # Get list of existing data in the database
        filters = []
        # Add start_time/end_time filters (if passed)
        if start_time:
            filters.append(model.utc_time >= str(
                start_time - timedelta(hours=1)))
        if end_time:
            filters.append(model.utc_time <= str(
                end_time + timedelta(hours=1)))

        if fields is None:
            fields = model

        results = query_db(self.session, fields,
                           filters=and_(*filters),
                           tryouts=self.tryouts,
                           wait=self.wait,
                           limit=self.limit,
                           to_dict='records')
        return results

    def parse_solohk_xml(self, solo_hk_xml):
        """
        Parse input SOLO HK EDDS XML file.

        :param solo_hk_xml: Path of the input Solo HK EDDS file
        :return: List of <ParamSampleListElement> elements
        """
        logger.debug(f'Parsing {solo_hk_xml} ...')
        with open(solo_hk_xml, 'r') as xml:
            xml_data = xmltodict.parse(xml.read())['ns2:ResponsePart']['Response'][
                'ParamResponse']['ParamSampleList']['ParamSampleListElement']

        if not isinstance(xml_data, list):
            xml_data = [xml_data]

        xml_data = pd.DataFrame.from_records(xml_data)

        return xml_data

    def xml_to_solohkparam(self, xml_data):
        """
        Convert <ParamSampleListElement> XML elements
        as entries to be inserted in the solo_hk_param table of the ROC database

        :param xml_data: pandas.Dataframe containing the <ParamSampleListElement> elements from input XML file
        :return: pandas.Dataframe with expected fields values for solo_hk_param table
        """
        # First keep only valid elements
        solohk_data = xml_data.loc[xml_data[
            'Validity'].isin(['VALID'])]
        solohk_data.reset_index(drop=True, inplace=True)

        if not solohk_data.shape[0] == 0:

            # Define field names as expected for solo_hk_param table
            solohk_data = solohk_data.rename(columns={
                'Name': 'name',
                'Unit': 'unit',
                'Description': 'description',
                'EngineeringValue': 'eng_value',
                'RawValue': 'raw_value',
            }, inplace=False,)

            # Convert elements times in datetime object
            solohk_data['utc_time'] = solohk_data.apply(
                lambda x: datetime.strptime(x['TimeStampAsciiA'],
                                            TIME_SQL_STRFORMAT), axis=1)
            # Compute SHA256 of the elements
            solohk_data['sha'] = solohk_data.apply(
                self._get_sha,
                axis=1)

            # Make sure to have unique elements (unique SHA values)
            solohk_data.drop_duplicates(subset=['sha'], inplace=True)

        return solohk_data

    def _get_sha(self, data):
        """
        Compute the SHA of the input element (from all parameters in data)

        :param data: Current SOLO HK parameter element
        :return: associated SHA256
        """
        sha = hashlib.sha256()
        sha.update(data['utc_time'].isoformat().encode('utf-8'))
        sha.update(data['name'].encode('utf-8'))
        sha.update(data['description'].encode('utf-8'))
        sha.update(data['raw_value'].encode('utf-8'))
        sha.update(data['eng_value'].encode('utf-8'))
        return str(sha.hexdigest())

    def _as_process_queue(self, current_date):
        """
        Return expected format for a process_queue table entry
        from input current date

        :param current_date: datetime.date() object to convert
        :return: dictionary for data_queue table entry
        """
        start_time = datetime.combine(current_date, datetime.min.time())
        return {'dataset_id': 'SOLO_HK_PLATFORM',
                'start_time': start_time,
                'insert_time': self.today}
