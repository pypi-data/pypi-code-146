#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import os

from sqlalchemy import and_, or_
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import load_only

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import \
    PIPELINE_DATABASE, \
    ROC_DATA_ROOT, \
    FILE_LEVEL_LIST
from roc.dingo.models.file import FileLog

__all__ = ['CheckFileInDb']


class CheckFileInDb(Task):
    """
    Parse ROC file tree and synchronize with the the ROC database
    """
    plugin_name = 'roc.dingo'
    name = 'check_file_in_db'
    files_to_check = []
    files_to_insert = []
    files_to_update = []

    def add_targets(self):
        logger.debug('CheckFileInDb() : add_targets')

        self.add_input(target_class=BaseTarget, many=True,
                       identifier='roc_data_files')

        self.add_input(target_class=BaseTarget, many=True,
                       identifier='roc_dir_list')

        self.add_output(target_class=BaseTarget, many=True,
                        identifier='roc_data_files_to_insert')

        self.add_output(target_class=BaseTarget, many=True,
                        identifier='roc_data_files_to_update')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('CheckFileInDb() : setup_inputs')

        # get files to check
        self.files_to_check = self.inputs['roc_data_files'].data

        # get the directory list
        self.dir_list = self.inputs['roc_dir_list'].data

        # get the root file tree
        self.root = self.pipeline.get('root', default=ROC_DATA_ROOT, args=True)
        # ensure that there is / at the end
        self.root = os.path.join(self.root, '')

        # get the directories to include
        self.level_list = self.pipeline.get('level',
                                            default=FILE_LEVEL_LIST,
                                            args=True)
        # get the force flag
        self.force = self.pipeline.get('force', default=False, args=True)

    def run(self):

        logger.debug('CheckFileInDb() : run')

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Initialize inputs
        self.setup_inputs()

        # Initialize outputs
        self.files_to_insert = self.files_to_check
        self.files_to_update = {}

        # Define filters to check file_log entry existence
        level_filter = FileLog.level.in_(self.level_list)
        dirname_filter = [
            FileLog.dirname.like(
                '%' + d.replace(self.root, '').rstrip(os.sep) + '%')
            for d in self.dir_list
        ]

        # Define relevant fields to retreive
        fields = ['basename', 'dirname', 'creation_time', 'size', 'is_removed']

        try:
            query = self.session.query(FileLog).\
                options(load_only(*fields)).\
                filter(and_(level_filter, or_(*dirname_filter)))
            logger.debug(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
            results = query.all()
        except Exception:
            logger.error('Query failed :')
            logger.error(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
        else:
            logger.debug('ok')
            for item in results:
                # find the corresponding file in the entry collection
                try:
                    item_file = self.files_to_insert.pop(item.basename)
                except Exception:
                    if not item.is_removed:
                        item.is_removed = True
                        item.state = 'OK'
                        item.error_log = None
                        self.session.commit()
                        logger.info(
                            'File {} in database not in root -> '
                            'mark as removed'.format(item.basename))
                    # else : the file was was already marked as removed
                    continue

                # Get item parameters
                creation_time = item_file['creation_time']
                size = item_file['size']
                dirname = os.path.dirname(
                    item_file['filepath']).replace(self.root, '')

                # dirname or size or creation_time is different => update
                if self.force:
                    logger.debug(
                        '{} to be updated [force]'.format(item.basename))
                    self.files_to_update[item.basename] = item_file
                elif (item.creation_time != creation_time) | \
                     (item.size != size) | \
                     (item.dirname != dirname):
                    self.files_to_update[item.basename] = item_file
                    logger.debug(
                        '{} already in database - has to be updated :'
                        '\n\tDirname : {} (db) / {} (fs)'
                        '\n\tSize : {} (db) / {} (fs)'
                        '\n\tDate : {} (db) / {} (fs)'.format(
                            item.basename,
                            item.dirname, dirname,
                            str(item.size), str(size),
                            str(item.creation_time), str(creation_time)))
                else:
                    logger.debug(
                        '{} already in database'.format(item.basename))
                    if item.is_removed:
                        # for any reason, file was marked as removed
                        logger.debug('-> is_removed set to False')
                        item.is_removed = False
                        self.session.commit()

        # Returns outputs
        self.outputs['roc_data_files_to_insert'].data = self.files_to_insert
        logger.info(
            '{} files to insert'.format(str(len(self.files_to_insert))))
        if len(self.files_to_insert) == 0:
            self.outputs['roc_data_files_to_insert'].is_empty = True

        self.outputs['roc_data_files_to_update'].data = self.files_to_update
        logger.info(
            '{} files to update'.format(str(len(self.files_to_update))))
        if len(self.files_to_update) == 0:
            self.outputs['roc_data_files_to_update'].is_empty = True
