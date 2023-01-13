import os
import sys
import logging

from . import config
from .helpers import runSubprocess

class Repo:
    def __init__(self):
        if not runSubprocess(['createrepo', '-h'], failOnError=False) and not config.dry_run:
            logging.error('createrepo is not installed')
            sys.exit(1)

    def create(self):
        logging.info('Recreating repo in %s' % config.target_rpm_dir)
        command = ['createrepo', config.target_rpm_dir]
        if config.dry_run:
            print(*command)
        else:
            runSubprocess(command)
