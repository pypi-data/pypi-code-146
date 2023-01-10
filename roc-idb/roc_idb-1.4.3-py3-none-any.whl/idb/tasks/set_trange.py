#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.tools.exceptions import MissingArgument
from roc.idb.constants import (IDB_SOURCE, TIME_SQL_STRFORMAT, VALIDITY_MAX,
                               VALIDITY_MIN)
from roc.idb.exceptions import IdbUpdateError, SetTrangeIdbReleaseError
from roc.idb.models.idb import IdbRelease
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

__all__ = ['SetTrangeTask']


class SetTrangeTask(Task):
    plugin_name = 'roc.idb'

    name = 'idb_set_trange'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):
        """
        Set the validity time range of a given IDB
        """

        # Get input arguments
        self.idb_version = self.pipeline.get(
            'idb_version', default=None, args=True
        )
        self.idb_source = self.pipeline.get(
            'idb_source', default=IDB_SOURCE, args=True
        )
        self.validity_min = self.pipeline.get(
            'validity_min', default=None, args=True
        )
        self.validity_max = self.pipeline.get(
            'validity_max', default=None, args=True
        )

        if self.idb_version is None:
            raise MissingArgument(
                'Input argument "idb_version" must be defined!'
            )
        elif self.idb_version.upper().startswith('V'):
            self.idb_version = self.idb_version[1:]

        if self.validity_min is None and self.validity_max is None:
            raise MissingArgument(
                'Input arguments "validity_min" and/or "validity_max" must be defined!'
            )

        # First, check that IDB release exists in the database
        idb = self.get_current_idb()

        if self.validity_min is not None:
            # Check that already defined validity_max is not older than input validity_min
            if (
                idb.validity_max is not None
                and idb.validity_max < self.validity_min
            ):
                raise IdbUpdateError(
                    f'Input validity_min ({self.validity_min}) is older '
                    f'than the validity_max ({idb.validity_max}) found in the database '
                    f'for IDB {self.idb_source} {self.idb_version}, exit task!'
                )

            # Check that validity_min is not already defined
            if idb.validity_min is not None:
                logger.warning(
                    f'Existing validity_min value "{idb.validity_min}" will be replaced'
                )

            idb.validity_min = self.validity_min
            logger.info(
                f'validity_min value set to "{self.validity_min}" for IDB {self.idb_version}'
            )

        if self.validity_max is not None:
            # Check that already defined validity_min is not younger than input validity_max
            if (
                idb.validity_min is not None
                and idb.validity_min > self.validity_max
            ):
                raise IdbUpdateError(
                    f'Input validity_max ({self.validity_max}) is younger '
                    f'than the validity_min ({idb.validity_min}) found in the database '
                    f'for IDB {self.idb_source} {self.idb_version}, exit task!'
                )

            # Check that validity_max is not already defined
            if idb.validity_max is not None:
                logger.warning(
                    f'Existing validity_max value "{idb.validity_max}" will be replaced'
                )

            idb.validity_max = self.validity_max
            logger.info(
                f'validity_max value set to "{self.validity_max}" for IDB {self.idb_version}'
            )

    def get_current_idb(self):

        # get all the releases stored in the database
        self.all_releases = self.pipeline.db.session.query(IdbRelease)

        # get the release we want to set
        query_filter = {'idb_version': self.idb_version}
        query_filter['idb_source'] = self.idb_source

        try:
            idb = self.all_releases.filter_by(**query_filter).one()
        except NoResultFound:
            raise SetTrangeIdbReleaseError(
                f"IDB version '{self.idb_version}' not found in the " 'MAIN-DB'
            )
        except MultipleResultsFound:
            raise SetTrangeIdbReleaseError(
                'Multiple entries found for IDB '
                f"'{self.idb_version}', please specify an IDB source."
            )
        else:
            logger.debug(
                f'IDB version {self.idb_version} found in the database'
            )

        return idb
