#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import os
import re
import numpy as np

from datetime import datetime

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import PIPELINE_DATABASE, \
    ROC_DATA_ROOT, FILE_LEVEL_LIST, \
    DATA_ALLOWED_EXTENSIONS, SPICE_KERNEL_ALLOWED_EXTENSIONS, \
    LEVEL_2_INST, LEVEL_3_INST, SPICE_KERNEL_TYPES, \
    LEVEL_BY_MONTH, LEVEL_BY_DAY

__all__ = ['ParseFileTree']


class ParseFileTree(Task):
    """
    Parse ROC file tree and keep unlogged files
    """
    plugin_name = 'roc.dingo'
    name = 'parse_file_tree'

    def add_targets(self):
        logger.debug('ParseFileTree() : add_targets')

        self.add_output(target_class=BaseTarget,
                        many=True,
                        identifier='roc_data_files')

        self.add_output(target_class=BaseTarget,
                        many=True,
                        identifier='roc_dir_list')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('ParseFileTree() : setup_inputs')

        # get the root file tree
        self.root = self.pipeline.get('root', default=ROC_DATA_ROOT, args=True)
        # ensure that there is / at the end
        self.root = os.path.join(self.root, '')

        # get the date directory to include
        self.date = self.pipeline.get('date',
                                      default=None,
                                      args=True)

        # get the level directories to include
        # default = all levels but spice kerlels (SK)
        all_levels = FILE_LEVEL_LIST.copy()
        all_levels.remove('SK')
        self.level_list = self.pipeline.get('level',
                                            default=all_levels,
                                            args=True)

        # be sure that levels are read in a logical way
        # (set by file_level_list)
        # in order to parse L0 before L1, HK before L0, ...
        np_file_level_list = np.array(FILE_LEVEL_LIST)
        self.level_list = np_file_level_list[
            np.array([(i in self.level_list) for i in np_file_level_list])]
        logger.debug(self.level_list)

        # get a database session
        self.db = Connector.manager[PIPELINE_DATABASE]

        # get the former-versions flag
        self.no_former_versions = self.pipeline.get(
            'no_former_versions', default=False, args=True)

    @Connector.if_connected(PIPELINE_DATABASE)
    def run(self):

        # Initialize inputs
        self.setup_inputs()

        logger.debug('LogFileToDb() : run')

        # Initialize list of ROC data files to insert into db
        file_list = {}

        logger.info('Root directory: {}'.format(self.root))
        logger.debug('Directories to include: {}, ({})'.format(
            ', '.join(self.level_list), len(self.level_list)))

        level_inst = {}
        for level in FILE_LEVEL_LIST:
            level_inst[level] = ['']
            if level == 'L2':
                level_inst[level] = LEVEL_2_INST
            if level == 'L3':
                level_inst[level] = LEVEL_3_INST
            if level == 'SK':
                level_inst[level] = SPICE_KERNEL_TYPES

        # if a date is specified, is it a day or a month ?
        set_date_month = False
        set_date_day = False
        if self.date:
            if len(self.date.split('/')) == 3:
                set_date_day = True
            elif len(self.date.split('/')) == 2:
                set_date_month = True
        else:
            self.date = ''

        # Set the directories to parse
        dir_list = []

        for file_level in self.level_list:
            if set_date_day and file_level not in LEVEL_BY_DAY:
                logger.info(
                    'Skipping {}, not available on a day basis'.format(
                        file_level))
                continue
            if set_date_month and \
                file_level not in LEVEL_BY_MONTH and \
                    file_level not in LEVEL_BY_DAY:
                logger.info(
                    'Skipping {}, not available on a month basis'.format(
                        file_level))
                continue

            for inst in level_inst[file_level]:
                if file_level == 'SK':
                    dir_list.append(os.path.join(inst))
                else:
                    dir_list.append(os.path.join(file_level, inst, self.date))

        logger.debug(dir_list)

        for dir_item in dir_list:
            file_level = dir_item.split('/')[0]

            logger.debug('========== %s ==========' % dir_item)
            logger.debug('%s', os.path.join(self.root, dir_item))
            for dirName, subdirList, fileList in \
                    os.walk(os.path.join(self.root, dir_item)):
                logger.debug('-----------------------------')
                logger.debug('Found directory: %s' % dirName)
                logger.debug('Found subdirList: %s' % subdirList)
                logger.debug('Found fileList: %s' % fileList)
                logger.debug('-----------------------------')

                if self.no_former_versions and 'former_versions' in dirName:
                    logger.debug('Skipping %s (-nf specified)' % dirName)
                    continue

                for fname in fileList:
                    # Skipping hidden files
                    if re.match(r'\.', fname):
                        logger.debug('Skipping hidden file %s' % fname)
                        continue

                    # Skipping non allowed extensions
                    file_name, file_extension = os.path.splitext(fname)
                    if not file_extension.replace('.', '') \
                       in DATA_ALLOWED_EXTENSIONS \
                       and not file_extension.replace('.', '') \
                       in SPICE_KERNEL_ALLOWED_EXTENSIONS:
                        logger.debug('Skipping non authorized %s' % fname)
                        continue

                    full_name = os.path.join(dirName, fname)
                    logger.debug('\t%s' % full_name)
                    file_list[fname] = {
                        'filepath': full_name,
                        'size': os.stat(full_name).st_size,
                        'creation_time': datetime.utcfromtimestamp(
                            int(os.path.getmtime(full_name)))
                    }

        logger.info('{} files found in root'.format(str(len(file_list))))

        self.outputs['roc_data_files'].data = file_list
        self.outputs['roc_dir_list'].data = dir_list
