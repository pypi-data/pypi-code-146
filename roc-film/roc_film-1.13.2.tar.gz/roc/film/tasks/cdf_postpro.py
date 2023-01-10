#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to create the RPW L1 SBM1/SBM2 CDF files."""
import collections
import json
import os
import shutil
from datetime import datetime

from sqlalchemy import and_
import numpy as np
import uuid

import subprocess
from spacepy import pycdf

from maser.tools.cdf.cdfcompare import cdf_compare

from poppy.core.db.connector import Connector
from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget

from roc.rpl.time import Time
from roc.dingo.models.data import EventLog
from roc.dingo.tools import query_db
from roc.dingo.constants import PIPELINE_DATABASE

from roc.film import TIME_JSON_STRFORMAT, TIME_DOY1_STRFORMAT, TIME_DOY2_STRFORMAT
from roc.film.tools.file_helpers import is_output_dir, get_output_dir
from roc.film.tools import glob_list
from roc.film.constants import CDFEXPORT_PATH, TIMEOUT, CDF_POST_PRO_OPTS_ARGS, TIME_DAILY_STRFORMAT
from roc.film.exceptions import L1PostProError

__all__ = ['CdfPostPro']


class CdfPostPro(Task):

    """
    Task to post-process RPW CDFs
    """
    plugin_name = 'roc.film'
    name = 'cdf_post_pro'

    def add_targets(self):

        self.add_input(target_class=FileTarget,
                       identifier='cdf_file',
                       filepath=self.get_cdf_files(),
                       many=True)

        self.add_output(target_class=FileTarget,
                        identifier='cdf_file',
                        many=True)

    def get_cdf_files(self):
        try:
            return self.pipeline.args.cdf_files
        except:
            pass

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        try:
            self.cdf_file_list = glob_list(self.inputs['cdf_file'].filepath)
        except:
            raise ValueError(
                'No input target "cdf_file" passed')

        if not self.cdf_file_list:
            raise FileNotFoundError('Empty list of input cdf files')

        # Get list of RPW Soopkitchen Observations JSON files
        self.rpw_obs_json_list = glob_list(self.pipeline.get(
            'rpw_obs_json', default=[]))

        # Get list of RPW IOR XML files
        self.rpw_ior_xml_list = glob_list(self.pipeline.get(
            'rpw_ior_xml', default=[]))

        # Get post-processing options
        self.options = [opt.lower()
                        for opt in self.pipeline.get('options', default=[], args=True)
                        if opt.lower() in CDF_POST_PRO_OPTS_ARGS]
        if not self.options:
            raise ValueError('No valid argument passed in --options')

        # Get cdfexport path
        self.cdfexport = self.pipeline.get('cdfexport',
                                           default=[CDFEXPORT_PATH],
                                           )[0]
        if not self.cdfexport or not os.path.isfile(self.cdfexport):
            self.cdfexport = os.path.join(
                os.getenv('CDF_BIN', os.path.dirname(CDFEXPORT_PATH)), 'cdfexport')

        # get update-jon value
        self.update_json = self.pipeline.get('update_json',
                                           default=[None],
                                           )[0]
        if 'update_cdf' in self.options and (
            not self.update_json or not os.path.isfile(self.update_json)):
            raise ValueError('"update_cdf" input option needs a valid update_json file path to be run!')

        # Get overwrite boolean input
        self.overwrite = self.pipeline.get('overwrite',
                                           default=False,
                                           args=True)
        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Get products directory (folder where final output files will be
        # moved)
        self.products_dir = self.pipeline.get('products_dir',
                                              default=[None], args=True)[0]

        # Get output dir
        self.output_dir = get_output_dir(self.pipeline)
        if not is_output_dir(self.output_dir,
                             products_dir=self.products_dir):
            logger.debug(f'Making {self.output_dir}')
            os.makedirs(self.output_dir)
        else:
            logger.info(f'Output files will be '
                        f'saved into existing folder {self.output_dir}')

        # Get (optional) arguments for SPICE
        self.predictive = self.pipeline.get(
            'predictive', default=False, args=True)
        self.kernel_date = self.pipeline.get(
            'kernel_date', default=None, args=True)
        self.no_spice = self.pipeline.get('no_spice',
                                          default=False, args=True)
        # Get/create Time singleton
        self.time_instance = Time(predictive=self.predictive,
                                  kernel_date=self.kernel_date,
                                  no_spice=self.no_spice)


        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Initialize some class variables
        self.soop_type_list = []
        self.obs_id_list = []

        return True

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'CdfPostPro-{self.job_uuid[:8]}'
        logger.info(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                f'Initializing inputs has failed for {self.job_id}!')
            self.pipeline.exit()
            return

        # Loop over each input CDF file
        logger.info(f'{len(self.cdf_file_list)} input CDF files to post-process')
        for current_file in self.cdf_file_list:

            if self.overwrite:
                # If overwrite is set, then update current file
                logger.warning(f'{current_file} will be overwritten')
                self.current_file = current_file
            else:
                # Otherwise create a copy of the input CDF in the output
                # directory, then update the copy
                logger.info(f'Making a copy of {current_file} in {self.output_dir}')
                self.current_file = os.path.join(self.output_dir,
                                                 os.path.basename(current_file))
                shutil.copyfile(current_file, self.current_file)

            # Open CDF
            try:
                logger.debug(f'Opening and updating {self.current_file}...')
                # Open CDF to change what can be updated in one shot
                with pycdf.CDF(self.current_file) as cdf:
                    cdf.readonly(False)

                    # Get RPW CDF dataset ID
                    self.dataset_id = cdf.attrs['Dataset_ID'][0]

                    # Get Datetime attribute value (only first 8 characters)
                    self.datetime = datetime.strptime(cdf.attrs['Datetime'][0][:8],
                                                      TIME_DAILY_STRFORMAT)

                    # Get time range of the input L1 CDF
                    self.time_min = cdf['Epoch'][0]
                    self.time_max = cdf['Epoch'][-1]
                    logger.info(f'{self.current_file} has data '
                                f'between {self.time_min} and {self.time_max}')

                    # Set SOOP_TYPE global attribute from RPW SOOPKitchen
                    # export observation JSON files
                    if 'soop_type' in self.options:
                        self._set_soop_type(cdf)

                    # Set OBS_ID global attribute from IOR XML files (get
                    # observationID)
                    if 'obs_id' in self.options:
                        self._set_obs_id(cdf)

                    # Set quality_bitmask
                    if 'quality_bitmask' in self.options:
                        if 'QUALITY_BITMASK' in cdf:
                            self._set_bitmask(cdf)
                        else:
                            logger.debug(f'No "QUALITY_BITMASK" variable found in {self.current_file}: skip setting!')

                    # Resize TDS/LFR waveform array (only for TDS/LFR RSWF/TSWF
                    # products)
                    if 'resize_wf' in self.options:
                        # Only resize TDS RSWF/TSWF products
                        if 'RSWF' in self.dataset_id or 'TSWF' in self.dataset_id:
                            self._set_resize_wf(cdf)
                        else:
                            logger.debug(f'Resizing wf cannot be applied on {self.dataset_id}')

                    # Update CDF content with information in the input update_json file
                    if 'update_cdf' in self.options:
                        self._update_cdf(cdf)

                # Apply cdfexport to rebuild CDF properly
                if 'cdf_export' in self.options:
                    try:
                        self._run_cdfexport(self.current_file)
                    except FileNotFoundError:
                        logger.exception(f'Process has failed because file has not been found')
                        if self.current_file not in self.failed_files:
                            self.failed_files.append(self.current_file)
                    except subprocess.CalledProcessError as e:
                        logger.exception(f'Process has failed: \n {e}')
                        if self.current_file not in self.failed_files:
                            self.failed_files.append(self.current_file)
                    except subprocess.TimeoutExpired as e:
                        logger.exception(f'Process has expired: \n {e}')
                        if self.current_file not in self.failed_files:
                            self.failed_files.append(self.current_file)
                    except:
                        logger.exception(f'Process has failed!')
                        if self.current_file not in self.failed_files:
                            self.failed_files.append(self.current_file)

            except:
                logger.exception(f'Post-processing {self.current_file} has failed')
                if self.current_file not in self.failed_files:
                    self.failed_files.append(self.current_file)
            else:
                if not self.overwrite and self.current_file not in self.processed_files:
                    self.processed_files.append(self.current_file)

    def _run_cdfexport(self, cdf_file):
        """
        Run cdfexport tool for input CDF file

        :param cdf_file: cdf file to process with cdfexport
        :return: CompletedProcess object returned by subprocess.run()
        """

        # Check if cdfexport tool path exists
        if not os.path.isfile(self.cdfexport):
            raise FileNotFoundError(f'{self.cdfexport} not found')

        # Build command to run with subprocess.run
        cdf_without_ext = os.path.splitext(cdf_file)[0]
        new_cdf = f'{cdf_without_ext}__{str(uuid.uuid4())[:7]}'
        cmd = [self.cdfexport]
        cmd.append('-batch cdf')
        cmd.append(f'-cdf {new_cdf}')
        cmd.append('-initial "network"')
        cmd.append(cdf_without_ext)
        cmd = ' '.join(cmd)

        # run cdfexport
        logger.info(f'Running --> {cmd}')
        completed = subprocess.run(cmd,
                                   shell=True,
                                   check=True,
                                   timeout=TIMEOUT)

        new_cdf += '.cdf'
        if os.path.isfile(new_cdf):
            # First check that both files are the same
            if cdf_compare(new_cdf, cdf_file):
                os.remove(new_cdf)
                raise L1PostProError(f'Running cdfexport on {cdf_file} has failed!')
            else:
                logger.debug(f'{cdf_file} and {new_cdf} are identical')
                os.remove(cdf_file)
                os.rename(new_cdf, cdf_file)
        else:
            raise FileNotFoundError(f'{new_cdf} not found')

        return completed

    def _set_resize_wf(self, cdf_obj):
        """
        Resize Waveform array in the input CDF.

        WARNING: At the end, WF arrays will be resized,
        but CDF file size will remain unchanged.
        To make sure to have the final CDF size,
        run cdf_post_pro with cdf_export option

        :param cdf_cdf_obj: CDF to update (passed as a spacepy.pycdf.CDF class instance)
        :return: True if resizing has succeeded, False otherwise
        """
        is_succeeded = True

        # pycdf.lib.set_backward(False)

        logger.info(f'Resizing waveform data array in {self.current_file} ...')
        try:
            # Get max number of data samples in the file
            max_samp_per_ch = np.max(cdf_obj['SAMPS_PER_CH'][...])

            # Loop over old CDF zVariables
            for varname in cdf_obj:
                if (varname == 'WAVEFORM_DATA' or
                        varname == 'WAVEFORM_DATA_VOLTAGE' or
                        varname == 'B'):
                    old_var = cdf_obj[varname]
                    # Re-size waveform data array
                    if len(old_var.shape) == 2:
                        new_var_data = old_var[
                            :, :max_samp_per_ch]
                        new_var_dims = [new_var_data.shape[1]]
                    elif len(old_var.shape) == 3:
                        new_var_data = old_var[
                            :, :, :max_samp_per_ch]
                        new_var_dims = [new_var_data.shape[
                            1], new_var_data.shape[2]]
                    else:
                        raise IndexError

                    logger.debug(f'Resizing {varname} zVar '
                                 f'from {old_var.shape} to {new_var_data.shape} '
                                 f'in {self.current_file}')

                    # Create temporary new zVar with the new shape
                    temp_varname = f'{varname}__TMP'
                    cdf_obj.new(temp_varname,
                                   data=new_var_data,
                                   recVary=old_var.rv(),
                                   dimVarys=old_var.dv(),
                                   type=old_var.type(),
                                   dims=new_var_dims,
                                   n_elements=old_var.nelems(),
                                   compress=old_var.compress()[0],
                                   compress_param=old_var.compress()[1],
                                   )

                    # Copy zVar attributes
                    cdf_obj[temp_varname].attrs = cdf_obj[varname].attrs

                    # Delete old zVar
                    del cdf_obj[varname]

                    # Rename temporary zVar with expected name
                    cdf_obj[temp_varname].rename(varname)

        except:
            raise L1PostProError(f'Resizing {self.current_file} has failed!')
        else:
            # make sure to save the change
            cdf_obj.save()

        return is_succeeded

    def _set_soop_type(self, cdf_obj):
        """
        Set input CDF file with expected value for SOOP_TYPE g.attribute.

        :param cdf_obj: CDF to update (passed as a spacepy.pycdf.CDF class instance)
        :return: True if SOOP_TYPE has been set, False otherwise
        """

        logger.info(f'Setting SOOP_TYPE global attribute in {self.current_file} ...')

        # Get list of SOOP type from RPW soopkitchen observation json files
        if not self.soop_type_list:
            logger.info(
                f'Extracting soopType elements from input list of {len(self.rpw_obs_json_list)} RPW SoopKitchen JSON files...')
            self.soop_type_list = CdfPostPro.get_soop_type(
                self.rpw_obs_json_list)

        # Only keep list of soop type betwen time_min and time_max
        soop_type_list = [current_soop_type['soopType']
                          for current_soop_type in self.soop_type_list
                          if (datetime.strptime(current_soop_type['startDate'], TIME_JSON_STRFORMAT) <= self.time_max and
                              datetime.strptime(current_soop_type['endDate'], TIME_JSON_STRFORMAT) >= self.time_min)]

        soop_type_len = len(soop_type_list)
        if soop_type_len == 0:
            logger.warning(f'No Soop Type value found between {self.time_min} and {self.time_max}')
            return False
        else:
            cdf_obj.attrs['SOOP_TYPE'] = list(set(soop_type_list))
            logger.debug(f'SOOP_TYPE = {soop_type_list} in {self.current_file}')
            logger.info(f'{soop_type_len} entries set for SOOP_TYPE in {self.current_file}')

        # make sure to save the change
        cdf_obj.save()

        return True

    @staticmethod
    def get_soop_type(rpw_obs_json_list):
        """
        Return list of SOOP_TYPE values for a given set of input RPW SoopKitchen observation JSON files

        :param rpw_obs_json_list: List of input RPW SK JSON files
        :return: list of SOOP_TYPE values found
        """

        # Define sub-method
        def extract_soop_type(json_file):
            """Extract soopType from input JSON"""

            # Open JSON file
            with open(json_file, 'r') as json_buff:
                data = json.load(json_buff)

            # Retrieve all "soopType" field from file
            return data['soops']

        # Initialize output list
        soop_type_list = []

        for current_json in rpw_obs_json_list:
            soop_type_list.extend(extract_soop_type(
                current_json))

        return soop_type_list

    def _set_obs_id(self, cdf_obj):
        """
        Set input CDF file with expected value for OBS_ID g.attribute.

        :param cdf_obj: CDF to update (passed as a spacepy.pycdf.CDF class instance)
        :return: True if OBS_ID has been set, False otherwise
        """

        logger.info(f'Setting OBS_ID global attribute in {self.current_file} ...')

        # Get list of RPW TC obs id values
        if not self.obs_id_list:
            logger.info(
                f'Extracting uniqueID elements from input list of {len(self.rpw_ior_xml_list)} RPW IOR files...')
            self.obs_id_list = CdfPostPro.get_ior_obs_id(self.rpw_ior_xml_list)

        # Keep only obs_id between time_min and time_max
        obs_id_list = [current_tc[1]
                       for current_tc in self.obs_id_list
                       if (current_tc[0] <= self.time_max and
                           current_tc[0] >= self.time_min)
                       ]

        obs_id_len = len(obs_id_list)
        if obs_id_len == 0:
            logger.warning(f'No OBS_ID value found between {self.time_min} and {self.time_max}')
            return False
        else:
            cdf_obj.attrs['OBS_ID'] = sorted(list(set(obs_id_list)))
            logger.debug(f'OBS_ID = {obs_id_list} in {self.current_file}')
            logger.info(f'{obs_id_len} entries set for OBS_ID in {self.current_file}')

        # make sure to save the change
        cdf_obj.save()

        return True

    @staticmethod
    def get_ior_obs_id(rpw_ior_xml_list):
        """
        Return list of OBS_ID values from
        an input list of RPW IOR XML files

        :param rpw_ior_xml_list: List of input RPW TC XML files.
                                 (ZIP files containing IOR XML can be also passed).
        :return: list of OBS_ID values found
        """
        import zipfile

        # Define sub-method
        def extract_obs_id(xml):
            """
            Extract OBS_ID from input XML

            :param xml: input IOR XML stream
            :return: List of (time, observationID) values extracted from IOR
            """
            import xmltodict

            # Convert input IOR XML stream into dictionary
            logger.debug(f'Parsing {xml} ...')
            data = xmltodict.parse(xml.read())

            # Extract list of sequences
            sequence_list = data['planningData'] \
                ['commandRequests']['occurrenceList'] \
                ['sequence']

            # Make sure that returned sequence_list is a list
            # (If only one sequence tag is found in the XML
            # the xml_to_dict method returns a collections.OrderedDict()
            # instance).
            if not isinstance(sequence_list, list):
                sequence_list = [sequence_list]

            # Retrieve all "observationID" field from input TC XML file
            # Return as a list of tuple (ExecutionTime, observationID)
            ior_seq_list = []
            for current_seq in sequence_list:
                # Make sure to retrieve executionTime with the
                # right time format (two are possible)
                for current_strtformat in [TIME_DOY1_STRFORMAT, TIME_DOY2_STRFORMAT]:
                    current_time = cast_ior_seq_datetime(
                        current_seq, current_strtformat)
                    if current_time is not None:
                        break
                current_obsid = current_seq['observationID'] if current_seq[
                    'observationID'] is not None else ' '

                ior_seq_list.append((current_time, current_obsid))

            return ior_seq_list

        # Initialize output list
        obs_id_list = []

        for current_file in rpw_ior_xml_list:
            if not os.path.basename(current_file).startswith('IOR'):
                logger.debug(f'{current_file} not a valid RPW IOR file, skip it')
                continue

            if zipfile.is_zipfile(current_file):
                with zipfile.ZipFile(current_file, 'r') as zip_stream:
                    for current_xml in zip_stream.namelist():
                        with zip_stream.open(current_xml, 'r') as ior_xml:
                            if ior_xml.name.startswith('IOR') and ior_xml.name.endswith('.SOL'):
                                obs_id_list.extend(extract_obs_id(ior_xml))
                            else:
                                logger.debug(f'{current_xml} is not a valid RPW IOR XML file, skip it')
            else:
                with open(current_file, 'r') as ior_xml:
                    obs_id_list.extend(extract_obs_id(ior_xml))

        return obs_id_list

    def _update_cdf(self, cdf_obj):
        """
        Update content of input CDF

        :param cdf_obj: spacepy.pycdf.CDF object containing input file data
        :return:
        """
        # Get info in the input JSON file
        try:
            with open(self.update_json, 'r') as jsonfile:
                update_data = json.load(jsonfile)
            update_data = update_data['updates']
        except:
            raise L1PostProError(f'Cannot parsing {self.update_json}')

        # Loop over each updates item
        for key, val in update_data.items():
            # Filter dataset to update
            if key not in self.dataset_id:
                logger.info(f'Skipping {self.current_file} for updating CDF: {self.dataset_id} not concerned')
                continue

            # Filter time range
            validity_start = datetime.strptime(val['validity_range']['start_time'],
                             TIME_DAILY_STRFORMAT)
            validity_end = datetime.strptime(val['validity_range']['end_time'],
                           TIME_DAILY_STRFORMAT)
            if self.datetime.date() < validity_start.date():
                logger.info(f'Skipping {self.current_file} for updating CDF: older than {validity_start.date()}')
                continue

            if self.datetime.date() > validity_end.date():
                logger.info(f'Skipping {self.current_file} for updating CDF: newer than {validity_end.date()}')
                continue

            # Run update for global attributes if any
            for gattr in val['globals']:
                gname = gattr['name']
                for gvalue in gattr['values']:
                    try:
                        cdf_obj.attrs[gname] = gvalue
                    except:
                        raise L1PostProError(f'Cannot update global attribute {gname} in {self.current_file}')
                    else:
                        logger.info(f'Global attribute {gname} updated in {self.current_file} with values {gvalue}')

            # Run update for zVariables if any
            for zvar in val['zvars']:
                zname = zvar['name']
                zvalues = zvar['values']
                nrec = cdf_obj[zname].shape[0]
                try:
                    cdf_obj[zname] = [zvalues] * nrec
                except:
                    raise L1PostProError(f'Cannot update zVariable {zname} [{nrec}] in {self.current_file}')
                else:
                    logger.info(f'zVariable {zname} updated in {self.current_file} with values {zvalues}')

        # make sure to save the change
        cdf_obj.save()

    def _set_bitmask(self, cdf_obj):
        """
        Set the QUALITY_BITMASK zVariable in RPW L1 CDF.
        See https://confluence-lesia.obspm.fr/display/ROC/RPW+Data+Quality+Verification

        :param cdf_obj: spacepy.pycdf.CDF object containing input file data
        :return: None
        """
        # Restore Epoch values and get number of records in CDF
        epoch = cdf_obj['Epoch'][...]
        nrec = epoch.shape[0]

        # Initialize quality_bitmask
        bitmask = np.zeros(nrec, dtype=np.uint16)
        #bitmask[:] = 65535

        # Get list of events to store in bitmask between time_min and time_max
        # Define filters
        model = EventLog
        filters = [model.start_time >= self.time_min]
        filters.append(model.end_time <= self.time_max)
        event_log = query_db(self.session, model,
                             filters=and_(filters))
        if event_log.shape[0] == 0:
            logger.warning(f'No event_log entry found between {self.time_min} and {self.time_max}')
        else:
            # Loop over CDF records to fill quality_bitmask
            for i, current_epoch in enumerate(epoch):
                # Initialize current bitmask
                current_bitmask = np.uint16(0)

                # BIAS SWEEP on ANT1
                if (event_log['label'] == 'BIA_SWEEP_ANT1' and
                event_log['start_time'] <= current_epoch and
                event_log['end_time'] >= current_epoch):
                    # Set 1st bit (X)
                    current_bitmask = current_bitmask | 1

                # BIAS SWEEP on ANT2
                if (event_log['label'] == 'BIA_SWEEP_ANT2' and
                event_log['start_time'] <= current_epoch and
                event_log['end_time'] >= current_epoch):
                    # Set 2nd bit (X0)
                    current_bitmask = current_bitmask | 2

                # BIAS SWEEP on ANT3
                if (event_log['label'] == 'BIA_SWEEP_ANT3' and
                event_log['start_time'] <= current_epoch and
                event_log['end_time'] >= current_epoch):
                    # Set 3rd bit (X00)
                    current_bitmask = current_bitmask | 4

                # EMC_MAND_QUIET
                if (event_log['label'] == 'EMC_MAND_QUIET' and
                event_log['start_time'] <= current_epoch and
                event_log['end_time'] >= current_epoch):
                    # Set 4th bit (X000)
                    current_bitmask = current_bitmask | 8

                # EMC_PREF_NOISY
                if (event_log['label'] == 'EMC_PREF_NOISY' and
                event_log['start_time'] <= current_epoch and
                event_log['end_time'] >= current_epoch):
                    # Set 5th bit (X0000)
                    current_bitmask = current_bitmask | 16

                # Spacecraft roll manoeuvre
                if ('ROLL' in event_log['label']  and
                event_log['start_time'] <= current_epoch and
                event_log['end_time'] >= current_epoch):
                    # Set 6th bit (X00000)
                    current_bitmask = current_bitmask | 32

                # Thruster firing
                if (event_log['label'].isin(['TCM', 'WOL']) and
                event_log['start_time'] <= current_epoch and
                event_log['end_time'] >= current_epoch):
                    current_bitmask = current_bitmask | 64

                # Store current bitmask
                bitmask[i] = current_bitmask

            # Save quality_bitmask
            cdf_obj['QUALITY_BITMASK'] = bitmask



        # make sure to save the change
        cdf_obj.save()

def cast_ior_seq_datetime(current_seq, strtformat):
    """
    cast the execution time of the input IOR sequence element into datetime object
    """
    try:
        seq_datetime = datetime.strptime(current_seq['executionTime'][
            'actionTime'], strtformat)
    except:
        seq_datetime = None

    return seq_datetime
