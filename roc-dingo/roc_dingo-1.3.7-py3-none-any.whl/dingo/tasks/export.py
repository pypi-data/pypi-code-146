#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to query the pipeline database."""
import json
import os

from sqlalchemy import and_

from roc.dingo.tools import query_db, valid_time

try:
    from poppy.core.logger import logger
    from poppy.core.db.connector import Connector
    from poppy.core.task import Task
    from poppy.core.target import PyObjectTarget, FileTarget
    from poppy.core.conf import settings
except:
    print("POPPy framework seems to not be installed properly!")

from roc.dingo.constants import PIPELINE_DATABASE, SQL_LIMIT, PIPELINE_TABLES, \
    TIME_OUTPUT_STRFORMAT, TIME_INPUT_STRFORMAT

__all__ = ["ExportToJson"]

# ________________ Global Variables _____________
# (define here the global variables)


# ________________ Class Definition __________
# (If required, define here classes)

class ExportToJson(Task):
    """
    Task to export content of the database into a JSON file.
    """
    plugin_name = 'roc.dingo'
    name = "export_to_json"

    @Connector.if_connected(PIPELINE_DATABASE)
    def run(self):

        # Initialize output dictionary
        output_json_dict = {}

        # get the pipeline connector and get the database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get list of pipeline database tables to query
        table_list = self.pipeline.get('tables',
                                       default=list(PIPELINE_TABLES.keys()), args=True)

        # If --start_time keyword value is set, add an lower time limit
        start_time = valid_time(self.pipeline.get('start_time',
                                       default=[None],
                                                  args=True)[0])

        # If --end_time keyword value is set, add an upper time limit
        end_time = valid_time(self.pipeline.get('end_time',
                                     default=[None],
                                    args=True)[0])

        # If --creation-time is set to True, then
        # filtering packet_log and file_log table entries using creation time
        # instead of insertion time (not possible for invalid_packet_log)
        creation_time_flag = self.pipeline.get('creation-time',
                                       default=False, args=True)

        for current_table in table_list:

            logger.info(f'Exporting entries for {current_table}')

            # Get table model
            current_model = PIPELINE_TABLES[current_table]

            if current_table == 'packet_log':
                # Define time to use for start_time/end_time filter
                # Default is insertion time
                if creation_time_flag:
                    time = current_model.utc_time
                else:
                    time = current_model.insertion_time
            elif current_table == 'invalid_packet_log':
                time = current_model.insertion_time
            elif current_table == 'file_log':
                if creation_time_flag:
                    time = current_model.file_creation_date
                else:
                    time = current_model.file_insert_date
            else:
                logger.warning(f'Unknown table: {current_table}')
                continue

            # Add input filters
            filters = []

            if start_time:
                filters.append(time >= start_time) # greater or equal than ...

            if end_time:
                filters.append(time < end_time) # lesser than ...

            filters = and_(*filters)

            # Retrieve --limit keyword value
            limit = self.pipeline.get('limit',
                                      default=[SQL_LIMIT],
                                      args=True)[0]

            # get entries from pipeline table in ROC database
            # Order by increasing time
            entries_dict = query_db(self.session, current_model,
                                    filters=filters,
                                    limit=limit,
                                    order_by=time,
                                    to_dict='records',
                                    )
            entry_count = len(entries_dict)
            if entry_count == limit:
                logger.warning(f'Row limit has been reached {limit}')
            elif entry_count == 0:
                logger.info(f'No entry found in {current_model}')
            else:
                output_json_dict[current_table] = entries_dict

        if not output_json_dict:
            return

        # Build output file path
        output_json = self.pipeline.get('output_json', default=None)
        if output_json is None:

            database_name = 'rocdb'
            for database in self.pipeline.properties.configuration["pipeline.databases"]:
                if database['identifier'] == settings.PIPELINE_DATABASE:
                    database_name = database['login_info']['database']
                    break

            filename_field_list = [database_name,
                                   "-".join(table_list)]
            if start_time:
                filename_field_list.append(
                    start_time.strftime(TIME_OUTPUT_STRFORMAT))
            if end_time:
                filename_field_list.append(
                    end_time.strftime(TIME_OUTPUT_STRFORMAT))
            output_json = "_".join(filename_field_list) + ".json"

        output_json_path = os.path.join(self.pipeline.output, output_json)
        # Write output JSON file
        with open(output_json_path, 'w') as json_buff:
            json.dump(output_json_dict, json_buff)
        logger.info(f'{output_json_path} saved')




# ________________ Global Functions __________
# (If required, define here global functions)

