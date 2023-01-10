#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to create the RPW L1 SBM1/SBM2 CDF files."""
import os
from datetime import timedelta
import uuid

from spacepy.pycdf import CDF

from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget
from roc.film.tools.l0 import L0

from roc.rpl.time import Time
from roc.rpl.packet_parser import raw_to_eng

from roc.film.tools.file_helpers import get_l0_files, l0_to_trange_cdf, get_output_dir, is_output_dir, get_l0_trange

from roc.film.constants import TIME_JSON_STRFORMAT

__all__ = ['L0ToL1Sbm']

# SBM1 QF TF ID
TF_PA_DPU_0038 = 'CIWP0028TM'
# SBM2 QF TF ID
TF_PA_DPU_0039 = 'CIWP0029TM'


class L0ToL1Sbm(Task):
    """
    Task to generate l1 sbm CDF from l0 file(s)
    """
    plugin_name = 'roc.film'
    name = 'l0_to_l1_sbm'

    def add_targets(self):

        self.add_input(target_class=FileTarget,
                       identifier='l0_file',
                       filepath=get_l0_files,
                       many=True)

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm1_rswf')

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm2_tswf')

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm1_cwf')

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm1_bp1')

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm1_bp2')

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm2_cwf')

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm2_bp1')

        self.add_output(target_class=FileTarget,
                        identifier='l1_sbm2_bp2')

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

        # Get (optional) arguments for SPICE
        predictive = self.pipeline.get('predictive', default=False, args=True)
        kernel_date = self.pipeline.get('kernel_date', default=None, args=True)
        no_spice = self.pipeline.get('no_spice', default=False, args=True)

        # Get/create Time singleton
        self.time = Time(predictive=predictive,
                         kernel_date=kernel_date,
                         no_spice=no_spice)

        # Get list of input l0 file(s)
        self.l0_file_list = self.inputs['l0_file'].filepath

        # Get or create failed_files list from pipeline properties
        self.failed_files = self.pipeline.get(
            'failed_files', default=[], create=True)

        # Get or create processed_files list from pipeline properties
        self.processed_files = self.pipeline.get(
            'processed_files', default=[], create=True)

        # Get overwrite argument
        self.overwrite = self.pipeline.get(
            'overwrite', default=False, args=True)

        # Get force optional keyword
        self.force = self.pipeline.get('force', default=False, args=True)

        # Get --cdag keyword
        self.is_cdag = self.pipeline.get('cdag', default=False, args=True)

        # Get --no-sbm1/2 ans --as-is keywords
        self.no_sbm1 = self.pipeline.get('no_sbm1', default=False, args=True)
        self.no_sbm2 = self.pipeline.get('no_sbm2', default=False, args=True)
        self.manual = self.pipeline.get('manual', default=False, args=True)

        # Define output file start time
        self.start_time = self.pipeline.get('start_time', default=[None])[0]
        logger.debug(f'start_time value is {self.start_time}')

        # Define output file end time
        self.end_time = self.pipeline.get('end_time', default=[None])[0]
        logger.debug(f'end_time value is {self.end_time}')

        # Define SBM type (only used with --as-is optional keyword)
        self.sbm_type = self.pipeline.get('sbm_type', default=[None])[0]
        logger.debug(f'sbm_type value is {self.sbm_type}')

        return True

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'L0ToL1Sbm-{self.job_uuid[:8]}'
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

        if self.manual:
            # If 'manual' option is passed, then try to
            # process straightly the SBM packet data found in the input L0 files
            logger.info(
                f'Try to process data manually    [{self.job_id}]')

            # Define time range to process
            if not self.start_time and not self.end_time:
                # If not passed as inputs, take min/max L0 time range
                l0_time_min, l0_time_max = get_l0_trange(self.l0_file_list)
                start_time = min(l0_time_min)
                end_time = max(l0_time_max)
            else:
                start_time = self.start_time
                end_time = self.end_time

            if not self.sbm_type:
                logger.warning('--sbm-type argument value is not passed!')
            elif self.sbm_type and self.sbm_type not in [1,2]:
                logger.error('--sbm-type argument value is not valid: must be 1 or 2!')
                self.pipeline.exit()

            sbm_list = [{'start_time': start_time,
                         'end_time': end_time,
                         # We do not know DT?_SBM? parameters here, so assume
                         # that SBM event occurrence time is in the center of the window
                         'sbm_time': start_time + 0.5 * (end_time - start_time),
                         'sbm_l0': self.l0_file_list,
                         'sbm_type': self.sbm_type}]
            sbm_num = 1
        else:

            # Build list of sbm events by looking for
            # TM_DPU_EVENT_PR_DPU_SBM1 or TM_DPU_EVENT_PR_DPU_SBM2 packets in input L0 files
            logger.info(f'Building list of SBM events to process...    [{self.job_id}]')
            sbm_list = self._build_sbm_list(self.l0_file_list,
                                            start_time=self.start_time,
                                            end_time=self.end_time,
                                            no_sbm1=self.no_sbm1,
                                            no_sbm2=self.no_sbm2)

            sbm_num = len(sbm_list)
            if sbm_num == 0:
                logger.info('No SBM detection event found in input L0 files    [{self.job_id}]')
                return
            else:
                logger.info(f'{sbm_num} SBM events to process    [{self.job_id}]')

        # Initialize loop variables
        l1_cdf_path = None

        # Loop over each SBM event in the list
        for i, current_sbm in enumerate(sbm_list):

            # Get info of current sbm event
            sbm_start_time = current_sbm['start_time']
            sbm_end_time = current_sbm['end_time']
            sbm_time = current_sbm['sbm_time']
            sbm_l0_list = current_sbm['sbm_l0']
            sbm_type = current_sbm.get('sbm_type', 'UNKNOWN')
            sbm_qf = current_sbm.get('sbm_qf', 'UNKNOWN')
            sbm_algo = current_sbm.get('sbm_algo', 'UNKNOWN')
            sbm_duration = current_sbm.get('sbm_duration', 'UNKNOWN')
            if sbm_type != 'UNKNOWN':
                logger.info(f'Processing SBM{sbm_type} event detected '
                            f"between {current_sbm['start_time']} and "
                            f"{current_sbm['end_time']}... ({sbm_num - i} events remaining)    [{self.job_id}]")

            try:
                # Generate L1 CDF from L0 files
                l1_cdf_path = l0_to_trange_cdf(self, 'l0_to_l1_sbm',
                                               sbm_l0_list, self.output_dir,
                                               start_time=sbm_start_time,
                                               end_time=sbm_end_time,
                                               failed_files=self.failed_files,
                                               processed_files=self.processed_files,
                                               is_cdag=self.is_cdag,
                                               overwrite=self.overwrite)
            except:
                logger.exception(f'L1 SBM CDF production has failed!    [{self.job_id}]')
                if not l1_cdf_path:
                    l1_cdf_path = [os.path.join(
                        self.output_dir, '.l0_to_l1_sbm_failed')]
                if l1_cdf_path[0] not in self.failed_files:
                    self.failed_files.append(l1_cdf_path[0])
                return

            if l1_cdf_path and os.path.isfile(l1_cdf_path[0]):
                # Open CDF and add some extra information about SBM event
                # parameters
                logger.info(f'Filling {l1_cdf_path[0]} file with SBM event parameters...    [{self.job_id}]')
                cdf = None
                try:
                    cdf = CDF(l1_cdf_path[0])
                    cdf.readonly(False)

                    # Add QF, detection time, duration and algo type
                    # as g. attributes
                    # TODO - Add also in CDF skeletons
                    cdf.attrs['SBM_QUALITY_FACTOR'] = str(sbm_qf)
                    cdf.attrs['SBM_DURATION'] = str(sbm_duration)
                    cdf.attrs['SBM_ALGO_TYPE'] = str(sbm_algo)
                    cdf.attrs['SBM_TIME'] = sbm_time.strftime(
                        TIME_JSON_STRFORMAT)

                except:
                    logger.exception(
                        'Filling L1 SBM CDF with SBM parameter has failed!    [{self.job_id}]')
                    if l1_cdf_path[0] not in self.failed_files:
                        self.failed_files.append(l1_cdf_path[0])

                else:
                    logger.info(f'{l1_cdf_path[0]} filled with SBM parameters    [{self.job_id}]')
                    if l1_cdf_path[0] not in self.processed_files:
                        self.processed_files.append(l1_cdf_path[0])
                finally:
                    if cdf:
                        cdf.close()

    def _build_sbm_list(self, l0_file_list,
                        start_time=None,
                        end_time=None,
                        no_sbm1=False,
                        no_sbm2=False,
                        ):
        """
        Build list of SBM events to process
        from an input set of l0 files.

        :param l0_file_list: set of input l0 files to process
        :param start_time: Filter data by start time
        :param end_time: Filter data by end_time
        :param no_sbm1: If True, do not include SBM1 event in the output list
        :param no_sbm2: If True, do not include SBM1 event in the output list
        :return: list of sbm events to process
        """

        # Initialize output list
        sbm_event_list = []

        expected_packet_list = []
        if not no_sbm1:
            expected_packet_list.append('TM_DPU_EVENT_PR_DPU_SBM1')
        if not no_sbm2:
            expected_packet_list.append('TM_DPU_EVENT_PR_DPU_SBM2')

        if not expected_packet_list:
            logger.warning('--no-sbm1 and --no-sbm2 keywords '
                           'should not be passed together!')
        else:
            # Extract wanted packets and re-order by increasing time
            sbm_packet_list = L0.l0_to_raw(l0_file_list,
                                           expected_packet_list=expected_packet_list,
                                           start_time=start_time,
                                           end_time=end_time,
                                           increasing_time=True,
                                           )['packet_list']
            if sbm_packet_list:

                for current_packet in sbm_packet_list:

                    current_time = current_packet['utc_time']
                    current_name = current_packet['palisade_id']
                    current_data = current_packet['data']

                    current_idb_source = current_packet['idb_source']
                    current_idb_version = current_packet['idb_version']

                    # Get SBM event parameters
                    current_sbm_type = int(current_name[-1])
                    # Get SBM detection time (UTC)
                    current_sbm_time = Time().obt_to_utc(
                        current_data[f'HK_RPW_S20_SBM{current_sbm_type}_TIME_D'][:2].reshape([1, 2]),
                        to_datetime=True)[0]

                    # Get algo
                    current_sbm_algo = current_data[f'SY_DPU_SBM{current_sbm_type}_ALGO']

                    # Get SBM duration
                    # (see SSS or DAS User manual for details)
                    if current_sbm_type == 1:
                        current_sbm_dt1_sbm1 = current_data[
                            'SY_DPU_SBM1_DT1_SBM1_D']
                        current_sbm_dt2_sbm1 = current_data[
                            'SY_DPU_SBM1_DT2_SBM1_D']
                        current_sbm_dt3_sbm1 = current_data[
                            'SY_DPU_SBM1_DT3_SBM1_D']
                        current_sbm_qf = sbm1_qf_eng(current_data['HK_RPW_S20_SBM1_QF_D'],
                                                     idb_source=current_idb_source,
                                                     idb_version=current_idb_version)
                        logger.debug(
                            f'Current SBM1 event parameters: [{current_sbm_dt1_sbm1}, {current_sbm_dt2_sbm1}, {current_sbm_dt3_sbm1}, {current_sbm_qf}]')
                        # Set SBM1 duration
                        current_sbm_duration = int(current_sbm_dt2_sbm1)
                        # Get SBM1 start/end time (UTC)
                        if current_sbm_dt2_sbm1 < 2 * current_sbm_dt1_sbm1:
                            current_sbm_end = current_sbm_time + \
                                              timedelta(seconds=int(
                                                  current_sbm_dt1_sbm1))
                            current_sbm_start = current_sbm_end - \
                                                timedelta(seconds=int(current_sbm_duration))
                        elif current_sbm_dt2_sbm1 > 2 * current_sbm_dt1_sbm1:
                            current_sbm_end = current_sbm_time + \
                                              timedelta(
                                                  seconds=int(current_sbm_dt1_sbm1 + current_sbm_dt3_sbm1))
                            current_sbm_start = current_sbm_end - \
                                                timedelta(seconds=current_sbm_duration)
                        else:
                            current_sbm_start = current_sbm_time - timedelta(
                                seconds=(current_sbm_duration / 2))
                            current_sbm_end = current_sbm_time + timedelta(
                                seconds=(current_sbm_duration / 2))

                    elif current_sbm_type == 2:
                        current_sbm_duration = current_data[
                            'HK_DPU_SBM2_DT_SBM2']
                        current_sbm_qf = sbm2_qf_eng(current_data['HK_RPW_S20_SBM2_QF_D'],
                                                     idb_source=current_idb_source,
                                                     idb_version=current_idb_version)
                        # Get SBM2 start/end time (UTC)
                        current_sbm_start = current_sbm_time
                        current_sbm_end = current_sbm_time + timedelta(
                            seconds=(int(current_sbm_duration) + 1))

                        logger.debug(f'Current SBM2 event parameters: [{current_sbm_duration}, {current_sbm_qf}]')
                    else:
                        logger.error(f'Wrong SBM type: {current_sbm_type}! (should be 1 or 2)')
                        continue

                    # Extend start_time/end_time by 1 minutes
                    # see https://gitlab.obspm.fr/ROC/RCS/LFR_CALBUT/-/issues/69
                    current_sbm_start -= timedelta(minutes=1)
                    current_sbm_end += timedelta(minutes=1)

                    # Get corresponding list of L0 files
                    current_sbm_l0 = L0.filter_l0_files(
                        l0_file_list,
                        start_time=current_sbm_start,
                        end_time=current_sbm_end)

                    # add current event to the list of events to return
                    sbm_event_list.append(
                        {'start_time': current_sbm_start,
                         'end_time': current_sbm_end,
                         'sbm_time': current_sbm_time,
                         'sbm_type': current_sbm_type,
                         'sbm_duration': current_sbm_duration,
                         'sbm_algo': current_sbm_algo,
                         'sbm_qf': current_sbm_qf,
                         'sbm_l0': current_sbm_l0}
                    )

        return sbm_event_list


def sbm1_qf_eng(raw_values, tf_srdb_id=TF_PA_DPU_0038,
                idb_source='MIB', idb_version=None):
    """
    Retrieve engineering values of the SBM1 event quality factor

    :param raw_values: SBM1 QF raw values
    :param tf_srdb_id: SBM1 F Transfer function SRDB ID
    :param idb_source:
    :param idb_version:
    :return: engineering values of SBM1 QF
    """
    return raw_to_eng(raw_values, tf_srdb_id,
                      idb_source=idb_source, idb_version=idb_version)


def sbm2_qf_eng(raw_values, tf_srdb_id=TF_PA_DPU_0039,
                idb_source='MIB', idb_version=None):
    """
     Retrieve engineering values of the SBM2 event quality factor

    :param raw_values: SBM2 QF raw values
    :param tf_srdb_id: SBM2 QF Transfer function SRDB ID
    :param idb_source:
    :param idb_version:
    :return: engineering values of SBM1 QF
    """
    return raw_to_eng(raw_values, tf_srdb_id,
                      idb_source=idb_source, idb_version=idb_version)
