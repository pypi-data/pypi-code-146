#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import argparse
import time
from datetime import datetime
import hashlib
import shutil

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import and_, inspect

from poppy.core.logger import logger
from poppy.core.db.handlers import get_or_create_with_info

from roc.rpl.packet_parser import raw_to_eng
from roc.idb.models.idb import IdbRelease

from roc.dingo.constants import TIME_DAILY_STRFORMAT, \
    TIME_INPUT_STRFORMAT, SQL_LIMIT, TRYOUTS, TIME_WAIT_SEC, \
    TF_CP_BIA_P011_SRDB_ID, IDB_SOURCE

from roc.dingo.exceptions import DingoException, DbQueryError
from roc.dingo.models.data import ProcessQueue

__all__ = ['valid_time',
           'valid_date',
           'valid_dir',
           'valid_data_version',
           'glob_paths',
           'get_packet_sha',
           'get_dict_sha',
           'compute_apid',
           'compute_pkt_seq_control',
           'load_spice',
           'insert_in_db',
           'safe_move',
           'get_or_create_in_db',
           'query_db',
           'delete_in_db',
           'actual_sql',
           'gen_sql_filters',
           'is_sclk_uptodate',
           'get_columns',
           'bulk_insert',
           'sbm_qf_eng',
           'raw_to_na',
           'compute_hfr_list_freq']


def raise_error(message, exception=DingoException):
    """Add an error entry to the logger and raise an exception."""
    logger.error(message)
    raise exception(message)


def valid_dir(dir):
    """
    Make sure to have a valid input directory.

    :param dir: 1-element list or string containing the path to the directory
    :return:
    """
    try:
        if isinstance(dir, list):
            dir = dir[0]
        if os.path.isdir(dir):
            return dir
        else:
            raise IsADirectoryError
    except IsADirectoryError:
        raise_error(f'Input directory not found! ({dir})',
                    exception=IsADirectoryError)
    except ValueError:
        raise_error(f'Input directory is not valid! ({dir})',
                    exception=ValueError)
    except Exception as e:
        raise_error(f'Problem with input directory! ({dir})',
                    exception=e)


def glob_paths(paths):
    """
    Make sure input paths are expanded
    (can be used to avoid any path with wildcard pattern)

    :param path: list of input paths to glob
    :return: list of paths after glob filtering
    """
    globbed_paths = []
    if not isinstance(paths, list):
        paths = [paths]

    for current_path in paths:
        globbed_paths.extend(glob.glob(current_path))

    return globbed_paths


def valid_time(t, format=TIME_INPUT_STRFORMAT):
    """
    Validate input datetime string format.

    :param t: input datetime string
    :param format: expected datetime string format
    :return: datetime object with input datetime info
    """
    if t and isinstance(t, str):
        try:
            t = datetime.strptime(t, format)
        except:
            raise ValueError(f"Not a valid time: '{t}'!")

    return t


def valid_date(t, format=TIME_DAILY_STRFORMAT):
    """
    Validate input date string format.

    :param t: input date string
    :param format: expected date string format
    :return: date object with input date info
    """
    if t and isinstance(t, str):
        try:
            t = datetime.strptime(t, format).date()
        except ValueError:
            argparse.ArgumentTypeError(f"Not a valid date: '{t}'!")
    return t


def valid_data_version(data_version):
    """
    Make sure to have a valid data version.

    :param data_version: integer or string containing the data version
    :return: string containing valid data version (i.e., 2 digits string)
    """
    try:
        data_version = int(data_version)
        return f'{data_version:02d}'
    except ValueError:
        raise_error(f'Input value for --data-version is not valid! \
                     ({data_version})')


def get_packet_sha(packet_data):
    """
    Compute the SHA256 of the input packet.
    TM sha is computed from binary
    TC sha is computed from packet name (SRDB ID), execution UTC time and status

    :param packet_data: h5.Group containing data of the input packet
    :return: string containing SHA (hexdigest)
    """
    sha = None
    packet_name = packet_data['palisade_id']
    if packet_name.startswith('TC'):
        raw_sha = hashlib.sha256()
        raw_sha.update(packet_data['srdb_id'].encode('utf-8'))
        raw_sha.update(packet_data['utc_time'].isoformat().encode('utf-8'))
        raw_sha.update(packet_data['tc_exe_state'].encode('utf-8'))
        sha = str(raw_sha.hexdigest())
    elif packet_name.startswith('TM'):
        raw_sha = hashlib.sha256()
        raw_sha.update(packet_data['binary'].encode('utf-8'))
        sha = str(raw_sha.hexdigest())
    else:
        logger.error(f'Unknown packet name: {packet_name}')

    return sha


