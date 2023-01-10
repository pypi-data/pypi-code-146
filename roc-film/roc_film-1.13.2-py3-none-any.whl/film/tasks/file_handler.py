#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Tasks for file handling in FILM plugin."""

import os
import shutil

from poppy.core.logger import logger
from poppy.core.task import Task

__all__ = ['MoveToProdDir', 'MoveFailedFiles',
           'CopyFailedDds', 'CopyProcessedDds']

from roc.film.tools.tools import safe_move

from roc.film.tools.file_helpers import get_output_dir, get_products_dir


class MoveToProdDir(Task):
    """Task to move output files folder to
    final products directory."""
    plugin_name = 'roc.film'
    name = 'move_to_products_dir'

    def run(self):

        # TODO - add a lock file mechanism but at the task level
        #   (useful here to make sure that the
        #   a folder in the products_dir is not moved/removed while
        #   the pipeline is still working on it
        #   Add a LockFile class instance to the Task class in Poppy ?

        # See if --no-move keyword is defined
        no_move = self.pipeline.get('no_move', default=False, args=True)
        if no_move:
            logger.info(
                'Skip current task "move_to_products_dir": --no-move is True')
            return

        # Retrieve pipeline output file directory
        output_dir = get_output_dir(self.pipeline)

        # Retrieve path of the product directory where output file directory
        # shall be moved
        products_dir = get_products_dir(self.pipeline)

        # Ignore possible lock file in the output directory
        ignore_patterns = '*.lock'

        if not products_dir:
            logger.info(
                'Skip current task "move_to_products_dir": products_dir argument not defined')
        else:
            output_dirbasename = os.path.basename(output_dir)
            target_dir = os.path.join(products_dir, output_dirbasename)
            logger.info(f'Moving {output_dir} into {products_dir}')
            if safe_move(output_dir, target_dir,
                         ignore_patterns=ignore_patterns):
                logger.info(f'{output_dir} moved into {products_dir}')


class MoveFailedFiles(Task):
    """Move any failed files found
    into a 'failed' subdirectory."""
    plugin_name = 'roc.film'
    name = 'move_failed_files'

    def run(self):

        # Retrieve list of failed files
        failed_file_list = self.pipeline.get('failed_files', default=[])
        failed_file_count = len(failed_file_list)

        # Retrieve output directory
        output_dir = get_output_dir(self.pipeline)

        if failed_file_count == 0:
            logger.debug('No failed file(s) to move')
        else:

            # Loop over failed files list
            for failed_file in failed_file_list:

                # Make failed subdir if not exists
                failed_dir = os.path.join(output_dir, 'failed')
                os.makedirs(failed_dir, exist_ok=True)

                # if failed item is a file
                if os.path.isfile(failed_file):

                    # Get failed file basename
                    failed_basename = os.path.basename(failed_file)

                    # target file path
                    target_filepath = os.path.join(failed_dir, failed_basename)

                    # perform a safe move (i.e., copy, check and delete) into
                    # failed dir
                    if safe_move(failed_file, target_filepath):
                        logger.info(f'{failed_file} moved into {failed_dir}')


