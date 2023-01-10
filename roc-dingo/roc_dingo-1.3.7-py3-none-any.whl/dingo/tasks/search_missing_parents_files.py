#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import os


from sqlalchemy import and_
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import load_only

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import PIPELINE_DATABASE, ROC_DATA_ROOT
from roc.dingo.models.file import FileLog


__all__ = ['SearchMissingParentsFiles']


class SearchMissingParentsFiles(Task):
    """
    Parse ROC db and search for files with Missing Parents in the error_log
    """
    plugin_name = 'roc.dingo'
    name = 'search_missing_parents_files'
    files_to_update = []

    def add_targets(self):
        logger.debug('SearchMissingParentsFiles() : add_targets')

        self.add_output(target_class=BaseTarget, many=True,
                        identifier='roc_data_files_to_update')

        # useless here but necessary for LogFileToDb()
        self.add_output(target_class=BaseTarget, many=True,
                        identifier='roc_data_files_to_insert')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('SearchMissingParentsFiles() : setup_inputs')

        # get the root file tree
        self.root = self.pipeline.get('root', default=ROC_DATA_ROOT, args=True)
        # ensure that there is / at the end
        self.root = os.path.join(self.root, '')

    def run(self):

        logger.debug('SearchMissingParentsFiles() : run')

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Initialize inputs
        self.setup_inputs()

        # Initialize list of ROC data files to update into db
        file_list = {}

        logger.debug('Root directory: {}'.format(self.root))

        # Define relevant fields to retreive
        fields = ['basename', 'dirname', 'creation_time', 'size']

        # Search files with "Missing parents in error_log"
        missing_filter = FileLog.error_log.like('%Missing parents%')
        not_removed_filter = FileLog.is_removed == False  # noqa: E712
        try:
            query = self.session.query(FileLog).\
                options(load_only(*fields)).\
                filter(and_(missing_filter, not_removed_filter))
            logger.debug(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
            results = query.all()
        except Exception:
            logger.error('Query has failed: \n {!s}'.format(
                query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})
            ))
        else:
            for item in results:
                # adding an entry in file_list
                file_list[item.basename] = {
                    'filepath': os.path.join(
                        self.root, item.dirname, item.basename),
                    'size': item.size,
                    'creation_time': item.creation_time
                }

        # Returns outputs
        self.outputs['roc_data_files_to_update'].data = file_list
        logger.info('{} files to update'.format(str(len(file_list))))
        if len(file_list) == 0:
            self.outputs['roc_data_files_to_update'].is_empty = True

        self.outputs['roc_data_files_to_insert'].data = {}
        self.outputs['roc_data_files_to_insert'].is_empty = True
