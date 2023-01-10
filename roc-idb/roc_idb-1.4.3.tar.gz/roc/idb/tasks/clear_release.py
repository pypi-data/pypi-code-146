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


class ClearIdbReleaseTask(Task):
    plugin_name = 'roc.idb'

    name = 'idb_clear_release'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):

        # Get input arguments
        idb_version = self.pipeline.get('idb_version', default=None, args=True)
        idb_source = self.pipeline.get('idb_source', default=None, args=True)
        force = self.pipeline.get('force', default=False, args=True)

        if idb_version is None:
            raise MissingArgument(
                'Input argument "idb_version" must be defined!'
            )
        elif idb_version.upper().startswith('V'):
            idb_version = idb_version[1:]

        # Get database session
        session = self.pipeline.db.session

        # get all the releases stored in the database
        all_releases = session.query(IdbRelease)

        # get the release we want to set to current
        query_filter = {'idb_version': idb_version}

        if idb_source is not None:
            query_filter['idb_source'] = idb_source

        try:
            idb_to_clear = all_releases.filter_by(**query_filter).one()
        except NoResultFound:
            raise NoIdbFound(
                f"The IDB version '{idb_version}' does not exist in the "
                'MAIN-DB'
            )
        except MultipleResultsFound:
            raise MultipleIdbFound(
                'Multiple releases exist for the IDB version '
                f"'{idb_version}', please specify an IDB source."
            )
        else:

            if not force:
                answer = input(
                    f'ENTER IDB VERSION TO CONFIRM THE DELETION [{idb_version}]: '
                )
            else:
                answer = idb_version

            if answer == idb_version:
                logger.debug(f'Deleting IDB {idb_version} from database...')
                session.delete(idb_to_clear)
                session.commit()
                logger.info(
                    f'IDB {idb_version} has been removed from the database'
                )
            else:
                logger.info(
                    f'IDB {idb_version} has not been removed from the database'
                )
