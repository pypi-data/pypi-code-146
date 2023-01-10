#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import and_, inspect

from poppy.core.logger import logger

from roc.idb.exceptions import NoIdbFound, MultipleIdbFound
from roc.idb.models.idb import IdbRelease
from roc.idb.constants import IDB_SOURCE, TRYOUTS, TIME_WAIT_SEC

__all__ = ['actual_sql', 'get_current_idb', 'clean_idb']

def actual_sql(sqlalchemy_query):
    """
    convert input Sqlalchemy query into explicit SQL syntax query

    :param sqlalchemy_query: input Sqlalchemy query object
    :return: string with corresponding SQL syntax
    """
    return str(
        sqlalchemy_query.statement.compile(
            compile_kwargs={'literal_binds': True}))



def get_current_idb(idb_source, session,
                    tryouts=TRYOUTS,
                    wait=TIME_WAIT_SEC):
    """
    Get current idb release stored in the database

    :param idb_source: IDB source to use (MIB, SRDB or PALISADE).
    :param session: database session
    :param tryouts: number of tries
    :param wait: seconds to wait between two tries
    :return: version of the idb tagged as current, None if not found
    """
    idb_version = None

    filters = []
    if idb_source:
        filters.append(IdbRelease.idb_source == idb_source)
    filters.append(IdbRelease.current == True)
    for i in range(tryouts):
        try:
            query = session.query(
                IdbRelease.idb_version).filter(and_(*filters))
            results = query.one()
        except MultipleResultsFound:
            logger.error(f'Multiple results found for {actual_sql(query)}!')
            break
        except NoResultFound:
            logger.info(f'No result found for {actual_sql(query)}')
            break
        except:
            logger.exception(f'Cannot run {actual_sql(query)} (trying again in {wait} seconds)')
            time.sleep(wait)
        else:
            idb_version = results.idb_version
            break

    return idb_version


def clean_idb(session, idb_source, idb_version):
    """
    Clean a given IDB release in the database

    :param session: database session instance
    :param idb_source: IDB source
    :param idb_version: IDB version
    :return: True if IDB release has been deleted correctly
    """
    is_deleted = False
    try:
        idb_to_delete = (session.query(IdbRelease)
                         .filter(IdbRelease.idb_source == idb_source,
                                 IdbRelease.idb_version == idb_version).one())
        logger.debug(f'Deleting pre-existing IDB [{idb_source}-{idb_version}] ...')
        session.delete(idb_to_delete)
    except MultipleResultsFound:
        logger.exception(f'Multiple IDB [{idb_source}-{idb_version}] has been found!')
    except NoResultFound:
        is_deleted = True
    except:
        logger.exception(f'Pre-existing IDB [{idb_source}-{idb_version}] cannot be deleted!')
    else:
        is_deleted = True

    return is_deleted
