import os
import sys
import logging

from . import config
from .helpers import runSubprocess

class S3:
    def __init__(self):
        self.bucket = os.path.join(config.s3_bucket, config.architecture, config.release_tag, 'o2', '')
        if not runSubprocess(['s3cmd', 'ls', self.bucket], failOnError=False) and not config.dry_run:
            logging.error('s3cmd is not installed or configured properly')
            sys.exit(1)
        logging.info('Using S3 bucket: %s' % self.bucket)

    def pull_rpms(self):
        command = ['s3cmd', 'sync', os.path.join(self.bucket, ''), os.path.join(config.target_rpm_dir, '')]
        if config.dry_run:
            print(*command)
        else:
            runSubprocess(command)

    def push_rpms(self, delete_removed = False):
        command = ['s3cmd', 'sync', os.path.join(config.target_rpm_dir, ''), self.bucket]
        if delete_removed:
            command.append('--delete-removed')
        if config.dry_run:
            print(*command)
        else:
            runSubprocess(command)

    def copy(self, source, dest, delete_removed = False):
        source_bucket = os.path.join(config.s3_bucket, config.architecture, source, 'o2', '')
        dest_bucket = os.path.join(config.s3_bucket, config.architecture, dest, 'o2', '')
        logging.info('S3 copy from %s to %s' % (source_bucket, dest_bucket))
        command = ['s3cmd', 'sync', source_bucket, dest_bucket]
        if delete_removed:
            command.append('--delete-removed')
        if config.dry_run:
            print(*command)
        else:
            runSubprocess(command)