def get_dict_sha(dict_to_hash,
                 include=[],
                 exclude=[]):
    """
    Compute a SHA256 from the values in a input dictionary

    :param dict_to_has: input dictionary to hash
    :param include: list of keywords to include. Ignored if empty
    :param exclude: list of keywords to ignore
    :return: SHA as a hexa digest string
    """

    sha = hashlib.sha256()
    for key, val in dict_to_hash.items():
        if include and key not in include:
            continue
        if key in exclude:
            continue
        if isinstance(val, datetime):
            sha.update(val.isoformat().encode('utf-8'))
        else:
            sha.update(str(val).encode('utf-8'))

    return str(sha.hexdigest())


def compute_apid(process_id, packet_category):
    """
    Compute the APID using the process_id and the packet_category
    APID = |0000000|0000|
        process_id | packet_category
    """
    return (process_id << 4) + packet_category  # 4 bits shift


def compute_pkt_seq_control(segmentation_grouping_flag, sequence_cnt):
    """
    Compute Packet Sequence Control field for a given packet

    :param segmentation_grouping_flag: Integer storing the packet segmentation_grouping_flag
    :param sequence_cnt: Integer containing the packet sequence counter
    :return: Packet Sequence Control (16-bits)
    """
    return (segmentation_grouping_flag << 14) + sequence_cnt


def load_spice(spice_kernels=[]):
    """
    Load SpiceManager instance with input SOLO kernels

    :param spice_kernels: List of input kernels to load in SPICE
    :return: SpiceManager instance
    """
    from spice_manager import SpiceManager

    return SpiceManager(spice_kernels,
                        logger=logger)


def insert_in_db(session, model, data_to_insert,
                 update_fields={},
                 update_fields_kwargs={},
                 tryouts=TRYOUTS,
                 wait=TIME_WAIT_SEC):
    """
    Insert a data entry in the database

    :param session: open database session
    :param model: database model to use for input data
    :param data_to_insert: data to insert as an entry in the database
    :param update_fields: If entry already exists in the database,
                            then update only fields provided in this dictionary
    :param update_fields_kwargs: dictionary to pass to filter_by() method when query for updating
    :param tryouts: number of tries
    :param wait: seconds to wait between two tries
    :return: insertion status (0=OK, -1=NOK, 1=Already inserted, 2=Updated)
    """
    # if update_fields_kwargs not provided,
    # then use data_to_insert dictionary
    if not update_fields_kwargs:
        update_fields_kwargs = data_to_insert

    for i in range(tryouts):
        try:
            # Add current data as a new entry of the model table
            # in the database
            session.add(model(**data_to_insert))
            # Commit database change(s)
            session.commit()
        except IntegrityError:
            session.rollback()
            logger.debug(f'{data_to_insert} already inserted')
            # If entry already exists,
            # check if fields needs to be updated
            if update_fields:
                logger.debug(f'Updating {update_fields} in the database ...')
                instance = session.query(model).filter_by(
                    **update_fields_kwargs).one()
                # update it
                for field in update_fields or {}:
                    if getattr(instance, field) != update_fields[field]:
                        setattr(instance, field, update_fields[field])
                session.commit()
                insert_status = 2
            else:
                insert_status = 1
            break
        except:
            session.rollback()
            logger.exception(f'Inserting {data_to_insert} has failed!')
            insert_status = -1
            time.sleep(wait)
        else:
            logger.debug(f'{data_to_insert} inserted')
            insert_status = 0
            break

    return insert_status


def safe_move(src, dst, ignore_patterns=[]):
    """
    Perform a safe move of a file or directory.

    :param src: string containing the path of the file/directory to move
    :param dst: string containing the path of the target file/directory
    :param ignore: string containing the file patterns to ignore (for copytree only)
    :return: True if the move has succeeded, False otherwise
    """

    # Initialize output
    is_copied = False

    # First do a copy...
    try:
        if os.path.isfile(src):
            shutil.copy(src, dst, follow_symlinks=True)
        elif os.path.isdir(src):
            shutil.copytree(src, dst,
                            ignore=shutil.ignore_patterns(ignore_patterns),
                            dirs_exist_ok=True)
    except Exception as e:
        logger.exception(f'Cannot move {src} into {dst}!')
        raise e
    else:
        # then delete if the file has well copied
        if os.path.exists(dst):
            is_copied = True
            if os.path.isfile(src):
                os.remove(src)
            elif os.path.isdir(src):
                shutil.rmtree(src)

    return is_copied


