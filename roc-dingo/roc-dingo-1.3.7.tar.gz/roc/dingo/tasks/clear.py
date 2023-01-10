#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.task import Task
from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import and_

from roc.dingo.constants import PIPELINE_DATABASE, PIPELINE_TABLES, TIME_INPUT_STRFORMAT
from roc.dingo.exceptions import DbQueryError
from roc.dingo.models.packet import TmLog, TcLog

__all__ = ['ClearRocDb']

# ________________ Global Variables _____________
# (define here the global variables)


# ________________ Class Definition __________
# (If required, define here classes)


# ________________ Global Functions __________
# (If required, define here global functions)
from roc.dingo.tools import valid_time


class ClearRocDb(Task):

    plugin_name = 'roc.dingo'
    name = 'clear_rocdb'

    def run(self):

        # get the pipeline connector and get the database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get list of possible tables to delete
        available_table_list = list(PIPELINE_TABLES.keys())

        # Get tables to delete
        table_list = self.pipeline.get('tables',
                                            default=available_table_list,
                                            args=True)

        # Loop over table(s) to clear
        for table_name in table_list:

            if table_name not in available_table_list:
                logger.warning(f'{table_name} not found in pipeline '
                               f'table list {available_table_list}, skip it')
                continue
            else:
                # Get database model representation
                representation = PIPELINE_TABLES[table_name]

            # Initialize filter(s)
            query_filters = []

            # Get time for filtering
            if table_name == 'tm_log':
                time = TmLog.utc_time
            elif table_name == 'tc_log':
                time = TcLog.utc_time
            else:
                time = None

            if time:
                # If --start_time option is set, add an lower time limit
                start_time = valid_time(
                    self.pipeline.get('start_time',
                                      default=[None],
                                      args=True)[0])
                if start_time:
                    query_filters.append(time <= start_time)

                # If --end_time option is set, add an lower time limit
                end_time = valid_time(
                    self.pipeline.get('end_time',
                                      default=[None],
                                      args=True)[0])
                if end_time:
                    query_filters.append(time >= end_time)

            # If --force keyword is True, then do not ask before deleting
            force = self.pipeline.get('force', default=False, args=True)

            # build query
            query = self.session.query(representation)

            try:
                entries_to_clear = (
                    query
                        .filter(and_(*query_filters))
                        .all()
                )
            except NoResultFound:
                logger.info(f'No entry found for table {table_name} in the database '
                            f'(query_filters={query_filters})')
            except:
                raise DbQueryError(f'Deletion of table {table_name} has failed!')
            else:
                # Number of entries found
                entry_count = query.count()
                if entry_count == 0:
                    logger.info(f'No entry found for table {table_name} in the database '
                                f'(query_filters={query_filters})')
                else:
                    logger.info(f'{entry_count} entries to delete have been found in {table_name} '
                                f'(query_filters={query_filters})')

                    if not force:
                        answer = input(f'ENTER TABLE NAME TO CONFIRM THE DELETION ["{table_name}"]: ')
                    else:
                        answer = table_name

                    if answer == table_name:
                        logger.debug(f'Deleting {entry_count} entries from table {table_name} ...')
                        for current_entry in entries_to_clear:
                            logger.debug(f'Deleting {current_entry.__dict__}')
                            self.session.delete(current_entry)

                        self.session.commit()
                        logger.info(f'{entry_count} entries have been removed from table {table_name}'
                                    f' (query_filters={query_filters})')
                    else:
                        logger.info(f'Table {table_name} has not been cleaned')