class CopyProcessedDds(Task):
    """
    Task to copy processed DDs files into a dedicated directory.
    """

    plugin_name = 'roc.film'
    name = 'copy_processed_dds'

    def run(self):

        # Get processed file target directory
        processed_dir = self.pipeline.get('processed_dds_dir',
                                          default=[None], args=True)[0]

        # skip task if processed_dir is None
        if processed_dir is None:
            logger.info(
                'Skip task copy_processed_dds: No processed_dds_dir argument defined')
            return
        elif not os.path.isdir(processed_dir):
            logger.debug(f'Creating {processed_dir}...')
            os.makedirs(processed_dir)
        else:
            logger.debug(f'process_dir set to {processed_dir}')

        # If processed_files list not defined in the pipeline properties,
        # initialize it
        processed_file_list = self.pipeline.get(
            'processed_dds_files', default=[])
        processed_files_count = len(processed_file_list)
        # Skip task if no processed files
        if processed_files_count == 0:
            logger.info(
                'Skip task copy_processed_dds: No processed file to move')
            return

        # Get clear-dds keyword
        clear_dds = self.pipeline.get('clear_dds', default=False)

        # Get list of failed files too
        failed_file_list = self.pipeline.get('failed_dds_files', default=[])

        # Loop over processed files to copy
        for processed_file in processed_file_list.copy():

            # Check first that processed file is not in failed list
            if processed_file in failed_file_list:
                logger.warning(f'{processed_file} found in the failed file list!')
                continue

            # Build target filepath
            basename = os.path.basename(processed_file)
            target_filepath = os.path.join(processed_dir, basename)

            # copy file
            logger.debug(f'Copying {processed_file} into {processed_dir}')
            try:
                shutil.copyfile(processed_file, target_filepath)
            except:
                logger.exception(f'Copying {processed_file} into {processed_dir} has failed!')
            else:
                logger.info(f'{processed_file} copied into {target_filepath}')

            # Remove current file from the list in pipeline properties
            processed_file_list.remove(processed_file)

            # if clear-dds keyword is passed, then remove processed Dds
            if clear_dds:
                os.remove(processed_file)
                logger.debug(f'{processed_file} deleted')


class CopyFailedDds(Task):
    """
     Task to copy failed DDs files into a dedicated directory.
     """
    plugin_name = 'roc.film'
    name = 'copy_failed_dds'

    def run(self):

        # Get failed file target directory
        failed_dir = self.pipeline.get('failed_dds_dir',
                                       default=[None], args=True)[0]
        # skip task if failed_dir is None
        if failed_dir is None:
            logger.info(
                'Skip task copy_failed_dds: No failed_dds_dir argument defined')
            return
        elif not os.path.isdir(failed_dir):
            logger.debug(f'Creating {failed_dir}...')
            os.makedirs(failed_dir)
        else:
            logger.debug(f'failed_dir set to {failed_dir}')

        # If failed_files list not defined in the pipeline properties,
        # initialize it
        failed_file_list = self.pipeline.get('failed_dds_files', default=[])
        failed_files_count = len(failed_file_list)
        # Skip task if no failed dds files
        if failed_files_count == 0:
            logger.info('Skip task copy_failed_dds: No failed file to move')
            return

        # Get clear-dds keyword
        clear_dds = self.pipeline.get('clear_dds', default=False)

        # Loop over failed files to copy
        for failed_file in failed_file_list.copy():

            # Build target filepath
            basename = os.path.basename(failed_file)
            target_filepath = os.path.join(failed_dir, basename)

            # copy file
            logger.debug(f'Copying {failed_file} into {failed_dir}')
            try:
                shutil.copyfile(failed_file, target_filepath)
            except:
                logger.exception(f'Copying {failed_file} into {failed_dir} has failed!')
            else:
                logger.info(f'{failed_file} copied into {target_filepath}')

            # Remove current file from the list in pipeline properties
            failed_file_list.remove(failed_file)

            # if clear-dds keyword is passed, then remove processed Dds
            if clear_dds:
                os.remove(failed_file)
                logger.debug(f'{failed_file} deleted')

        # Get failed tmraw list
        failed_tmraw_list = self.pipeline.get('failed_tmraw', default=[])
        failed_tmraw_count = len(failed_tmraw_list)
        # Skip task if no failed tmraw
        if failed_tmraw_count == 0:
            logger.debug('No failed tmraw to write')
            return
        else:
            # Else save list of failed tmraw into text file
            tmraw_failed_file = os.path.join(failed_dir, 'tmraw_failed.log')
            with open(tmraw_failed_file, 'a') as fw:
                fw.writelines(failed_tmraw_list)
            logger.info(f'{failed_tmraw_count} failed TmRaw entries '
                        f'saved into {tmraw_failed_file}')
