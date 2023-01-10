#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Constant variables for roc.idb plugin.
"""
import os
from datetime import datetime

__all__ = [
    'TIME_ARG_STRFORMAT',
    'TIME_SQL_STRFORMAT',
    'VALIDITY_MAX',
    'VALIDITY_MIN',
    'IDB_SOURCE',
    'IDB_INSTALL_DIR',
    'MIB_VERSION_STRFORMAT',
    'MIB_RELEASE_URL_PATTERN',
    'MIB_ARCHIVE_URL_PATTERN',
    'MIB_GITLAB_TOKEN',
    'IDB_SVN_URL',
    'IDB_SVN_USER',
    'IDB_SVN_PASSWORD',
    'TIMEOUT',
    'POSTGRES_DB_PORT',
    'TIME_WAIT_SEC',
    'TRYOUTS',
    'TIMEOUT',
]

# STRING format for time
TIME_ARG_STRFORMAT = '%Y-%m-%dT%H:%M:%S'
TIME_SQL_STRFORMAT = '%Y-%m-%d %H:%M:%S'

# Default values
VALIDITY_MIN = datetime(2000, 1, 1)
VALIDITY_MAX = datetime(2050, 12, 31)

# Expected input format for MIB version
MIB_VERSION_STRFORMAT = '%Y%m%d'

# Default IDB source
IDB_SOURCE = 'MIB'

# Default IDB installation directory
IDB_INSTALL_DIR = os.environ.get('IDB_INSTALL_DIR', '/pipeline/lib/idb')

# Default URL pattern for the ROC MIB release page
MIB_RELEASE_URL_PATTERN = 'https://gitlab.obspm.fr/api/v4/projects/930/packages/generic/mib_release/{mib_version}/idb_dump.sql'

# Default URL pattern for the RPW MIB archive
MIB_ARCHIVE_URL_PATTERN = 'https://gitlab.obspm.fr/api/v4/projects/ROC%2Fmib/repository/archive.zip?sha={version}'

# IDB SVN URL
IDB_SVN_URL = 'https://version-lesia.obspm.fr/repos/SO-RPW/IDB/tags'
IDB_SVN_USER = os.environ.get('IDB_SVN_USER', None)
IDB_SVN_PASSWORD = os.environ.get('IDB_SVN_PASSWORD', None)

# Gitlab access token
MIB_GITLAB_TOKEN = os.environ.get('MIB_GITLAB_TOKEN', None)

# Default process timeout in seconds
TIMEOUT = 3600

# Postgres database default port
POSTGRES_DB_PORT = 5432

# Database tries and seconds to wait between two tries
TRYOUTS = 3
TIME_WAIT_SEC = 3
