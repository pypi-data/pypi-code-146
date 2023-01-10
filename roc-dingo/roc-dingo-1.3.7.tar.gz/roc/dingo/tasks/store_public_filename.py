#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import os
import re
from csv import DictReader

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import load_only

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import PIPELINE_DATABASE, \
    DATA_ALLOWED_EXTENSIONS, ROC_PUBLIC_DATA_ROOT
from roc.dingo.models.file import FileLog

import h5py
from spacepy.pycdf import CDF


__all__ = ['StorePublicFilename']


class StorePublicFilename(Task):
    """
    Parse ROC public tree, and for each file get the CDAG_PARENT attribute,
    search for the associated file in the file_log table, and store the
    public filename for this file
    """
    plugin_name = 'roc.dingo'
    name = 'store_public_filename'

    def add_targets(self):
        self.add_output(target_class=BaseTarget,
                        many=True,
                        identifier='store_public_filename_results')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('StorePublicFilename() : setup_inputs')

        # get the public root file tree
        self.root = self.pipeline.get(
            'public', default=ROC_PUBLIC_DATA_ROOT, args=True)

        # ensure that there is / at the end
        self.root = os.path.join(self.root, '')

    def run(self):

        logger.debug('StorePublicFilename() : run')

        # Initialize inputs
        self.setup_inputs()

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get the files already in database (public_* not null)
        fields = ['id', 'basename', 'public_filename', 'public_dirname']
        public_not_null = FileLog.public_filename.isnot(None)

        try:
            query = self.session.query(FileLog).\
                options(load_only(*fields)).\
                filter(public_not_null)
            results = query.all()
            logger.info(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))

            files_in_db = [r.public_filename for r in results]
        except Exception:
            logger.error('Query failed :')
            logger.error(
                str(query.statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True})))
            files_in_db = []

        # Levels to be delivered
        levels = ['L0', 'L1', 'L2', 'L3']

        # Files to be stored
        to_store = []

        # Get the file list
        for level in levels:
            db_file = os.path.join(self.root, level, 'db.csv')
            with open(db_file, 'r') as db:
                lines = DictReader(db, dialect='unix')
                for line in lines:
                    filepath = line['relative_filepath']
                    public_filename = os.path.basename(filepath)

                    if public_filename not in files_in_db:
                        public_dirname = os.path.join(
                            level,
                            os.path.dirname(filepath)
                        )
                        item = {
                            'public_filename': public_filename,
                            'public_dirname': public_dirname
                        }
                        to_store.append(item)

        logger.info(f'{len(to_store)} public files to store in DB')

        cpt_to_store = len(to_store)
        cpt_err = 0
        cpt_cur = 0
        cpt_new = 0

        # For each file to be inserted, open it and read the CDAG_PARENT
        # attribute
        for item in to_store:
            cpt_cur += 1
            filepath = os.path.join(
                self.root,
                item['public_dirname'],
                item['public_filename'])
            cdag_parent = None
            former_version = ('former_versions' in item['public_dirname'])

            attrs_keys = []
            attrs = {}

            logger.info(f'[{cpt_cur}/{cpt_to_store}] Reading {filepath}')
            if '.cdf' in item['public_filename']:
                try:
                    with CDF(filepath) as fh:
                        attrs_keys = [key for key, val in fh.attrs.items()]
                        attrs = \
                            {key: val[...][0] for key, val in fh.attrs.items()}
                except Exception as e:
                    logger.error(f'Error while reading {filepath} : {e}')
                    logger.debug('Break to next')
                    cpt_err += 1
                    continue

            if '.h5' in item['public_filename']:
                try:
                    with h5py.File(filepath, 'r') as fh:
                        attrs_keys = [key for key in fh.attrs.keys()]
                        attrs = {val[0]: val[1] for val in fh.attrs.items()}
                except Exception as e:
                    logger.error(f'Error while reading {filepath} : {e}')
                    logger.debug('Break to next')
                    cpt_err += 1
                    continue

            if 'CDAG_PARENT' in attrs_keys:
                cdag_parent = attrs['CDAG_PARENT']
            elif former_version and 'CDAG_PARENTS' in attrs_keys:
                # some old files have CDAG_PARENT*S* attribute
                cdag_parent = attrs['CDAG_PARENTS']
            else:
                logger.warning(f'No attribute found for {filepath}')
                logger.debug('Break to next')
                cpt_err += 1
                continue

            # search for the cdag parent
            logger.info(f'Parent is {cdag_parent}')
            basename_filter = FileLog.basename == cdag_parent

            file_to_be_added = False

            try:
                query = self.session.query(FileLog).\
                    filter(basename_filter)
                result = query.one()
            except MultipleResultsFound:
                logger.warning(f'Multiple files found for {cdag_parent}')
                result = None
            except NoResultFound:
                logger.warning(f'No files found for {cdag_parent}')
                file_to_be_added = True
                result = None

            if result is None and not file_to_be_added:
                cpt_err += 1
                logger.debug('Break to next')
                continue

            # if needed, add the FileLog object in DB, to keep track
            # of all the delivered objects
            if file_to_be_added:
                new_item = {}
                new_item['basename'] = cdag_parent

                # search for version number
                re_ext = '|'.join(DATA_ALLOWED_EXTENSIONS)
                res = re.search(
                    r'(v|V)([0-9a-zA-Z]+)\.(' + re_ext + ')',
                    cdag_parent)
                res_id = 2

                if res:
                    new_item['version'] = res.group(res_id)
                else:
                    logger.warning(
                        f'No version number found for {cdag_parent}')
                    cpt_err += 1
                    logger.debug('Break to next')
                    continue

                product = re.sub(
                    r'^([^\.]+)_V[0-9U]+\.[^$]+$', r'\1', cdag_parent)
                new_item['product'] = product

                new_item['state'] = 'OK'
                new_item['status'] = 'Terminated'
                new_item['creation_time'] = attrs['Generation_date'].strip()
                if new_item['creation_time'] == '':
                    new_item['creation_time'] = None

                new_item['insert_time'] = 'now()'
                new_item['dirname'] = item['public_dirname']
                new_item['dataset_id'] = attrs['Dataset_ID']
                new_item['level'] = item['public_dirname'].split('/')[0]
                if new_item['level'] not in levels:
                    logger.warning(
                        'Wrong file level found for '
                        f'{cdag_parent} : {new_item["level"]}')
                    cpt_err += 1
                    logger.debug('Break to next')
                    continue

                new_item['is_latest'] = False
                new_item['is_removed'] = True
                # URL is set no NULL because file is removed

                # Add the new FileLog
                new_file = FileLog(**new_item)
                try:
                    self.session.add(new_file)
                    # force flush to be sure to get the insertion error
                    # if needed
                    self.session.flush()
                except Exception as e:
                    logger.error(f'Add of {cdag_parent} has failed: \n {e}')
                    cpt_err += 1
                    continue
                else:
                    cpt_new += 1
                    logger.info(f'{cdag_parent} added successfully')

                # And retreive it
                try:
                    query = self.session.query(FileLog).\
                        filter(basename_filter)
                    result = query.one()
                except Exception as e:
                    logger.error(
                        f'Retreive of {cdag_parent} has failed: '
                        f'\n {e}')
                    cpt_err += 1
                    continue

            # update the object
            item_dict = {}
            item_dict['public_filename'] = item['public_filename']
            item_dict['public_dirname'] = item['public_dirname']

            try:
                query.update(item_dict)
            except Exception as e:
                logger.error(f'Update of {cdag_parent} has failed: \n {e}')
                cpt_err += 1
            else:
                logger.info(f'{cdag_parent} updated successfully')

        cpt_ok = cpt_to_store - cpt_err
        logger.info(f'{cpt_ok} files have been stored')
        if cpt_err > 0:
            logger.warning(f'{cpt_err} files in error')

        # number of public_filenames stored
        self.outputs['store_public_filename_results'].data = {
            'files_stored': cpt_ok,
            'files_added': cpt_new
        }
