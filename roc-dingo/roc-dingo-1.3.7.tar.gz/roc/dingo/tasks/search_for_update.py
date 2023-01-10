#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Search for items in file_log to be updated
"""

import os

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import load_only

from datetime import datetime

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import \
    PIPELINE_DATABASE, \
    ROC_DATA_ROOT
from roc.dingo.models.file import FileLog

__all__ = ['SearchForUpdate']


class SearchForUpdate(Task):
    """
    Parse ROC file tree and synchronize with the the ROC database
    """
    plugin_name = 'roc.dingo'
    name = 'search_for_update'
    files_to_check = []
    files_to_insert = []
    files_to_update = []

    def add_targets(self):
        logger.debug('SearchForUpdate() : add_targets')

        self.add_output(target_class=BaseTarget, many=True,
                        identifier='roc_data_files_to_update')
        self.add_output(target_class=BaseTarget, many=True,
                        identifier='roc_data_files_to_insert')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('SearchForUpdate() : setup_inputs')

        # get the root file tree
        self.root = self.pipeline.get('root', default=ROC_DATA_ROOT, args=True)
        # ensure that there is / at the end
        self.root = os.path.join(self.root, '')

    def run(self):

        logger.debug('SearchForUpdate() : run')

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Initialize inputs
        self.setup_inputs()

        # Initialize outputs
        self.files_to_update = {}

        # Define filters to check file_log entry to update
        update_filter = FileLog.to_update == True  # noqa: E712

        # Define relevant fields to retreive
        fields = ['basename', 'dirname', 'creation_time', 'size']

        try:
            query = self.session.query(FileLog).\
                options(load_only(*fields)).\
                filter(update_filter)
            logger.debug(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
            results = query.all()
        except Exception:  # pragma: no cover
            logger.error('Query failed :')
            logger.error(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
        else:
            for item in results:
                full_name = os.path.join(
                    self.root, item.dirname, item.basename)

                # test if the file is still here
                if os.path.exists(full_name):
                    # do not rely on database creation_time and size
                    size = os.stat(full_name).st_size,
                    creation_time = datetime.utcfromtimestamp(
                        int(os.path.getmtime(full_name)))
                else:
                    # it was removed, keep the values in db
                    logger.info(f'File {item.basename} is not anymore '
                                'in the file system -> mark as removed')
                    item.is_removed = True
                    item.state = 'OK'
                    item.error_log = None
                    item.to_update = False
                    self.session.commit()
                    # do not continue with this file
                    continue

                self.files_to_update[item.basename] = {
                    'filepath': os.path.join(
                        self.root,
                        item.dirname,
                        item.basename),
                    'creation_time': creation_time,
                    'size': size,
                }

        # Returns outputs
        self.outputs['roc_data_files_to_update'].data = self.files_to_update
        logger.info(
            '{} files to update'.format(str(len(self.files_to_update))))
        if len(self.files_to_update) == 0:
            self.outputs['roc_data_files_to_update'].is_empty = True

        self.outputs['roc_data_files_to_insert'].data = {}
        self.outputs['roc_data_files_to_insert'].is_empty = True