def query_db(session, model,
             filters=None,
             limit=SQL_LIMIT,
             order_by=None,
             to_dict=None,
             is_one=False,
             tryouts=TRYOUTS,
             wait=TIME_WAIT_SEC,
             raise_exception=False):
    """
    Query entries from the ROC pipeline database.

    :param session: ROC database open session
    :param model: Table model class
    :param filters: query filters passed as a SQL expression object
    :param limit: Integer containing max. number of returned rows
    :param order_by: Sort returned rows by column value passed in order_by keyword
    :param to_dict: If passed with argument, apply the pandas.DataFrame.to_dict(orient=arg) method
    :param is_one: If True, only one entry is expected.
    :param tryouts: Number of query retries
    :param wait: number of seconds to wait between two retries
    :param raise_exception: If True, raise an exception
    :return: entries found in the database as returned by pandas.read_sql() method
    """
    # Initialize output
    table_entries = None
    # Run query
    has_failed = True
    for current_try in range(tryouts):
        try:
            if isinstance(model, list) or isinstance(model, tuple):
                query = session.query(*model)
            else:
                query = session.query(model)
            if filters is not None:
                query = query.filter(filters)
            if order_by is not None:
                query = query.order_by(order_by)
            query.limit(int(limit))
            logger.debug(f'Querying database: {actual_sql(query)} ...')
            table_entries = pd.read_sql(query.statement, session.bind)
            nrec = table_entries.shape[0]
            if nrec == 0:
                raise NoResultFound
            elif is_one and nrec != 1:
                raise MultipleResultsFound
        except MultipleResultsFound:
            logger.exception(f'Query has returned multiple results!')
            break
        except NoResultFound:
            logger.debug('No results found')
            has_failed = False
            break
        except:
            logger.exception(f'Query has failed!')
        else:
            # logger.debug(f'{query.count()} entries found in the {model} table for {filters}')
            # Convert returned entries into list of lists
            if to_dict is not None:
                table_entries = table_entries.to_dict(orient=to_dict)

            has_failed = False
            break
        logger.debug(f'Retrying query ({current_try} on {tryouts})')
        time.sleep(wait)

    if has_failed and raise_exception:
        raise DbQueryError(f'Querying database with model {model} has failed!')

    return table_entries


def get_or_create_in_db(session, model, entry,
                        kwargs=None,
                        tryouts=TRYOUTS,
                        wait=TIME_WAIT_SEC):
    """
    Insert input entry to pipeline.data_queue table

    :param session: database session object
    :param model: Database table model class
    :param entry: A dictionary containing column:value to insert in the table
    :param kwargs: A dictionary containing the column:value to use to get data
    :param tryouts: number of tries to insert data
    :param wait: seconds to wait between two tries
    :return: (table entry created, database request status flag, creation status flag)
    """
    job = None
    created = None
    done = False
    if not kwargs:
        kwargs = entry
    for current_try in range(tryouts):
        try:
            job, created = get_or_create_with_info(
                session,
                model,
                **kwargs,
                create_method_kwargs=entry)
        except:
            logger.exception(f'Cannot query {model.__tablename__} '
                             f'[retry {tryouts - current_try}]')
            time.sleep(wait)
        else:
            done = True
            break

    return job, done, created

def bulk_insert(session, model, data_to_insert,
                tryouts=TRYOUTS,
                wait=TIME_WAIT_SEC,
                exists_ok=False,
                raise_exception=True):
    """
    Run the bulk_insert_mappings() SQLAlchemy method
    to insert a bulk of data into the database.

    :param session: current database session
    :param model: database table model class
    :param data_to_insert: List of dictionaries to insert in the database
    :param tryouts: number of insertion attempts
    :param wait: seconds to wait between two attempts
    :param raise_exception: if true raise an exception
    :param exists_ok: If True then insertion is OK if entry is already found in the database
    :return: True if insertion has worked, False otherwise
    """
    has_worked = False
    raised_exc = Exception()
    for current_try in range(tryouts):
        try:
            session.bulk_insert_mappings(model, data_to_insert)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raised_exc = e
            if exists_ok:
                has_worked = True
            break
        except Exception as e:
            session.rollback()
            time.sleep(wait)
            raised_exc = e
        else:
            has_worked = True
            break

    if not has_worked and raise_exception:
        raise raised_exc

    return has_worked


