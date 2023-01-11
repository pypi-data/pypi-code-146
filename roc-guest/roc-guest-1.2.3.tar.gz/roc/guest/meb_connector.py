#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.logger import logger

from functools import lru_cache
from poppy.core.db.connector import Connector
from poppy.core.generic.metaclasses import Singleton
from poppy.core.db.database import Database
from .models.meb_gse.database import DatabaseInformation

__all__ = ["MEB", "MEBException"]




class MEBException(Exception):
    pass


class MEBSelector(object, metaclass=Singleton):
    """
    Class to manage the database of the MEB which are *backuped* regularly but
    must be available to the user.
    """
    def __init__(self, meb):
        """
        Need the instance of the MEB database as an argument to be able to
        query the other provided databases.
        """
        self.meb = meb

    def current(self):
        """
        Return the database marked as current.
        """
        # check connected and reflected
        if not self.meb.is_available():
            logger.error("{0} is not connected".format(self.meb))
            return None

        # get a session from the database
        with self.meb.query_context() as session:

            # get the current database
            tmp_meb = session.query(DatabaseInformation).filter(
                DatabaseInformation.Current==1
            )
            meb = tmp_meb.one().DatabaseName

        # check that there is a current database
        if meb is None:
            message = "No current database for MEB. Why?"
            logger.error(message)
            raise MEBException(message)

        # generate the database object for the current
        return self.select(meb)

    @lru_cache(maxsize=32)
    def select(self, name):
        """
        Return a database according to its name.
        """
        # make a copy of parameters of the database for common informations
        parameters = {k: v for k, v in self.meb.parameters.items()}

        # update parameters with the information on the name of the meb
        # database FIXME: here forced for purpose tests
        parameters["database"] = name

        # create the database
        meb = Database(name)
        meb.parameters = parameters
        meb.base = Database.bases_manager.get("MEB")

        # return the database
        return meb


class MEB(Connector):
    """
    The connector class for the MEB database.
    """
    def __init__(self, *args, **kwargs):
        """
        Init the selected database to None.
        """
        # create instance as usual
        super(MEB, self).__init__(*args, **kwargs)

        # indicate that no database is selected
        self._selected = None

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, name):
        self._database = name

        # also set the database to the selector
        self.selector = MEBSelector(self.get_database())

    def select(self, name):
        """
        To select the MEB database for the data that will be used for the other
        selections on the database. Thus the database will be the current one
        in internal to do tasks.
        """
        # get the database from the selector
        self.selected = self.selector.select(name)

        # return the selected database
        return self.selected

    @property
    def selected(self):
        """
        Get the current database from the MEB informations if no one is already
        selected.
        """
        if self._selected is None:
            self._selected = self.selector.current()
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

