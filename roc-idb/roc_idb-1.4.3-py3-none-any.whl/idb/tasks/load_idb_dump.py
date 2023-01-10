#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
import uuid
from datetime import datetime
import subprocess
import shlex

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.generic.requests import download_file
from poppy.core.logger import logger
from poppy.core.task import Task

__all__ = ['LoadIdbDump']

from roc.idb.constants import MIB_RELEASE_URL_PATTERN, IDB_INSTALL_DIR, TIMEOUT, POSTGRES_DB_PORT


class LoadIdbDump(Task):
    plugin_name = 'roc.idb'
    name = 'idb_load_idb_dump'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def setup_inputs(self):

        # Get input arguments ===
        self.dump_file = self.pipeline.get('dump_file',
                                           default=[None])[0]
        self.install_dir = self.pipeline.get('install_dir',
                                             default=[IDB_INSTALL_DIR])[0]
        self.auth = tuple(self.pipeline.get('auth', default=(None, None)))
        self.timeout = self.pipeline.get('timeout', default=[TIMEOUT])
        self.pg_restore = self.pipeline.get('pg_restore',
                                            default=False)
        self.clear_temp = self.pipeline.get('clear_temp',
                                            default=False)
        self.force = self.pipeline.get('force', default=False)
        self.shell = self.pipeline.get('shell', default=False)

        # Building a valid dump file path before ingestion
        if self.dump_file is None and self.mib_version:
            # If no dump file provided, then try to retrieve dump file
            # from ROC gitlab server using mib version

            # First build the URL with input MIB version
            self.dump_file = MIB_RELEASE_URL_PATTERN.format(mib_version=self.mib_version)
        elif self.dump_file is None and self.mib_version is None:
            raise ValueError(f'Not enough information to continue: \n '
                             f'at least one of the following inputs must be passed: '
                             f'dump_file or mib_version ')

        # get the database information
        db_info = self.pipeline.properties.configuration['pipeline.databases'][0]
        self.db_user, self.db_pass = db_info['login_info']['admin'].split(':')
        self.db_host = db_info['login_info']['address']
        self.db_name = db_info['login_info']['database']
        try:
            self.db_port = db_info['login_info']['port']
        except:
            self.db_port = POSTGRES_DB_PORT

    def run(self):
        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = self.job_uuid[:8]
        logger.info(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(f'Initializing inputs has failed for task {self.job_id}!')
            self.pipeline.exit()
            return

        # Get idb dump filename
        dump_basename = os.path.basename(self.dump_file)

        # Check if input dump file path is a URL or a local path
        if self.dump_file.startswith('https'):
            # if it is a URL, then download first the file

            # Build local file path
            Path(self.install_dir).mkdir(parents=True, exist_ok=True)
            local_filepath = os.path.join(self.install_dir,
                                          dump_basename)

            # Call the gitlab API using the user token
            if not os.path.isfile(local_filepath) or self.force:
                try:
                    logger.info(f'Downloading {self.dump_file} in {local_filepath}, please wait')
                    download_file(local_filepath, self.dump_file,
                                  auth=self.auth,
                                  )
                except:
                    logger.exception(f'Downloading {self.dump_file} has failed!')
                else:
                    logger.info(f'{local_filepath} downloaded')

        else:
            logger.info(f'Use {self.dump_file} as IDB dump file')
            local_filepath = self.dump_file

        # Now run psql tool to insert IDB dump file content
        # into the ROC database
        if self.pg_restore:
            exe = 'pg_restore'
            sep = ''
        else:
            exe = 'psql'
            sep = '<'

        cmd = ' '.join([exe,
                f'-h {self.db_host}',
                f'-U {self.db_user}',
                f'-d {self.db_name}',
                f'-p {self.db_port}',
                sep, local_filepath])
        process = None
        if os.path.isfile(local_filepath):
            try:
                run_start_time = datetime.now()
                logger.info(f'Running "{cmd}" started on {run_start_time}')

                # Let the shell out of this (i.e. shell=False)
                process = subprocess.call(shlex.split(cmd),
                                          shell=self.shell,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          env={'PGPASSWORD': self.db_pass})

            except subprocess.CalledProcessError as e:
                logger.exception(f'Process has failed: \n {e}')
            except subprocess.TimeoutExpired as e:
                logger.exception(f'Process has expired: \n {e}')
            except:
                logger.exception(f'Process has failed!')
            else:
                run_end_time = datetime.now()
                logger.info(f'Running --> "{cmd}" has ended on {run_end_time} '
                            f'(took {run_end_time - run_start_time})')
        else:
            logger.error(f'{local_filepath} not found!')

        return process
