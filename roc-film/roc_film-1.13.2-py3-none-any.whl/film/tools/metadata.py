#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from os import path as osp
from datetime import datetime

from poppy.core.configuration import Configuration
from poppy.core.logger import logger
from poppy.pop.plugins import Plugin

from roc.film.exceptions import UnknownPipeline, InvalidDataVersion
from roc.film.tools import valid_data_version
from roc.film.constants import PLUGIN, TIME_DAILY_STRFORMAT, \
    CDF_TRANGE_STRFORMAT, UNKNOWN_IDB, DATA_VERSION

__all__ = ['init_l0_meta',
           'init_cdf_global',
           'get_data_version',
           'set_logical_file_id',
           'get_logical_file_id',
           ]


def init_cdf_global(l0_attrs, task, master_path,
                    overwrite=None):
    """
    Define global attributes data to save into the CDF from the content of the L0 file and task.
    See roc.film.tasks.l0.init_l0_meta for the list of specific L0 meta
    (Generic metadata are filled via the roc.rap plugin)

    :param l0_attrs: RPW L0 file attributes
    :param task: input task containing properties
    :master_path: Path to the master CDF
    :overwrite: Dictionary containing g.attrs as keys and expecting values as values
    :return: output CDF global attribute dictionary
    """
    from spacepy.pycdf import CDF

    # Initialize the output dictionary that will contain the metadata for CDF
    # by import master CDF global attributes
    meta = dict(CDF(master_path).attrs)

    pipeline_id = Configuration.manager['descriptor']['pipeline.identifier'].upper()
    pipeline_version = Configuration.manager['descriptor']['pipeline.release.version']

    if pipeline_id == 'RGTS':
        # Specific to RGTS
        meta['Pipeline_name'] = pipeline_id + '>ROC Ground Test SGSE'

        try:
            meta['Test_name'] = l0_attrs['Test_name'].encode('utf-8')
            meta['Test_uuid'] = l0_attrs['Test_uuid']
            meta['Test_description'] = l0_attrs[
                'Test_description'].encode('utf-8')
            meta['Test_creation_date'] = l0_attrs['Test_creation_date']
            meta['Test_launched_date'] = l0_attrs['Test_launched_date']
            meta['Test_terminated_date'] = l0_attrs['Test_terminated_date']
            meta['Test_log_file'] = l0_attrs['Test_log_file']

            # ID of the test for the ROC internal use
            meta['Test_id'] = l0_attrs['Test_id']
        except:
            logger.warning('No "Test_*" attribute found for the input l0')


    elif pipeline_id == 'RODP':
        # TODO - Complete specific global attributes for RODP
        meta['Pipeline_name'] = pipeline_id + '>RPW Operation and Data Pipeline'
        pass
    else:
        raise UnknownPipeline(f'UNKNOWN PIPELINE TYPE:'
                              f' {pipeline_id}, ABORTING!')

    # Common global attributes
    try:
        # Perform some verifications on metadata
        if str(meta['Pipeline_name']) != str(l0_attrs['Pipeline_name']):
            logger.warning('Pipeline_name is inconsistent '
                           f"between the pipeline ({meta['Pipeline_name']})"
                           f"and the input L0 file ({l0_attrs['Pipeline_name']})!")

        meta['Pipeline_version'] = pipeline_version
        meta['Parents'] = ['CDF>' + l0_attrs['Logical_file_id']]
        meta['Parent_version'] = valid_data_version(l0_attrs['Data_version'])
        meta['Free_field'] = l0_attrs['Free_field']
        meta['Software_version'] = Plugin.manager[PLUGIN].version

        # Use for building filename
        meta['Datetime'] = l0_attrs['Datetime']

        # provider in the good format
        meta['Provider'] = l0_attrs['Provider']

        # Get file naming convention
        meta['File_naming_convention'] = l0_attrs['File_naming_convention']
    except:
        logger.error('Missing attributes in l0 file!')

    # the name of the software (plugin) that generated the file, from the
    # descriptor information
    meta['Software_name'] = PLUGIN

    # Initialize Validate (0 = no validation)
    meta['Validate'] = '0'

    # Initialize data_version
    meta['Data_version'] = get_data_version(task) # Initialize data_Version to "01"

    # If overwrite keyword, then replace g.attrs value
    if overwrite:
        for key, val in overwrite.items():
            meta[key] = val
            logger.debug(f'{key} g.attribute value set to {val}')

    # Initialize logical_file_id
    meta['Logical_file_id'] = set_logical_file_id(meta)

    return meta