def delete_in_db(session, model,
                 filters=None,
                 tryouts=TRYOUTS,
                 wait=TIME_WAIT_SEC):
    """
    Delete row(s) of a table in the database

    :param session: database session
    :param model: Table model
    :param filters: list of filters
    :param tryouts: number of tries
    :param wait: seconds to wait between two tries
    :return: True if deletion has succeeded, False otherwise
    """
    is_deleted = False
    for current_try in range(tryouts):
        try:
            query = session.query(model)
            if filters:
                query.filter(filters)
            query.delete()
            session.commit()
        except NoResultFound:
            is_deleted = True
            break
        except:
            logger.exception(f'Deleting {model} with filters {filters} has failed!')
            time.sleep(wait)
        else:
            is_deleted = True
            break

    return is_deleted


def actual_sql(sqlalchemy_query):
    """
    convert input Sqlalchemy query into explicit SQL syntax query

    :param sqlalchemy_query: input Sqlalchemy query object
    :return: string with corresponding SQL syntax
    """
    return str(
        sqlalchemy_query.statement.compile(
            compile_kwargs={"literal_binds": True}))


def is_sclk_uptodate(current_datetime, sclk_basename):
    """
    Check if the input SOLO SCLK SPICE kernel is newer or older than a give datetime

    :param current_datetime: datetime.datetime object to compare with SOLO SCLK SPICE kernel date
    :param sclk_basename: string containing SOLO SCLK SPICE kernel basename
    :return: True if SCLK SPICE kernel is newer than current_datetime
            , False otherwise
    """
    # Get the date of the SCLK SPICE kernel
    sclk_date = datetime.strptime(
        sclk_basename.split('_')[3],
        TIME_DAILY_STRFORMAT,
    ).date()

    return sclk_date > current_datetime.date()


def get_columns(model, remove=[]):
    """
    Get list of table columns for input model class

    :param model: Table model class
    :param remove: list of columns to remove
    :return: list of table columns
    """
    # Get columns
    columns = model.__table__.columns.keys()
    for key in remove:
        columns.remove(key)
    return columns


def raw_to_na(raw_values,
              idb_source=IDB_SOURCE,
              idb_version=None):
    """
    Convert input raw values of bias current into physical units (nA)

    :param raw_values: numpy array with raw values of Bias current
    :param idb_version: string with idb version
    :param idb_source: string with idb_source
    :return: values in physical units (nA)
    """

    # Retrieve engineering values in uA and return them in nA
    return raw_to_eng(raw_values, TF_CP_BIA_P011_SRDB_ID,
                      idb_source=idb_source, idb_version=idb_version) * 1000


def sbm_qf_eng(raw_values, tf_srdb_id,
               idb_source='MIB', idb_version=None):
    """
    Retrieve engineering values of the SBM1/SBM2 event quality factor

    :param raw_values: SBM1 QF raw values
    :param tf_srdb_id: SBM1/SBM2 F Transfer function SRDB ID (i.e, TF_PA_DPU_0038 or =TF_PA_DPU_0039)
    :param idb_source:
    :param idb_version:
    :return: engineering values of SBM1 QF
    """
    return raw_to_eng(raw_values, tf_srdb_id,
                      idb_source=idb_source, idb_version=idb_version)


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


def gen_sql_filters(model,
                    start_time=None,
                    end_time=None,
                    field='utc_time'):
    """
    Generate common filters for query.

    :param model: table class
    :start_time: query rows greater or equal than start_time only (datetime object)
    :end_time: query rows lesser than end_time only (datetime object)
    :param field: field to use for filters
    :return: list of filters
    """
    filters = []
    if start_time:
        filters.append(model.__dict__[field] >= start_time)
    if end_time:
        filters.append(model.__dict__[field] < end_time)

    return and_(*filters)

def compute_hfr_list_freq(freq_index):
    """
    In HFR LIST mode, return frequency value in kHz giving its
    index

    :param freq_index: index of the frequency
    :return: Value of the frequency in kHz
    """
    return 375 + 50 * (int(freq_index) - 436)
