#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to export SOLO HK EDDS data from the ROC database."""


import os
from datetime import timedelta, datetime
from pathlib import Path

from sqlalchemy import asc

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import FileTarget

from roc.dingo.constants import PIPELINE_DATABASE, START_TIME, END_TIME, TRYOUTS, TIME_WAIT_SEC, SQL_LIMIT, \
    DATA_VERSION, JENV, SOLO_HK_TEMPLATE, TIME_DAILY_STRFORMAT, TIME_SQL_STRFORMAT
from roc.dingo.models.data import ProcessQueue, SoloHkParam
from roc.dingo.tools import valid_data_version, query_db, delete_in_db, valid_time

__all__ = ["DbToSoloHk"]


class DbToSoloHk(Task):
    """
    Export solo_hk_param table data of the ROC database into output daily files.
    The output file format is a light version of SOLO EDDS response XML.
    """
    plugin_name = 'roc.dingo'
    name = 'db_to_solohk'

    def add_targets(self):
        self.add_output(identifier='solo_hk_files',
                        many=True,
                        target_class=FileTarget)

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        # Get start_time input value
        self.start_time = valid_time(self.pipeline.get(
            'start_time', default=[None],
            create=True)[0])
        if not self.start_time:
            self.start_time = START_TIME

        # Get end_time input value
        self.end_time = valid_time(self.pipeline.get(
            'end_time', default=[None],
            create=True)[0])
        if not self.end_time:
            self.end_time = END_TIME

        # Get list of dates to process
        # (If passed with start_time/end_time keywords, then only
        # process dates between start_time and end_time)
        self.date_list = self.pipeline.get(
            'date_list', default=[])

        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get(
            'tryouts', default=[TRYOUTS],
            create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get(
            'wait', default=[TIME_WAIT_SEC],
            create=True)[0]

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Retrieve --limit keyword value
        self.limit = self.pipeline.get('limit',
                                       default=[SQL_LIMIT],
                                       args=True)[0]

        # Retrieve --limit keyword value
        self.data_version = valid_data_version(self.pipeline.get('data_version',
                                                                 default=[
                                                                     DATA_VERSION],
                                                                 args=True)[0])

        # Get output directory
        self.output_dir = self.pipeline.output
        if not self.output_dir:
            raise FileNotFoundError(f'[DbToSoloHk]: output directory is not defined or does not exist ({self.output_dir})')
        if not os.path.isdir(self.output_dir):
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        # Get overwrite optional keyword
        self.overwrite = self.pipeline.get(
            'overwrite', default=False, args=True)

        # Get from-queue optional keyword
        self.from_queue = self.pipeline.get(
            'from_queue', default=False)

        # Get clean-queue optional keyword
        self.clean_queue = self.pipeline.get(
            'clean_queue', default=False)

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

    def run(self):
        logger.debug('[DbToSoloHk]: Task is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                '[DbToSoloHk]: Initializing inputs has failed!')
            self.pipeline.exit()
            return

        # if --from-queue is set get list of dates to process
        queue_entries = None
        if self.from_queue:
            try:
                filters = (ProcessQueue.dataset_id == "SOLO_HK_PLATFORM")
                queue_entries = query_db(self.session, ProcessQueue,
                                         filters=filters,
                                         order_by=asc(ProcessQueue.start_time),
                                         limit=self.limit,
                                         tryouts=self.tryouts,
                                         wait=self.wait,
                                         to_dict='records',
                                         raise_exception=True)
            except:
                logger.exception(
                    '[DbToSoloHk]: Flagged current job as failed')
                # TODO - Add a method to make failed/ directory with relevant
                # files inside (log, input/output, etc.)
                return
            else:
                logger.debug(f'{len(queue_entries)} dates to process returned from the database queue')
                self.date_list = [current_row['start_time'].date()
                                  for current_row in queue_entries]
        elif not self.date_list:
            current_day = self.start_time
            while current_day < self.end_time:
                self.date_list.append(current_day.date())
                current_day += timedelta(days=1)

        # Make sure to have unique values in date list
        self.date_list = sorted(list(set(self.date_list)))

        n_dates = len(self.date_list)
        if n_dates == 0:
            logger.info('No date to process, exiting')
            return
        else:
            logger.info(f'Exporting SOLO HK from database for {n_dates} dates')

        # Loop on date_list
        output_files = []
        queue_entries_to_clean = []
        for i, current_date in enumerate(self.date_list):

            # Get file version
            if queue_entries and queue_entries[i]['version']:
                current_version = valid_data_version(
                    queue_entries[i]['version'])
            else:
                current_version = self.data_version

            # Generate the output XML file path
            xml_path = os.path.join(
                self.output_dir,
                f'solo_HK_platform_{current_date.strftime(TIME_DAILY_STRFORMAT)}_V{current_version}.xml'
            )
            # Open a file with the name
            if os.path.isfile(xml_path) and not self.overwrite:
                logger.info(f'{xml_path} already exists!')
                if queue_entries:
                    queue_entries_to_clean.append(queue_entries[i])
                continue

            # Current start is date at 00:00:00
            current_start = datetime.combine(current_date,
                                             datetime.min.time())
            # current end is date + 1 at 00:00:00
            current_end = datetime.combine(current_date + timedelta(days=1),
                                           datetime.min.time())
            # Add input filters
            time = SoloHkParam.utc_time
            # greater or equal than ...
            # lesser than ...
            filters = (time >= str(current_start)) & (time < str(current_end))

            # Query data from database
            try:
                solohk_entries = query_db(self.session, SoloHkParam,
                                          filters=filters,
                                          limit=self.limit,
                                          tryouts=self.tryouts,
                                          wait=self.wait,
                                          order_by=SoloHkParam.utc_time,
                                          to_dict='records',
                                          raise_exception=True)
            except:
                logger.exception(f'[DbToSoloHk]: Task has failed for {current_date}')
                # TODO - Add a method to make failed/ directory with relevant
                # files inside (log, input/output, etc.)
                self.failed_files.append(xml_path)
                continue
            else:
                n_entries = len(solohk_entries)
                logger.info(f'{n_entries} entries returned from the database for {current_date}')

            if n_entries == 0:
                return

            # Write the output file using Jinja2
            # Load GSE test log template
            template = JENV.get_template(SOLO_HK_TEMPLATE)

            # Convert solo_hk_param table data into list of dictionaries
            param_sample_list = [self._convert_entry(current_entry)
                                 for current_entry in solohk_entries]

            # Build the output SOLO HK XML template render
            render = template.render(param_sample_list=param_sample_list)

            logger.info(f'Saving {xml_path}...  ({n_dates - i - 1} remaining)')
            # Create output file
            with open(xml_path, 'w') as outfile:
                outfile.write(render)
            if os.path.isfile(xml_path):
                output_files.append(xml_path)
            else:
                self.failed_files.append(xml_path)
                logger.error(f'Saving {xml_path} has failed')
                continue

            if queue_entries:
                queue_entries_to_clean.append(queue_entries[i])

        # Remove corresponding entry in pipeline.data_queue
        if self.clean_queue and queue_entries_to_clean:
            for current_entry in queue_entries_to_clean:
                if not delete_in_db(self.session, ProcessQueue,
                                    filters=(ProcessQueue.id ==
                                             current_entry['id']),
                                    tryouts=self.tryouts,
                                    wait=self.wait):
                    logger.error(f'{current_entry} has not been deleted from pipeline.data_queue table!')
                else:
                    logger.info(f'{current_entry} deleted from pipeline.data_queue table')

        # store list of output files as output target of the task
        self.outputs['solo_hk_files'].filepath = output_files

    def _convert_entry(self, current_entry):
        """

        :param current_entry:
        :return:
        """
        xml_element = {}
        xml_element['Name'] = current_entry['name']
        xml_element['TimeStampAsciiA'] = current_entry[
            'utc_time'].strftime(TIME_SQL_STRFORMAT)
        xml_element['Unit'] = current_entry['unit']
        xml_element['Description'] = current_entry['description']
        xml_element['EngineeringValue'] = current_entry['eng_value']
        xml_element['RawValue'] = current_entry['raw_value']

        return xml_element