def get_idb_version(task, **kwargs):
    """
    Try to get idb version used to parsed packets

    :param task: task instance
    :return: string with idb_version
    """

    idb_version = task.pipeline.get('idb_version',
                                    default=kwargs.get('idb_version', UNKNOWN_IDB))
    try:
        idb_version = task.inputs['raw_data'].value.packet_parser.idb_version
    except:
        logger.debug('No IDB version found in the input raw_data:\n'
                     f'attempting to retrieve value from pipeline properties: {idb_version}')

    return idb_version

def get_idb_source(task, **kwargs):
    """
    Try to get idb source used to parsed packets

    :param task: task instance
    :return: string with idb_source
    """

    idb_source = task.pipeline.get('idb_source',
                                   default=kwargs.get('idb_source', UNKNOWN_IDB))
    try:
        idb_source = task.inputs['raw_data'].value.packet_parser.idb_source
    except:
        logger.debug('No IDB source found in the input raw_data:\n'
                     f'attempting to retrieve value from pipeline properties: {idb_source}')

    return idb_source


def init_l0_meta(task,
                 extra_attrs={}):
    """
    Initialize RPW L0 metadata

    :param task: task
    :param extra_attrs: Dictionary containing extra attributes to be inserted into the L0 root groupe.
    :return: meta, a dictionary containing metadata for the output L0 file.
    """

    # Initialize the output dictionary that will contain the metadata for L0
    meta = dict()

    ## Retrieve required values from the pipeline properties
    # Get pipeline ID ("RGTS" or "RODP")
    pipeline_id = task.pipeline.properties.configuration['environment.ROC_PIP_NAME'].upper()

    # Get input RawData value
    try:
        raw_data = task.inputs['raw_data'].value
    except:
        raw_data = None

    # Get metadata specific to ROC-SGSE
    if pipeline_id == 'RGTS':

        meta['Pipeline_name'] = pipeline_id + '>ROC Ground Test SGSE'

        try:
            # Get the 7 first characters of the test log SHA
            test_sha = raw_data.sha1
            test_short_sha = raw_data.short_sha1

            meta['Test_name'] = raw_data.name
            meta['Test_uuid'] = raw_data.uuid
            meta['Test_description'] = raw_data.description
            meta['Test_creation_date'] = str(raw_data.creation_date)
            meta['Test_launched_date'] = str(raw_data.date)
            meta['Test_terminated_date'] = str(raw_data.terminated_date)
            meta['Test_log_file'] = osp.basename(raw_data.file_path)
            meta['Test_id'] = test_short_sha + '>' + test_sha

            meta['Free_field'] = '-'.join([task.pipeline.provider[:3].lower(),
                                           test_short_sha])
            meta['Datetime'] = '-'.join([raw_data.time_min.strftime(CDF_TRANGE_STRFORMAT),
                                         raw_data.time_max.strftime(CDF_TRANGE_STRFORMAT)])
        except:
            logger.warning('No input test log found!')
            meta['Free_field'] = ''
            meta['Datetime'] = datetime.now().strftime(TIME_DAILY_STRFORMAT)

        meta['File_naming_convention'] = '<Source_name>_<LEVEL>_<Descriptor>_' \
                                         '<Datetime>_V<Data_version>_' \
                                         '<Free_field>'

    elif pipeline_id == 'RODP':
        # Get metadata specific to RODP
        # TODO - Complete metadata for RPW L0

        meta['File_naming_convention'] = '<Source_name>_<LEVEL>_<Descriptor>_' \
                                         '<Datetime>_V<Data_version>'

        meta['Pipeline_name'] = pipeline_id + '>RPW Operation and Data Pipeline'
        meta['Free_field'] = ''

        # Define Datetime value
        datetime_attr = extra_attrs.pop('Datetime', None)
        if datetime_attr is None:
            if raw_data is not None and hasattr(raw_data, 'datetime') and raw_data.datetime is not None:
                datetime_attr = raw_data.datetime.strftime(TIME_DAILY_STRFORMAT)
            else:
                datetime_attr = task.pipeline.get('datetime')
                if datetime_attr is None:
                    logger.warning('Unknown Datetime attribute value')
                else:
                    datetime_attr = datetime_attr.strftime(TIME_DAILY_STRFORMAT)

        meta['Datetime'] = datetime_attr

    else:
        raise UnknownPipeline(f'UNKNOWN PIPELINE TYPE:'
                              f' {pipeline_id}, ABORTING!')

    # Common metadata
    meta['Project'] = 'SOLO>Solar Orbiter'
    meta['Source_name'] = 'SOLO>Solar Orbiter'
    meta['Software_name'] = PLUGIN
    meta['Software_version'] = Plugin.manager[PLUGIN].version
    meta['Dataset_ID'] = 'SOLO_L0_RPW'
    meta['Descriptor'] = 'RPW>Radio and Plasma Waves instrument'
    meta['LEVEL'] = 'L0>Level 0 data processing'
    meta['Provider'] = '>'.join(
        [
            task.pipeline.provider[:3].upper(),
            task.pipeline.provider,
        ]
    )

    meta['Pipeline_version'] = Configuration.manager['descriptor'][
        'pipeline.release.version'
    ]

    # Initialize data_version
    data_version = extra_attrs.pop('Data_version', None)
    if data_version is None:
        meta['Data_version'] = get_data_version(task) # Initialize data_Version to "01"
    else:
        meta['Data_version'] = data_version

    # Add extra attributes (if any)
    if extra_attrs:
        for key, val in extra_attrs.items():
            meta[key] = val

    # Initialize logical_file_id
    meta['Logical_file_id'] = set_logical_file_id(meta)

    return meta

