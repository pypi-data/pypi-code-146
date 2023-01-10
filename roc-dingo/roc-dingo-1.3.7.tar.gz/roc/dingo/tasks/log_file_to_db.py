#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import os
import re

from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import load_only

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.dingo.constants import PIPELINE_DATABASE, ROC_DATA_ROOT, \
    DATA_ALLOWED_EXTENSIONS, SPICE_KERNEL_ALLOWED_EXTENSIONS, \
    ROC_DATA_HTTPS_ROOT, ROC_SPICE_KERNEL_HTTPS_ROOT
from roc.dingo.models.file import FileLog

from roc.film.constants import TIME_ISO_STRFORMAT

import h5py
from spacepy.pycdf import CDF
from astropy.time import Time


__all__ = ['LogFileToDb']


class LogFileToDb(Task):
    """
    Parse ROC file tree and synchronize withe the ROC databaser
    """
    plugin_name = 'roc.dingo'
    name = 'log_file_to_db'
    files_to_update = []
    files_to_insert = []

    def add_targets(self):
        logger.debug('LogFileToDb() : add_targets')
        self.add_input(target_class=BaseTarget, many=True,
                       identifier='roc_data_files_to_insert')
        self.add_input(target_class=BaseTarget, many=True,
                       identifier='roc_data_files_to_update')

    def setup_inputs(self):
        """
        Setup task inputs.

        :param task:
        :return:
        """

        logger.debug('LogFileToDb() : setup_inputs')

        # get the root file tree
        self.root = self.pipeline.get('root', default=ROC_DATA_ROOT, args=True)
        # ensure that there is / at the end
        self.root = os.path.join(self.root, '')

        # get files to update
        self.files_to_db = {}
        self.files_to_db['update'] = self.inputs['roc_data_files_to_update']
        self.files_to_db['insert'] = self.inputs['roc_data_files_to_insert']

    def run(self):

        logger.debug('LogFileToDb() : run')

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Initialize inputs
        self.setup_inputs()

        # Insert / Update files
        for action, files in self.files_to_db.items():
            if files.is_empty:
                continue

            logger.debug('*** TO {} ***'.format(action.upper()))
            num_files = len(files.data)
            cpt_file_ok = 0
            cpt_file_ko = 0
            for basename, item in files.data.items():
                logger.debug(item['filepath'])

                try:
                    file_dict = LogFileToDb.item_to_file_log(
                        item, self.root)
                except ValueError as e:
                    logger.error('Value error:', e)
                    if action == 'update':
                        # We only store that there was an error
                        file_dict = {
                            'basename': basename,
                            'status': 'Failed'}
                    else:
                        cpt_file_ko += 1
                        continue
                except Exception as e:
                    cpt_file_ko += 1
                    logger.error('Unexpected error:', e)
                    continue

                # retreive parents ID (1/2)
                # remove "parents" item before inserting
                parents = file_dict.pop('parents')

                try:
                    if action == 'insert':
                        file_log = FileLog(**file_dict)
                        query = self.session.add(file_log)
                    else:
                        # action == 'update'
                        query = self.session.query(FileLog).\
                            filter(FileLog.basename == basename).\
                            update(file_dict)
                        file_log = self.session.query(FileLog).\
                            filter(FileLog.basename == basename).first()
                except Exception:
                    cpt_file_ko += 1
                    logger.error('{} file {} has failed: \n {!s}'.format(
                        action.capitalize,
                        file_dict['basename'],
                        query.statement.compile(
                            dialect=postgresql.dialect(),
                            compile_kwargs={'literal_binds': True})
                    ))
                    # break to the following file
                    continue
                else:
                    cpt_file_ok += 1
                    logger.info(
                        '{} file {:60s} OK [{:05.2f}% complete]'.format(
                            action.capitalize(),
                            file_dict['basename'],
                            100 * cpt_file_ok / num_files
                        ))

                # ensure that previous versions are set to is_latest=False
                # get file filename without extension and version
                if file_dict['level'] != 'SK':
                    trunc_basename = os.path.splitext(
                        file_dict['basename'])[0].\
                        replace('_V' + file_dict['version'], '')
                    logger.debug(f'TRUNC : {trunc_basename}')

                    base_filter = FileLog.basename.like(
                        '%' + trunc_basename + '%')
                    latest_filter = FileLog.is_latest == True  # noqa: E712
                    version_filter = FileLog.version < file_dict['version']

                    try:
                        query = self.session.query(FileLog).\
                            filter(and_(
                                base_filter,
                                latest_filter,
                                version_filter))

                        for r in query.all():
                            logger.debug(f'OLD VERSION : {r.basename}')

                        old_items = {}
                        old_items['is_latest'] = False
                        nb = query.update(old_items, synchronize_session=False)

                    except Exception as e:
                        logger.error(
                            f'Error while searching previous versions : {e}')

                    else:
                        if nb > 0:
                            logger.info(
                                f'Setting {nb} files to is_latest = False')

                # retreive parents ID (2/2)
                parents_added = []
                parents_filter = FileLog.basename.in_(parents)
                logger.debug('Parents : {}'.format(parents))
                try:
                    query = self.session.query(FileLog).\
                        options(load_only('id')).\
                        filter(parents_filter)
                except Exception:
                    logger.error('{} file {} has failed: \n {!s}'.format(
                        action.capitalize,
                        file_dict['basename'],
                        query.statement.compile(
                            dialect=postgresql.dialect(),
                            compile_kwargs={'literal_binds': True})
                    ))
                else:
                    for result in query.all():
                        file_log.parents.append(result)
                        parents_added.append(result.basename)
                        parents.remove(result.basename)

                        # sometimes a parent without extension is specified
                        # both extensions cdf/h5 are then added
                        # in the parents list
                        # we have to remove the one which wasn't the good one
                        if '.cdf' in result.basename:
                            h5name = result.basename.replace(
                                '.cdf', '.h5')
                            if h5name in parents:
                                parents.remove(h5name)

                        if '.h5' in result.basename:
                            cdfname = result.basename.replace(
                                '.h5', '.cdf')
                            if cdfname in parents:
                                parents.remove(cdfname)

                    # some parents are missing
                    if len(parents) > 0:
                        if file_log.error_log is None:
                            file_log.error_log = ''

                        if file_log.error_log != '':
                            file_log.error_log += '; '

                        file_log.error_log += 'Missing parents : ' + \
                            ', '.join(parents)
                        logger.debug('Missing parents : {}'.format(
                            ', '.join(parents)))

                    self.session.commit()

                logger.debug('Parents added : {}'.format(parents_added))

            logger.info('{} : {} success / {} failure'.format(
                action.capitalize(), cpt_file_ok, cpt_file_ko
            ))

    @staticmethod
    def item_to_file_log(item, root):
        """
        Create a dictionnary ready to be inserted as a FileLog

        :param item: dictionnary with file-system elements already filled :
            size, creation_time, filepath, id
        :param root: the root name of the files (root os not striord in DB)
        :return: dictionnary ready to be inserted as a FileLog
        """

        # DATA or SPICE_KERNEL ?
        is_data = True
        url_prefix = ROC_DATA_HTTPS_ROOT
        re_ext = '|'.join(DATA_ALLOWED_EXTENSIONS)

        file_name, file_extension = os.path.splitext(item['filepath'])
        if file_extension.replace('.', '') in SPICE_KERNEL_ALLOWED_EXTENSIONS:
            url_prefix = ROC_SPICE_KERNEL_HTTPS_ROOT
            is_data = False
            re_ext = '|'.join(SPICE_KERNEL_ALLOWED_EXTENSIONS)

        error_log = []
        warning_log = []

        file_dict = {}
        file_dict['creation_time'] = item['creation_time']
        file_dict['size'] = item['size']

        file_dict['dirname'] = os.path.dirname(
            item['filepath']).replace(root, '')

        file_dict['basename'] = os.path.basename(
            item['filepath'])

        file_dict['sha'] = ''
        file_dict['state'] = 'OK'
        file_dict['status'] = 'Terminated'
        file_dict['insert_time'] = datetime.now()
        file_dict['descr'] = ''
        file_dict['author'] = ''

        file_dict['is_removed'] = not os.path.exists(item['filepath'])
        # Removed file cannot be the latest one
        file_dict['is_latest'] = (not file_dict['is_removed']) and \
            ('former_version' not in file_dict['dirname'])

        file_dict['url'] = url_prefix + '/' + file_dict['dirname'] + '/' + \
            file_dict['basename']

        # Things in path
        file_path = file_dict['dirname'].split('/')
        if is_data:
            file_dict['level'] = file_path[0]
        else:
            file_dict['level'] = 'SK'

        # Things in filename
        if not is_data:
            res = re.search(
                r'^([^\.]+)_V([0-9]+)\.(' + re_ext + ')',
                file_dict['basename'])
        else:
            res = re.search(
                r'^([^\.]+)_(v|V)([0-9a-zA-Z]+)\.(' + re_ext + ')',
                file_dict['basename'])

        if res:
            file_dict['product'] = res.group(1)
        else:
            file_dict['product'] = ''
            logger.error('Unable to get product name in {}'.format(
                file_dict['basename']))
            error_log.append('Unable to get product name in {}'.format(
                file_dict['basename']))

        file_attrs = {
            'TIME_MIN': None,
            'TIME_MAX': None,
            'Dataset_ID': None,
            'Data_version': '00',
            'Parents': [],
            'SPICE_KERNELS': [],
        }

        try:
            if '.h5' in file_dict['basename']:
                file_attrs = LogFileToDb.get_attrs_from_h5(
                    item['filepath'], file_attrs)

            if '.cdf' in file_dict['basename']:
                file_attrs = LogFileToDb.get_attrs_from_cdf(
                    item['filepath'], file_attrs)

        except Exception as e:
            logger.error('Error while reading {} : {}'.format(
                file_dict['basename'], e))
            # import traceback
            # traceback.print_exc()
            error_log.append(str(e))

        parents = file_attrs['Parents']
        start_time = file_attrs['TIME_MIN']
        end_time = file_attrs['TIME_MAX']
        data_set_id = file_attrs['Dataset_ID']
        version = file_attrs['Data_version']

        # fields error_log and warning_log may have been
        # filled during get_attrs_from_xxx()
        if 'error_log' in file_attrs:
            error_log += file_attrs['error_log']

        if 'warning_log' in file_attrs:
            warning_log += file_attrs['warning_log']

        # Version checks
        if is_data and file_extension != '.xml':
            # remove leading 'V'
            res = re.search(r'^[v|V]([0-9a-zA-Z]+)$', version)
            if res:
                logger.debug(f'Removing leading V in version : {version}')
                version = res.group(1)

            # check if the one in filename is the one in attributes
            res = re.search(
                r'(v|V)([0-9a-zA-Z]+)\.(' + re_ext + ')',
                file_dict['basename'])
            if version != '' and res:
                version_in_filename = res.group(2)
                if version != version_in_filename:
                    msg = 'Versions in filename and attributes do not match'
                    logger.error(msg)
                    error_log.append(msg)
            elif version == '' and res:
                version = res.group(2)
                msg = 'No version in attributes'
                logger.warning(msg)
                warning_log.append(msg)
            else:
                version = '00'
                msg = 'No version in filename'
                logger.warning(msg)
                warning_log.append(msg)
        else:
            res = re.search(
                r'_(v|V)([0-9]+)\.(' + re_ext + ')',
                file_dict['basename'])
            if res:
                version = res.group(2)
            else:
                version = '00'

        logger.debug(f'Version =  {version}')

        # Skipping parents[] search for spice kernels
        if is_data:
            logger.debug('Reading regular data')
            # some parents entries are not well formed
            to_be_removed = []
            for i, p in enumerate(parents):
                # Some entries are empty
                if re.match(r'\s*$', p):
                    to_be_removed.append(p)
                    continue

                # Some parents have no file extension
                if not re.search(r'\.(\w{,3})$', p):
                    to_be_removed.append(p)
                    # either extensions can be the good one
                    parents.append(p + '.cdf')
                    parents.append(p + '.h5')

                # ignoring mk/*.tm spice kernels (meta kernel)
                if re.search(r'\.tm$', p):
                    to_be_removed.append(p)

            # finally cleaning parents array
            for i, p in enumerate(to_be_removed):
                parents.remove(p)

        # Reading spice kernels
        if not is_data:
            logger.debug('Reading spice kernels')

            start_time = LogFileToDb.commnt_get_meta(
                item['filepath'], 'START_TIME')
            if len(start_time) > 0:
                start_time = min(start_time)
            else:
                start_time = None

            end_time = LogFileToDb.commnt_get_meta(
                item['filepath'], 'STOP_TIME')
            if len(end_time) > 0:
                end_time = min(end_time)
            else:
                end_time = None

        # When start/stop time have not been set
        # Guess them from basename
        datetimes_expr = \
            re.compile(r'_([0-9]{8}T[0-9]{6})\-([0-9]{8}T[0-9]{6})_')
        dates_expr = re.compile(r'_([0-9]{8})\-([0-9]{8})_')
        date_expr = re.compile(r'_([0-9]{8})_')
        if start_time is None or end_time is None:
            res_times = re.search(datetimes_expr, file_dict['basename'])
            res_dates = re.search(dates_expr, file_dict['basename'])
            res_date = re.search(date_expr, file_dict['basename'])

            if res_times:
                start_time = res_times.group(1)
                end_time = res_times.group(2)

            elif res_dates:
                start_time = res_dates.group(1)
                end_time = res_dates.group(2)

            elif res_date:
                start_time = res_date.group(1)
                try:
                    end_time = (
                        Time.strptime(
                            res_date.group(1), '%Y%m%d') + timedelta(days=1)
                    ).iso
                except ValueError as e:
                    logger.warning(
                        f'Unable to parse end time {end_time} : {e}')
                    end_time = None

            if start_time is not None or end_time is not None:
                logger.info(
                    'Guessing start/end time for {} : {} - {}'.format(
                        file_dict['basename'],
                        start_time,
                        end_time
                    ))

        if len(error_log) > 0:
            file_dict['state'] = 'ERROR'

        elif len(warning_log) > 0:
            file_dict['state'] = 'WARNING'

        # Save both error and warning messages
        if (len(error_log) + len(warning_log)) > 0:
            file_dict['error_log'] = '; '.join(error_log + warning_log)
        else:
            # necessary in order to reset error_log when the error is cleared
            file_dict['error_log'] = ''

        # trimming whitespaces
        file_dict['parents'] = [p.strip() for p in parents]

        file_dict['dataset_id'] = data_set_id
        file_dict['version'] = version
        file_dict['start_time'] = start_time
        file_dict['end_time'] = end_time
        file_dict['validity_end'] = None
        file_dict['validity_start'] = None

        # do not set these values here
        # either they are set to false at creation (table default value)
        # or they are set to True with specific tasks
        # file_dict['is_archived'] = False
        # file_dict['is_delivered'] = False

        file_dict['to_update'] = False

        logger.debug(file_dict)

        return file_dict

    @staticmethod
    def commnt_get_meta(filename, key):
        """
        Retreive parameters in spice kernel using the commnt command

        :param filename: full path of the spice kernel
        :param key: parameter to read
        :return: parameter array values
        """
        val = os.popen(
            'commnt -r ' + filename + ' | '
            "awk -F '=' ' /" + key + "/ {print $2} '").read().split()
        if len(val) == 0:
            if key == 'START_TIME':
                val = LogFileToDb.commnt_get_meta(filename, 'CK-144000START')
            elif key == 'STOP_TIME':
                val = LogFileToDb.commnt_get_meta(filename, 'CK-144000STOP')

            val = [datetime.strptime(
                v, '@%Y-%b-%d-%H:%M:%S.%f').isoformat() for v in val]

        return val

    @staticmethod
    def get_attrs_from_cdf(filename, file_attrs):
        """
        Retreive a attrs from CDF file
            :param filename: full path of the file
            :param file_attrs: dictionnary with the attributes to retreive
            :return: dictionnary file_attrs with the attributes filled plus
                error_log and warning_log
        """

        basename = os.path.basename(filename)
        data_set_id = None
        version = '00'
        parents = []
        parent_version = []
        error_log = []
        warning_log = []

        # Add Parent_version for CDF only
        file_attrs['Parent_version'] = []

        with CDF(filename) as cdf:
            for attr in file_attrs:
                try:
                    logger.debug('{} : {}'.format(basename, attr))
                    # don't forget the [...] to get a copy and not a pointer
                    file_attrs[attr] = cdf.attrs[attr][...]
                except KeyError as e:
                    logger.warning(
                        'Missing attribute in {} : {}'.format(
                            basename,
                            re.sub(r'\'', r'', str(e))))
                    warning_log.append(re.sub(r'\'', r'', str(e)))
                    continue

        try:
            start_time = Time(
                float(file_attrs['TIME_MIN'][0]),
                format='jd', precision=9)
        except ValueError as e:
            start_time = Time('1900-01-01')  # fake date
            msg = 'Formatting date error for time_min in {} : '\
                '{} ({})'.format(
                    basename,
                    re.sub(r'\'', r'', str(e)),
                    file_attrs['TIME_MIN'][0])
            logger.error(msg)
            error_log.append(msg)

        try:
            end_time = Time(
                float(file_attrs['TIME_MAX'][0]),
                format='jd', precision=9)
        except ValueError as e:
            end_time = Time('1900-01-01')  # fake date
            msg = 'Formatting date error for time_max in {} : '\
                '{} ({})'.format(
                    basename,
                    re.sub(r'\'', r'', str(e)),
                    file_attrs['TIME_MAX'][0])
            logger.error(msg)
            error_log.append(msg)

        # Check if data seems to be coherent
        # we sometimes get
        # WARNING: ErfaWarning: ERFA function "d2dtf" yielded
        # 1 of "dubious year (Note 5)" [astropy._erfa.core]

        if start_time.jd < Time('2020-02-11').jd or \
           start_time.jd > Time('2100-01-01').jd:
            msg = f'Start time seems to be erroneous : {start_time.iso}'
            logger.error(msg)
            error_log.append(msg)
            start_time = None
        else:
            start_time = start_time.iso

        if end_time.jd < Time('2020-02-11').jd or \
           end_time.jd > Time('2100-01-01').jd:
            msg = f'End time seems to be erroneous : {end_time.iso}'
            logger.error(msg)
            error_log.append(msg)
            end_time = None
        else:
            end_time = end_time.iso

        try:
            data_set_id = file_attrs['Dataset_ID'][0]
            # Clean data_set_id
            # some files have {} around id
            data_set_id = re.sub(r'[\{\}]', '', data_set_id)
        except Exception:
            logger.warning('Dataset_ID missing')

        try:
            version = f'{file_attrs["Data_version"][0]}'
            # ensure version number is a string on 2 digits
            version = version.strip()
            if len(version) == 1:
                version = f'0{version}'
        except Exception:
            version = '00'
            logger.warning('Data_version missing')

        # some files store one parents in each entry,
        # other in string concatenated with commas
        for entry in file_attrs['Parents']:
            if entry.strip() != '':
                parents += entry.split(',')

        for entry in file_attrs['Parent_version']:
            # ensure it is a string
            entry = f'{entry}'
            if entry.strip() != '':
                parent_version += entry.split(',')

        # remove extra whitespace
        parents = [p.strip() for p in parents]
        parent_version = [p.strip() for p in parent_version]

        logger.debug('*** PARENTS ***')
        logger.debug(f'{parents}')
        logger.debug(f'{parent_version}')

        # if parents and parent_version don't have the same length
        # it is useless to try to append the version number
        if len(parents) != len(parent_version):
            logger.debug(parents)
            logger.debug(parent_version)
            error_log.append('Parents and Parent_version length mismatch')
        else:
            # Append the version number if needed
            for i, p in enumerate(parents):
                p_name, p_ext = os.path.splitext(p)
                if not re.search(r'_V[0-9U]+$', p_name):
                    version = parent_version[i]
                    # some files say '5' instead of '05'
                    if len(version) == 1:
                        version = f'0{version}'
                    p_name += f'_V{version}'
                    parents[i] = p_name + p_ext
                    logger.debug('Adding version to parent name : '
                                 f'{parents[i]}')

        # some files store spice kernels in array,
        # other in string concatenated with commas
        for entry in file_attrs['SPICE_KERNELS']:
            parents += entry.split(',')

        for i, p in enumerate(parents):
            if (p.find('CDF>') != -1):
                parents[i] = p.replace('CDF>', '')
            if (p.find('L0>') != -1):
                parents[i] = p.replace('L0>', '')
            if (p.find('ANC>') != -1):
                parents[i] = p.replace('ANC>', '')

        file_attrs['TIME_MIN'] = start_time
        file_attrs['TIME_MAX'] = end_time
        file_attrs['Dataset_ID'] = data_set_id
        file_attrs['Parents'] = parents
        file_attrs['Data_version'] = version

        file_attrs['error_log'] = error_log
        file_attrs['warning_log'] = warning_log

        return file_attrs

    @staticmethod
    def get_attrs_from_h5(filename, file_attrs):
        """
        Retreive a attrs from HDF5 file
            :param filename: full path of the file
            :param file_attrs: dictionnary with the attributes to retreive
            :return: dictionnary file_attrs with the attributes filled plus
                error_log and warning_log
        """

        basename = os.path.basename(filename)
        error_log = []
        warning_log = []

        with h5py.File(filename, 'r') as l0:
            for attr in file_attrs:
                try:
                    logger.debug('{} : {}'.format(basename, attr))
                    file_attrs[attr] = l0.attrs[attr]
                except KeyError as e:
                    logger.warning('Missing attribute in {} : {}'.format(
                        basename, e))
                    warning_log.append(str(e))
                    continue

        # Get TIME_MIN/TIME_MAX L0 attributes value as datetime
        file_attrs['TIME_MIN'] = datetime.strptime(
            file_attrs['TIME_MIN'], TIME_ISO_STRFORMAT)

        file_attrs['TIME_MAX'] = datetime.strptime(
            file_attrs['TIME_MAX'], TIME_ISO_STRFORMAT)

        file_attrs['Parents'] = file_attrs['Parents'].split(',')
        if len(file_attrs['SPICE_KERNELS']) > 0:
            file_attrs['Parents'] += file_attrs['SPICE_KERNELS'].split(',')

        # Ensure data version is a string on 2 digits
        file_attrs['Data_version'] = f'{file_attrs["Data_version"]}'
        file_attrs['Data_version'] = file_attrs['Data_version'].strip()
        if len(file_attrs['Data_version']) == 1:
            file_attrs['Data_version'] = f'0{file_attrs["Data_version"]}'

        file_attrs['error_log'] = error_log
        file_attrs['warning_log'] = warning_log

        return file_attrs
