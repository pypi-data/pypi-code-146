#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from poppy.core.configuration import Configuration
from poppy.core.db.dry_runner import DryRunner
from poppy.core.generic.cache import CachedProperty
from poppy.pop.db_connector import POPPy as POPPyConnector
from roc.idb.models.idb import IdbRelease
from roc.idb.manager import IDBManager
from sqlalchemy.orm.exc import NoResultFound

__all__ = ['IdbConnector']


class IdbDatabaseError(Exception):
    """
    Errors for the connector of the POPPy database.
    """


class IdbConnector(POPPyConnector):
    """
    A class for querying the POPPy database with the IDB schema.
    """

    @CachedProperty
    def idb_manager(self):
        """
        Create the IDB manager and store it.
        """
        return IDBManager(self.session)

    @DryRunner.dry_run
    def get_idb(self):
        """
        Return the database_descr object of the selected version of the IDB.
        """
        if self._idb is None:
            raise ValueError('Must specify a version for the IDB')

        # construct the query
        query = self.session.query(IdbRelease)
        query = query.filter_by(idb_version=self._idb)
        try:
            return query.one()
        except NoResultFound:
            raise IdbDatabaseError(
                (
                    'The IDB version {0} was not found on the database. '
                    + 'Have you loaded the IDB inside the database with '
                    + 'help of the -> pop rpl load command?'
                ).format(self._idb)
            )

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        self._configuration = configuration

        # get the descriptor file
        descriptor = Configuration.manager['descriptor']
        self._pipeline = descriptor['pipeline.release.version']
        self._pipeline_name = descriptor['pipeline.identifier']

        if 'idb_version' in self._configuration:
            self._idb = self._configuration.idb_version