def get_data_version(task):
    """
    Get value of Data_version attribute.

    :param task: input pipeline task object
    :return: string containing Data_version value
    """

    data_version = task.pipeline.get('data_version', default=None, args=True)
    if data_version is None:
        data_version = DATA_VERSION
    else:
        data_version = data_version[0]

    # Try to get Data_version from task (return only two digits)
    try:
        return valid_data_version(data_version)
    except:
        raise InvalidDataVersion(f'Input data version is invalid: {data_version}')


def set_logical_file_id(metadata):
    """
    Define Logical_file_id attribute value from the input metadata.

    :param metadata: dictionary containing metadata attributes
    :return: logical_file_id value
    """

    # Get expected fields in the file_naming_convention
    logical_file_id = str(metadata['File_naming_convention'])
    for field in re.findall(r'<([A-Za-z0-9_\-]+)>', logical_file_id):
        # Extract value from metadata
        value = str(metadata[field]).split('>')[0]
        if field == 'Datetime' or field == 'LEVEL':
            value = value.upper()
        else:
            value = value.lower()

        logical_file_id = logical_file_id.replace('<' + field + '>', value)

    return logical_file_id


def get_logical_file_id(filename):
    """
    Get the logical file ID for a file given its complete file name on the
    system. Assumes that the convention of the file name according to the one
    of the ROC is correct.

    :param filename: input file name
    :return: string of the expected logical_file_id
    """
    return osp.basename(osp.splitext(filename)[0])


def get_spice_kernels(time_instance=None,
                      pattern=None):

    # If time_instance not passed as input argument,
    # then initialize it from Time class (singleton)
    if time_instance is None:
        from roc.rpl.time import Time
        time_instance = Time()

    # get all loaded kernels
    loaded_kernels = time_instance.spice.kall()

    if pattern is not None:
        loaded_kernels = [kfile for kfile in loaded_kernels.keys()
                            if pattern in kfile]
    else:
        loaded_kernels = list(loaded_kernels.keys())

    return loaded_kernels
