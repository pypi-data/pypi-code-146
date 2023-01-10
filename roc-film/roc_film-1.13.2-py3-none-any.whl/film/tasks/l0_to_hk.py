#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module containing task for the RPW HK CDF file production."""

import os.path as osp
import os
import glob
from datetime import datetime
import uuid

import numpy as np
import h5py


from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget

from roc.rpl.time import Time

from roc.film.tools.file_helpers import put_cdf_global, \
    get_master_cdf_dir, get_output_dir, is_output_dir
from roc.film.tools.metadata import init_cdf_global, get_spice_kernels
from roc.film.tools.file_helpers import generate_filepath, is_packet, get_l0_file

__all__ = ['L0ToHk']

# Generate SOLO RPW HK daily CDF files
from roc.film.exceptions import LoadDataSetError

from roc.film.tools.tools import get_datasets, sort_cdf_by_epoch


@FileTarget.input(identifier='l0_file', filepath=get_l0_file)
@FileTarget.output(identifier='hk_dbs')
@FileTarget.output(identifier='hk_das')
@FileTarget.output(identifier='hk_das_stat')
@FileTarget.output(identifier='hk_tds')
@FileTarget.output(identifier='hk_lfr')
@FileTarget.output(identifier='hk_thr')
@FileTarget.output(identifier='hk_pdu')
@FileTarget.output(identifier='hk_bia')
@Task.as_task(plugin_name='roc.film', name='l0_to_hk')
def L0ToHk(task):
    """
    Task to write RPW HK "digest" survey data CDF files from an input L0 file.
    """

    # Import external modules
    from spacepy.pycdf import CDF

    # Define task job ID (long and short)
    job_uuid = str(uuid.uuid4())
    job_id = f'L0ToHk-{job_uuid[:8]}'
    logger.info(f'Task {job_id} is starting')

    try:
        # Get products directory (folder where final output files will be moved)
        products_dir = task.pipeline.get('products_dir',
                                         default=[None], args=True)[0]

        # Get output dir
        output_dir = get_output_dir(task.pipeline)
        if not is_output_dir(output_dir,
                             products_dir=products_dir):
            logger.info(f'Making {output_dir}')
            os.makedirs(output_dir)
        else:
            logger.debug(f'Output files will be '
                        f'saved into folder {output_dir}')


        # Get or create failed_files list from pipeline properties
        failed_files = task.pipeline.get('failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        processed_files = task.pipeline.get(
            'processed_files', default=[], create=True)

        # Get overwrite argument
        overwrite = task.pipeline.get('overwrite', default=False, args=True)

        # get the input l0_file
        l0_file = task.inputs['l0_file']

        # Get (optional) arguments for SPICE
        predictive = task.pipeline.get('predictive', default=False, args=True)
        kernel_date = task.pipeline.get('kernel_date', default=None, args=True)
        no_spice = task.pipeline.get('no_spice', default=False, args=True)

        # Get/create Time singleton
        time_instance = Time(predictive=predictive,
                             kernel_date=kernel_date,
                             no_spice=no_spice)
    except:
        logger.exception(
                f'Initializing inputs has failed for {job_id}!')
        try:
            os.makedirs(os.path.join(output_dir, 'failed'))
        except:
            logger.error(f'output_dir argument is not defined for {job_id}!')
        task.pipeline.exit()
        return

    # Retrieve list of output datasets to produce for the given task
    try:
        dataset_list = get_datasets(task, task.name)
    except:
        raise LoadDataSetError(f'Cannot load the list of datasets to produce for {task.name}    [{job_id}]')
    else:
        logger.debug(f'Produce HK CDF file(s) for the following dataset(s): {[ds["name"] for ds in dataset_list]}    [{job_id}]')

    # open the HDF5 file to extract information
    with h5py.File(l0_file.filepath, 'r') as l0:

        # Loops over each output dataset to produce for the current task
        for current_dataset in dataset_list:
            dataset_name = current_dataset['name']
            data_descr = current_dataset['descr']
            data_version = current_dataset['version']

            filepath = None
            try:
                # Display
                logger.info('Processing HK dataset {0}    [{1}]'.format(dataset_name, job_id))

                # get the path to the master CDF file of this dataset
                master_cdf_dir = get_master_cdf_dir(task)
                # Get master cdf filename from descriptor
                master_cdf_file = data_descr['template']
                # Build master file pattern
                master_pattern = osp.join(master_cdf_dir,
                                       master_cdf_file)
                # Get master filepath
                master_path = glob.glob(master_pattern)

                # Check existence
                if not master_path:
                    os.makedirs(os.path.join(output_dir, 'failed'))
                    raise FileNotFoundError('{0} MASTER CDF '
                                            'FILE NOT FOUND!    [{1}]'.format(master_pattern, job_id))
                else:
                    master_path = sorted(master_path)[-1]
                    logger.debug('Use {0} as a master CDF    [{1}]'.format(master_path, job_id))

                # Set CDF metadata
                metadata = init_cdf_global(l0.attrs, task, master_path)

                # Build output filepath from pipeline properties and L0 metadata
                # Generate output filepath
                filepath = generate_filepath(task, metadata, '.cdf',
                                             overwrite=overwrite)

                # Get TM packet(s) required to generate HK CDF for the current
                # dataset
                packet = data_descr['packet']
                # Check that TM packet(s) are in the input l0 data
                if is_packet(packet, l0['TM']):
                    data = l0['TM'][packet[0]]
                else:
                    # if not continue
                    logger.info(f'No packet found in {l0_file.filepath} '
                                f'for dataset {dataset_name}    [{job_id}]')
                    continue

                # open the target to update its status according to errors etc
                target = task.outputs[dataset_name]
                with target.activate():

                    # if output dir not exists, create it
                    if not os.path.isdir(task.pipeline.output):
                        os.makedirs(task.pipeline.output)

                    # create the file for the CDF containing results
                    cdf = CDF(filepath, master_path)
                    # cdf.readonly(False)
                    # write global information on the CDF
                    put_cdf_global(cdf, metadata)

                    # get the time from the header
                    time = data['data_field_header']['time']
                    # convert time to CDF_TIME_TT2000
                    tt2000 = time_instance.obt_to_utc(time,
                                                      to_tt2000=True)
                    # set time zVars into the CDF
                    cdf['ACQUISITION_TIME'] = time[:, :2]
                    cdf['Epoch'] = tt2000
                    cdf['SCET'] = Time.cuc_to_scet(time[:, :2])
                    cdf['SYNCHRO_FLAG'] = time[:, 2]

                    # copy data from file into memory
                    # TODO - Add conversion of HK parameters into engineering
                    # values
                    parameters = {}
                    for parameter, values in data['source_data'].items():
                        parameters[parameter] = values[...]
                    # loop over parameters and add them to the CDF file
                    for parameter, values in parameters.items():
                        cdf[parameter] = values
                        cdf[parameter].attrs['SCALEMIN'] = np.min(values)
                        cdf[parameter].attrs['SCALEMAX'] = np.max(values)

                    # TODO - Improve this part (add a check of requested attributes?)
                    # Generation date
                    cdf.attrs['Generation_date'] = datetime.utcnow().isoformat()

                    # file uuid
                    cdf.attrs['File_ID'] = str(uuid.uuid4())

                    cdf.attrs['TIME_MIN'] = str(
                        Time.tt2000_to_jd(min(tt2000)))
                    cdf.attrs['TIME_MAX'] = str(
                        Time.tt2000_to_jd(max(tt2000)))

                    # Add SPICE SCLK kernel as an entry
                    # of the "Kernels" g. attr
                    sclk_file = get_spice_kernels(time_instance=time_instance,
                                                  pattern='solo_ANC_soc-sclk')

                    if sclk_file:
                        cdf.attrs['SPICE_KERNELS'] = sclk_file[-1]
                    else:
                        logger.warning('No SPICE SCLK kernel '
                                       f'saved for {filepath}    [{job_id}]')

                    cdf.close()

                    if os.path.isfile(filepath):
                        # Sort by ascending Epoch time
                        logger.debug(f'Sorting by ascending Epoch times    [{job_id}]')
                        # Build list of Zvar to sort
                        zvar_list = list(parameters.keys())
                        zvar_list.extend(['Epoch',
                                          'ACQUISITION_TIME',
                                          'SCET',
                                          'SYNCHRO_FLAG'])
                        cdf = CDF(filepath)
                        cdf.readonly(False)
                        cdf = sort_cdf_by_epoch(cdf, zvar_list=zvar_list)
                        cdf.close()

                        logger.info(
                            f'{filepath} saved    [{job_id}]'
                        )
                    else:
                        raise FileNotFoundError(f'{filepath} not found!    [{job_id}]')

            except:
                logger.exception(f'Production for dataset {dataset_name} '
                                 f'from {l0_file.filepath} has failed!    [{job_id}]')
                if filepath:
                    failed_files.append(filepath)
            else:
                if filepath:
                    processed_files.append(filepath)

            # Pass output filepath in the output target
            target.filepath = filepath


# TODO - Add task to generate SOLO RPW HK dump CDF files
#L0ToHkDumpTask = Plugin.manager[PLUGIN].task("l0_to_hk_dump")
#@L0ToHkDumpTask.as_task
# def l0_to_hk_dump(task):
