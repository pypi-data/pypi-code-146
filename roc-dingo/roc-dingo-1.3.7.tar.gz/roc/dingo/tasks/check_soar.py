#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import urllib.request
import urllib.parse
from urllib.error import HTTPError
import json

from datetime import timedelta

from sqlalchemy import and_
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import load_only

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import PIPELINE_DATABASE
from roc.dingo.models.file import FileLog


__all__ = ['CheckSOARDataAvailability']


class CheckSOARDataAvailability(Task):
    """
    For each files flagged as delivered in DB, search SOAR if it available
    if yes : set is_archived
    """

    plugin_name = 'roc.dingo'
    name = 'check_soar'

    def add_targets(self):
        logger.debug('CheckSOARDataAvailability() : add_targets')

        # number of archived files
        self.add_output(target_class=BaseTarget,
                        many=True,
                        identifier='store_archived')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('CheckSOARDataAvailability() : setup_inputs')

        # get the TAP URL
        self.soar_tap_url = self.pipeline.get('url', args=True)

    def run(self):

        logger.debug('CheckSOARDataAvailability() : run')

        # Initialize inputs
        self.setup_inputs()

        # Initialize counters
        cpt_archived = 0          # files really stored as is_archived
        cpt_to_archive = 0        # files to be stored as is_archived
        cpt_files_to_archive = 0  # files delivered but not archived yet
        ids_archived = []
        min_start_time = None
        max_start_time = None

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Find entries in file_log with is_delivered and not is_archived
        is_not_archived_filter = FileLog.is_archived == False   # noqa: E712
        is_delivered_filter = FileLog.is_delivered == True   # noqa: E712
        fields = ['id', 'basename', 'public_filename']

        try:
            query = self.session.query(FileLog).\
                options(load_only(*fields)).\
                filter(and_(is_not_archived_filter, is_delivered_filter))
            results = query.all()
        except Exception:
            logger.error('Query failed :')
            logger.error(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
            results = []

        cpt_files_to_archive = len(results)
        logger.info(f'{cpt_files_to_archive} files to store as is_archived')

        # Find min anx max times for these files
        # This will be use to filter the TAP query, in order to limit
        # the data volume to retreive
        try:
            query_min = self.session.query(
                func.min(FileLog.start_time), func.max(FileLog.end_time)).\
                filter(and_(is_not_archived_filter, is_delivered_filter))
            min_start_time = query_min.one()[0]
            max_start_time = query_min.one()[1]
        except Exception:
            logger.error('Query failed :')
            logger.error(
                str(query_min.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))

        if min_start_time is not None:
            min_start_time = min_start_time - timedelta(days=1)
            min_start_time = min_start_time.strftime('%Y-%m-%d')
            logger.debug(f'Filtering on begin_time > {min_start_time}')

        if max_start_time is not None:
            max_start_time = max_start_time + timedelta(days=1)
            max_start_time = max_start_time.strftime('%Y-%m-%d')
            logger.debug(f'Filtering on begin_time < {max_start_time}')

        # Build URL of the query
        select_query = ['SELECT', 'file_name', 'FROM', 'v_public_files']

        where_query = ['WHERE', 'instrument', '=', '%27RPW%27']
        if min_start_time is not None:
            gt = urllib.parse.quote('>')
            where_query += ['AND', 'begin_time', gt, f'%27{min_start_time}%27']
        if max_start_time is not None:
            lt = urllib.parse.quote('<')
            where_query += ['AND', 'begin_time', lt, f'%27{max_start_time}%27']

        order_query = ['ORDER', 'BY', 'archived_on', 'ASC']

        tap_query = '+'.join(select_query + where_query + order_query)
        query_params = '&'.join([
            'REQUEST=doQuery',
            'LANG=ADQL',
            'FORMAT=json',
            f'QUERY={tap_query}'
        ])
        query_url = f'{self.soar_tap_url}/sync?{query_params}'
        logger.debug(query_url)

        # Run TAP query
        data = None
        try:
            logger.info(f'Querying --> {query_url}')
            data = CheckSOARDataAvailability.soar_run_query(query_url)
        except HTTPError as e:
            logger.error(f'SOAR TAP query has failed ({query_url})')
            logger.error(e)
            logger.exception(e.msg)

        # re-organise data
        archived_data = [d[0] for d in data['data']]

        for r in results:
            if r.public_filename in archived_data:
                logger.info(f'{r.basename} -> is_archived')
                ids_archived.append(r.id)
            else:
                logger.warning(f'{r.basename} not archived')

        cpt_to_archive = len(ids_archived)

        # update DB
        try:
            id_filter = FileLog.id.in_(ids_archived)
            query = self.session.query(FileLog).filter(id_filter)

            item = {}
            item['is_archived'] = True
            cpt_archived = query.update(item, synchronize_session=False)
        except Exception as e:
            logger.error(f'is_archived update has failed: \n {e}')
            logger.error(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))

        if cpt_archived != cpt_to_archive:
            # this should not happen
            logger.warning(f'[{cpt_archived}/{cpt_to_archive}] files '
                           'stored as is_archived')
        else:
            logger.info(f'{cpt_archived} files stored as is_archived')

        # number of archived files
        self.outputs['store_archived'].data = {
            'files_to_archive': cpt_files_to_archive,
            'files_archived': cpt_archived,
        }

    @staticmethod
    def soar_run_query(query: str) -> dict:
        """
        Runs a ADQL query on SOAR TAP server and return the data table.

        :param query: ADQL query_adql full URL string
        :return: a dictionary containing the query results
        """
        with urllib.request.urlopen(query) as url:
            data = json.loads(url.read().decode())
        return data
