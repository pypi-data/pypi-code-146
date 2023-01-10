#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import sys
import os
from datetime import datetime
import uuid
import traceback

import h5py
import numpy as np

from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget
from roc.film.exceptions import L1SurvProdFailure, LoadDataSetError, NoData

from roc.rap.tasks.utils import order_by_increasing_time
from roc.rpl.time import Time

# Import methods to extract data from RPW packets
from roc.film.tools.dataset_tasks import *

from roc.film.tools.file_helpers import put_cdf_global, \
    generate_filepath, get_master_cdf_dir, \
    is_packet, put_cdf_zvars, get_l0_file, get_output_dir, is_output_dir
from roc.film.tools.metadata import init_cdf_global, get_spice_kernels


# task for L0 to L1 Survey data CDF production (including LFM)
from roc.film.tools.tools import get_datasets

__all__ = ['L0ToL1Surv']



class L0ToL1Surv(Task):
    """
    Task to produce RPW L1 survey data daily CDF from a L0 daily file
    """
    plugin_name = 'roc.film'
    name = 'l0_to_l1_surv'

    def add_targets(self):

        self.add_input(identifier='l0_file', filepath=get_l0_file,
                       target_class=FileTarget)
        self.add_output(identifier='l1_surv_rswf',
                        target_class=FileTarget)
        self.add_output(identifier='l1_surv_tswf', target_class=FileTarget)
        self.add_output(identifier='l1_surv_hist1d', target_class=FileTarget)
        self.add_output(identifier='l1_surv_hist2d', target_class=FileTarget)
        self.add_output(identifier='l1_surv_stat', target_class=FileTarget)
        self.add_output(identifier='l1_surv_mamp', target_class=FileTarget)
        self.add_output(identifier='l1_lfm_rswf', target_class=FileTarget)
        self.add_output(identifier='l1_lfm_cwf', target_class=FileTarget)
        self.add_output(identifier='l1_lfm_sm', target_class=FileTarget)
        self.add_output(identifier='l1_lfm_psd', target_class=FileTarget)
        self.add_output(identifier='l1_surv_asm', target_class=FileTarget)
        self.add_output(identifier='l1_surv_bp1', target_class=FileTarget)
        self.add_output(identifier='l1_surv_bp2', target_class=FileTarget)
        self.add_output(identifier='l1_surv_cwf', target_class=FileTarget)
        self.add_output(identifier='l1_surv_swf', target_class=FileTarget)
        self.add_output(identifier='l1_surv_tnr', target_class=FileTarget)
        self.add_output(identifier='l1_surv_hfr', target_class=FileTarget)

    def setup_inputs(self):

        # Get products directory (folder where final output files will be
        # moved)
        self.products_dir = self.pipeline.get('products_dir',
                                              default=[None], args=True)[0]

        # Get output dir
        self.output_dir = get_output_dir(self.pipeline)
        if not is_output_dir(self.output_dir,
                             products_dir=self.products_dir):
            logger.info(f'Making {self.output_dir}')
            os.makedirs(self.output_dir)
        else:
            logger.debug(f'Output files will be '
                        f'saved into folder {self.output_dir}')

        # get the input l0 file
        self.l0_file = self.inputs['l0_file']

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Retrieve list of output datasets to produce for the given task
        try:
            self.dataset_list = get_datasets(self, self.name)
        except:
            raise LoadDataSetError(f'Cannot load the list of datasets to produce for {self.name}')
        else:
            logger.debug(f'Produce L1 CDF file(s) for the following dataset(s): {[ds["name"] for ds in self.dataset_list]}')

        # Get overwrite optional keyword
        self.overwrite = self.pipeline.get(
            'overwrite', default=False, args=True)

        # Get force optional keyword
        self.force = self.pipeline.get('force', default=False, args=True)

        # Get (optional) arguments for SPICE
        self.predictive = self.pipeline.get(
            'predictive', default=False, args=True)
        self.kernel_date = self.pipeline.get(
            'kernel_date', default=None, args=True)
        self.no_spice = self.pipeline.get('no_spice', default=False, args=True)
        # if is_cdag = True, add '-cdag' suffix to the end of the descriptor field in
        # the output filename
        # (used to indicate preliminary files to distributed to the CDAG members only)
        self.is_cdag = self.pipeline.get('cdag', default=False, args=True)
        if self.is_cdag:
            logger.info('Producing "cdag" output CDF')

        # Get/create Time singleton
        self.time_instance = Time(predictive=self.predictive,
                                  kernel_date=self.kernel_date,
                                  no_spice=self.no_spice)

        return True

    def run(self):

        # Import external modules
        from spacepy.pycdf import CDF

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'L0ToL1Surv-{self.job_uuid[:8]}'
        logger.info(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                f'Initializing inputs has failed for {self.job_id}!')
            try:
                os.makedirs(os.path.join(self.output_dir, 'failed'))
            except:
                logger.error(f'output_dir argument is not defined for {self.job_id}!')
            self.pipeline.exit()
            return

        # Open the HDF5 file to extract information
        with h5py.File(self.l0_file.filepath, 'r') as l0:
            # get modes for TNR
            logger.info(
                f'Producing RPW L1 SURVEY data file(s) from {self.l0_file.filepath}    [{self.job_id}]'
            )

            # Loops over each output dataset to produce for the current task
            for current_dataset in self.dataset_list:
                dataset_name = current_dataset['name']
                data_descr = current_dataset['descr']
                data_version = current_dataset['version']
                logger.debug(f'Running file production for the dataset {dataset_name} (V{data_version})    [{self.job_id}]')

                # get the path to the master CDF file of this dataset
                master_cdf_dir = get_master_cdf_dir(self)

                # Get master cdf filename from descriptor
                master_cdf_file = data_descr['template']

                # Get master filepath
                master_pattern = os.path.join(master_cdf_dir, master_cdf_file)
                master_path = glob(master_pattern)

                # Check existence
                if not master_path:
                    os.makedirs(os.path.join(self.output_dir, 'failed'))
                    raise FileNotFoundError(f'{master_pattern} MASTER CDF '
                                            f'FILE NOT FOUND!    [{self.job_id}]')
                else:
                    master_path = sorted(master_path)[-1]
                    logger.info('Producing dataset "{0}" from {1} '
                                'with the master CDF "{2}    [{3}]"'.format(
                                    dataset_name,
                                    os.path.basename(self.l0_file.filepath),
                                    master_path,
                                    self.job_id))

                # Set CDF metadata
                metadata = init_cdf_global(l0.attrs, self, master_path,
                                           overwrite={'MODS': data_descr['mods']})

                # Build output filepath from pipeline properties and metadata
                filepath = generate_filepath(self, metadata, 'cdf',
                                             is_cdag=self.is_cdag,
                                             overwrite=self.overwrite)

                # Get TM packet(s) required to generate HK CDF for the current
                # dataset
                expected_packet = data_descr['packet']
                # Check that TM packet(s) are in the input l0 data
                if not is_packet(expected_packet, l0['TM']):
                    logger.info(f'No packet for "{current_dataset}" '
                                f'found in {self.l0_file.filepath}    [{self.job_id}]')
                    # if not continue
                    continue

                # Get function to process data
                # IMPORTANT: function alias in import should have the same name
                # than the dataset alias in the descriptor
                func = getattr(sys.modules[__name__], dataset_name)

                # call the function
                try:
                    result = func(l0, self)
                except:
                    # Print error message
                    msg = (f'Running "{func}" function has failed '
                           f'for dataset {dataset_name}    [{self.job_id}]')
                    logger.exception(msg)
                    # creating empty output CDF to be saved into
                    # failed dir
                    cdf = CDF(filepath, master_path)
                    cdf.readonly(False)
                    cdf.attrs['Validate'] = '-1'
                    cdf.attrs['TEXT_supplement_1'] = ':'.join(
                        [msg, traceback.format_exc()])
                    cdf.close()
                    self.failed_files.append(filepath)
                    continue

                # open the target to update its status according to errors etc
                target = self.outputs[dataset_name]
                with target.activate():

                    try:
                        # check non empty
                        if result is None or result.shape[0] == 0:
                            self.failed_files.append(filepath)
                            raise target.TargetEmpty()

                        # reorder the data by increasing time
                        # NOTE - Temporary avoid sorting
                        #  for l1_surv_tnr dataset due to time issue
                        #  (see https://gitlab.obspm.fr/ROC/RCS/THR_CALBAR/-/issues/45)
                        if dataset_name != 'l1_surv_tnr' and dataset_name != 'l1_surv_mamp' and dataset_name != 'l1_surv_hfr':
                            result = order_by_increasing_time(result)
                        elif dataset_name == 'l1_surv_hfr':
                            result = order_by_increasing_time(result, sort_by='acquisition_time')
                            # Make sure to have increasing sweep num
                            i_sweep = 0
                            nrec = result.shape[0]
                            new_sweep = np.zeros(nrec, dtype=int)
                            for i in range(1, nrec):
                                if result['sweep_num'][i] != result['sweep_num'][i - 1]:
                                    i_sweep += 1
                                new_sweep[i] = i_sweep
                            result['sweep_num'] = new_sweep

                        # create the file for the CDF containing results
                        cdf = CDF(filepath, master_path)

                        # write global attribute entries on the CDF
                        put_cdf_global(cdf, metadata)

                        # write zVariable data and associated variable
                        # attributes on the CDF
                        time_min, time_max, nrec = put_cdf_zvars(cdf, result)

                        # Fill Generation date
                        cdf.attrs[
                            'Generation_date'] = datetime.utcnow().isoformat()

                        # Fill file uuid
                        cdf.attrs['File_ID'] = str(uuid.uuid4())

                        # Fill TIME_MIN, TIME_MAX (in julian days)
                        cdf.attrs['TIME_MIN'] = str(
                            Time.tt2000_to_jd(time_min))
                        cdf.attrs['TIME_MAX'] = str(
                            Time.tt2000_to_jd(time_max))

                        # Add SPICE SCLK kernel as an entry
                        # of the "Kernels" g. attr
                        sclk_file = get_spice_kernels(time_instance=self.time_instance,
                                                      pattern='solo_ANC_soc-sclk_')
                        if sclk_file:
                            cdf.attrs['SPICE_KERNELS'] = sorted(sclk_file)[-1]
                        else:
                            logger.warning('No SPICE SCLK kernel '
                                           f'saved for {filepath}    [{self.job_id}]')

                        cdf.close()

                        if os.path.isfile(filepath):
                            logger.info(f'{filepath} saved')
                            self.processed_files.append(filepath)
                        else:
                            raise L1SurvProdFailure(f'{filepath} not found    [{self.job_id}]')
                    except NoData:
                        # close cdf
                        cdf.close()
                        # output CDF is outside time range, remove it
                        os.remove(filepath)
                    except:
                        logger.exception(f'{filepath} production has failed!    [{self.job_id}]')
                        self.failed_files.append(filepath)
                    finally:
                        target.filepath = filepath
