#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.logger import logger
from poppy.core.tools.exceptions import MissingArgument

from roc.idb.exceptions import NoIdbFound, MultipleIdbFound
from roc.idb.models.idb import IdbRelease
from roc.idb.constants import IDB_SOURCE



class SetCurrentTask(Task):
    plugin_name = 'roc.idb'

    name = 'idb_set_current'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):
        """
        Set the given IDB version as current
        """
        self.idb_version = self.pipeline.get(
            'idb_version', default=None, args=True
        )
        self.idb_source = self.pipeline.get(
            'idb_source', default=IDB_SOURCE, args=True
        )

        if self.idb_version is None:
            raise MissingArgument(
                'Input argument "idb_version" must be defined!'
            )
        elif self.idb_version.upper().startswith('V'):
            self.idb_version = self.idb_version[1:]

        # get all the releases stored in the database
        all_releases = self.pipeline.db.session.query(IdbRelease)

        # get the release we want to set to current
        query_filter = {}
        query_filter['idb_version'] = self.idb_version

        if self.pipeline.args.idb_source:
            query_filter['idb_source'] = self.idb_source

        try:
            future_current_release = all_releases.filter_by(
                **query_filter
            ).one()
        except NoResultFound:
            raise NoIdbFound(
                f"The IDB version '{self.pipeline.args.idb_version}' does not exist in the "
                'MAIN-DB'
            )
        except MultipleResultsFound:
            raise MultipleIdbFound(
                'Multiple releases exist for the IDB version '
                f"'{self.pipeline.args.idb_version}', please specify an IDB source."
            )

        # set the current field of all releases to False
        all_releases.update({IdbRelease.current: False})

        # set the new current release
        future_current_release.current = True

    @staticmethod
    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def get_latest_idb(idb_source='MIB'):
        """
        Static method to retrieve latest IDB version for a given source

        :param idb_source: IDB source ("MIB" by default)
        :return: entries for latest IDB version (if any)
        """

        # get all the IDB releases stored in the database
        connector = Connector.manager[settings.PIPELINE_DATABASE]
        database = connector.get_database()

        # check the database is connected
        database.connectDatabase()

        # get a database session
        session = database.session_factory()

        all_releases = session.query(IdbRelease)

        # get the latest release we want to get for given idb_source
        query_filter = {'idb_source': idb_source}

        try:
            latest_release = (
                all_releases.filter_by(**query_filter)
                .order_by(IdbRelease.validity_max.desc())
                .all()
            )[0]
        except NoResultFound:
            logger.warning(f"No release found for IDB source '{idb_source}'")
            return []
        else:
            return latest_release
