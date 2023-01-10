#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import os

from sqlalchemy import and_
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import load_only

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import PIPELINE_DATABASE, ROC_DELIVERED_ROOT
from roc.dingo.models.file import FileLog


__all__ = ['StoreDelivered']


class StoreDelivered(Task):
    """
    Parse ROC `delivered` folder, and store into database that all these
    files have been successfully delivered to ESA (column is_delivered)
    """
    plugin_name = 'roc.dingo'
    name = 'store_delivered'

    def add_targets(self):
        logger.debug('StoreDelivered() : add_targets')

        self.add_output(target_class=BaseTarget,
                        many=True,
                        identifier='store_delivered_results')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('StoreDelivered() : setup_inputs')

        # get the root file tree
        self.root = self.pipeline.get(
            'delivered', default=ROC_DELIVERED_ROOT, args=True)

        # ensure that there is / at the end
        self.root = os.path.join(self.root, '')

        # get the remove_files flag
        self.remove_files = self.pipeline.get(
            'remove_files', default=False, args=True)

    def run(self):

        logger.debug('StoreDelivered() : run')

        # Initialize inputs
        self.setup_inputs()

        # Initialize counters
        cpt_remove = 0
        cpt_to_store = 0
        nb_files_stored = 0

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get the file list
        to_store = []
        files = os.listdir(self.root)
        for file in files:
            if os.path.isfile(os.path.join(self.root, file)):
                to_store.append(file)

        logger.info(f'{len(to_store)} files in DELIVERED root')

        # Find corresponding entries in file_log

        name_filter = FileLog.public_filename.in_(to_store)
        is_not_delivered_filter = FileLog.is_delivered == False   # noqa: E712
        fields = ['id', 'basename', 'public_filename']

        try:
            query = self.session.query(FileLog).\
                options(load_only(*fields)).\
                filter(and_(name_filter, is_not_delivered_filter))
            results = query.all()
        except NoResultFound:
            logger.info('Nothing to be done')
        except Exception:
            logger.error('Query failed :')
            logger.error(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
        else:
            logger.info(f'{len(results)} files found in DB')
            cpt_to_store = len(results)

            item_dict = {}
            item_dict['is_delivered'] = True
            try:
                nb_files_stored = self.session.query(FileLog).\
                    filter(and_(name_filter, is_not_delivered_filter)).\
                    update(item_dict, synchronize_session=False)

            except Exception as e:
                logger.error(f'is_delivered update has failed: \n {e}')
                logger.error(
                    str(query.statement.compile(
                        dialect=postgresql.dialect(),
                        compile_kwargs={'literal_binds': True})))
            else:
                if nb_files_stored == cpt_to_store:
                    logger.info(
                        f'{nb_files_stored} files have been updated with '
                        'is_delievered = True')
                else:
                    logger.warning(
                        f'{nb_files_stored}/{cpt_to_store} files have been '
                        'updated with is_delievered = True')

            if self.remove_files:
                # Now, delete file in DELIVERED folder
                for r in results:
                    file_to_delete = os.path.join(self.root, r.public_filename)
                    if os.path.isfile(file_to_delete):
                        try:
                            os.remove(file_to_delete)
                        except FileNotFoundError as e:
                            logger.error(
                                'Unable to remove '
                                f'{r.public_filename}: \n {e}')
                        else:
                            cpt_remove += 1
                            logger.debug(f'Remove {r.public_filename}')

                if cpt_remove != cpt_to_store:
                    logger.warning(
                        f'{cpt_remove}/{cpt_to_store} shadow '
                        'delivered files have been removed')
                else:
                    logger.info(
                        f'{cpt_remove} shadow delivered files '
                        'have been removed')

        # number of stored files
        self.outputs['store_delivered_results'].data = {
            'files_to_be_stored': cpt_to_store,
            'files_stored': nb_files_stored,
            'removed_files': cpt_remove
        }
