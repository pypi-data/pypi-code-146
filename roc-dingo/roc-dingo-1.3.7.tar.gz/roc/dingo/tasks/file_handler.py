#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Tasks for handling files processed by DINGO plugin."""

import os
from pathlib import Path

from poppy.core.logger import logger
from poppy.core.task import Task

__all__ = ['MoveProcessedFiles', 'MoveFailedFiles']

from roc.dingo.tools import safe_move


class MoveProcessedFiles(Task):
    """Task to move input list of well processed files in a given target directory."""
    plugin_name = 'roc.dingo'
    name = 'move_processed_files'

    def setup_inputs(self):

        # See if --no-move keyword is defined
        self.no_move = self.pipeline.get('no_move', default=False, args=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Get or create processed_files_dir from pipeline properties
        self.processed_files_dir = self.pipeline.get(
            'processed_files_dir', default=[None], create=True)[0]

    def run(self):

        try:
            self.setup_inputs()
        except:
            logger.exception(
                'Initializing inputs for task MoveProcessedFiles has failed!')
            self.pipeline.exit()
            return

        if self.no_move:
            logger.debug(
                'Skip MoveProcessedFiles task')
            return

        if not self.processed_files:
            logger.debug(
                'Input list of processed files is empty: skip MoveProcessedFiles task')
            return
        else:

            if not self.processed_files_dir:
                logger.debug(
                    'processed_files_dir argument not passed, skip task')
                return

            # Create folder if it does not exist
            Path(self.processed_files_dir).mkdir(parents=True, exist_ok=True)

            for current_file in self.processed_files:
                logger.info(f'Moving {current_file} into {self.processed_files_dir}')
                if not safe_move(current_file, self.processed_files_dir):
                    logger.error(f'Cannot move {current_file} into {self.processed_files_dir}')


class MoveFailedFiles(Task):
    """Move failed files found
    into a target directory."""
    plugin_name = 'roc.dingo'
    name = 'move_failed_files'

    def setup_inputs(self):

        # See if --no-move keyword is defined
        self.no_move = self.pipeline.get('no_move', default=False, args=True)

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create failed_files_dir list from pipeline properties
        self.failed_files_dir = self.pipeline.get(
            'failed_files_dir', default=[None], create=True)[0]

    def run(self):

        try:
            self.setup_inputs()
        except:
            logger.exception(
                'Initializing inputs for task MoveFailedFiles has failed!')
            self.pipeline.exit()
            return

        if self.no_move:
            logger.debug(
                'Skip current task MoveFailedFiles')
            return

        if not self.failed_files:
            logger.debug(
                'Input list of failed files is empty: skip MoveFailedFiles task')
            return
        else:

            if not self.failed_files_dir:
                logger.warning(f'There are failed files but failed_files_dir value is not defined, skip MoveFailedFiles task')
                return

            # Create folder if it does not exist
            Path(self.failed_files_dir).mkdir(parents=True, exist_ok=True)

            for current_file in self.failed_files:
                logger.info(f'Moving {current_file} into {self.failed_files_dir}')
                # If failed file does not exist, create an empty file
                if not os.path.isfile(current_file):
                    Path(current_file).touch(exist_ok=True)

                if not safe_move(current_file, self.failed_files_dir):
                    logger.error(f'Cannot move {current_file} into {self.failed_files_dir}')
