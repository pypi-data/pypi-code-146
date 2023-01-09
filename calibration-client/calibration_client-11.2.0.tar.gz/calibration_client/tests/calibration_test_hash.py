"""
This class is a Singleton created to allow us to access the current value
of the Calibration Hash used to test our code from any class and test instance.

That's necessary since we can only successfully retrieve a Calibration
Constant Version if the same was injected to the repository (Database)
"""

import logging
from datetime import datetime, timedelta

from pytz import timezone

__all__ = ['CalibrationTestHash']


class _CalibrationTestHash(object):
    def __init__(self, desired_begin_at=None):
        self.desired_begin_at = desired_begin_at

        self.valid_inject_01 = \
            _CalibrationTestHash._build_valid_test_hash_01(desired_begin_at)
        self.valid_inject_by_det_01 = \
            _CalibrationTestHash._build_valid_test_hash_03(desired_begin_at)
        self.valid_search_01 = \
            _CalibrationTestHash._build_valid_test_hash_02(desired_begin_at)
        self.valid_search_by_det_01 = \
            _CalibrationTestHash._build_valid_test_hash_04(desired_begin_at)

    @staticmethod
    def _build_valid_test_hash_01(desired_begin_at):
        logging.error('>' * 200 + ' _build_valid_test_hash_01 - INJECT')
        ccv_valid_dt = _CalibrationTestHash._gen_valid_ccv_datetime(
            desired_begin_at)

        valid_01_h = {
            'karabo_h': _CalibrationTestHash._build_valid_hash(ccv_valid_dt,
                                                               'inject'),
            'begin_validity_at_exp': ccv_valid_dt['begin_validity_at_exp'],
            'end_validity_at_exp': ccv_valid_dt['end_validity_at_exp'],
            'begin_at_exp': ccv_valid_dt['begin_at_exp']
        }

        return valid_01_h

    @staticmethod
    def _build_valid_test_hash_02(desired_begin_at):
        logging.error('>' * 200 + ' _build_valid_test_hash_02 - SEARCH')

        if desired_begin_at is None:
            desired_begin_at = '2016-10-11T17:57:19.757000'

        ccv_valid_dt = _CalibrationTestHash._gen_valid_ccv_datetime(
            desired_begin_at)

        valid_02_h = {
            'karabo_h': _CalibrationTestHash._build_valid_hash(ccv_valid_dt,
                                                               'search'),
            'begin_validity_at_exp': ccv_valid_dt['begin_validity_at_exp'],
            'end_validity_at_exp': ccv_valid_dt['end_validity_at_exp'],
            'begin_at_exp': ccv_valid_dt['begin_at_exp']
        }

        return valid_02_h

    @staticmethod
    def _build_valid_test_hash_03(desired_begin_at):
        logging.error(
            '>' * 200 + ' _build_valid_test_hash_03 - INJECT BY DETECTOR')
        ccv_valid_dt = _CalibrationTestHash._gen_valid_ccv_datetime(
            desired_begin_at)

        valid_03_h = {
            'karabo_h': _CalibrationTestHash._build_valid_hash(
                ccv_valid_dt, 'inject_by_detector'),
            'begin_validity_at_exp': ccv_valid_dt['begin_validity_at_exp'],
            'end_validity_at_exp': ccv_valid_dt['end_validity_at_exp'],
            'begin_at_exp': ccv_valid_dt['begin_at_exp']
        }

        return valid_03_h

    @staticmethod
    def _build_valid_test_hash_04(desired_begin_at):
        logging.error(
            '>' * 200 + ' _build_valid_test_hash_04 - SEARCH BY DETECTOR')

        if desired_begin_at is None:
            desired_begin_at = '2016-10-11T17:57:19.757000'

        ccv_valid_dt = _CalibrationTestHash._gen_valid_ccv_datetime(
            desired_begin_at)

        valid_04_h = {
            'karabo_h': _CalibrationTestHash._build_valid_hash(
                ccv_valid_dt, 'search_by_detector'),
            'begin_validity_at_exp': ccv_valid_dt['begin_validity_at_exp'],
            'end_validity_at_exp': ccv_valid_dt['end_validity_at_exp'],
            'begin_at_exp': ccv_valid_dt['begin_at_exp']
        }

        return valid_04_h

    @staticmethod
    def _loc(datetime_at, tz_str='Europe/Berlin'):
        tz = timezone(tz_str)

        datetime_at_tz = tz.localize(datetime_at)

        # Datetime should stop in the seconds
        # TODO, Milliseconds should be removed!!!!
        formatted_date_at = datetime_at_tz.isoformat()[:-13] + '.000'
        # formatted_date_at = datetime_at_tz.strftime("%Y-%M-%dT%H:%M:%S")
        # formatted_date_at = '{0}.000'.format(formatted_date_at)

        # And contain the timezone information in numeric values
        formatted_tz = datetime_at_tz.isoformat()[-6:]

        formatted_date_at = '{0}{1}'.format(formatted_date_at, formatted_tz)
        return formatted_date_at

    @staticmethod
    def _gen_valid_ccv_datetime(desired_begin_at):
        # begin_validity_at = '2013-10-16T23:52:41.000+02:00'
        begin_validity_at = '2013-10-17T00:52:41+03:00'
        begin_validity_at_exp = '2013-10-16T23:52:41.000+02:00'

        # NOW == '2015-11-17T16:35:38.006436'
        now = datetime.today()

        # begin_at = 2015-11-17T16:57:19.757+00:00
        # Subtract 1 hour because in Lisbon is one hour less than in Berlin
        insert_begin_at = now + timedelta(hours=-1)
        begin_at = _CalibrationTestHash._loc(insert_begin_at, 'Europe/Lisbon')

        if desired_begin_at is None:
            exp_begin_at = now
        else:
            exp_begin_at = datetime.strptime(desired_begin_at,
                                             '%Y-%m-%dT%H:%M:%S.%f')
            # exp_begin_at = now - timedelta(days=3* 365)

        begin_at_exp = _CalibrationTestHash._loc(exp_begin_at)

        #
        # end_validity_at = 2015-11-17T16:57:20.757+00:00
        # Subtract 1 hour because in Lisbon is one hour less than in Berlin
        insert_end_validity_at = now + timedelta(hours=-2, seconds=1)
        end_validity_at = _CalibrationTestHash._loc(insert_end_validity_at,
                                                    'Atlantic/Azores')

        # end_validity_at_exp = 2015-11-17T16:57:20.757+01:00
        exp_end_validity_at = now + timedelta(seconds=1)
        end_validity_at_exp = _CalibrationTestHash._loc(exp_end_validity_at)

        ccv_test_datetime_h = {
            'begin_validity_at': begin_validity_at,
            'begin_validity_at_exp': begin_validity_at_exp,
            'begin_at': begin_at,
            'begin_at_exp': begin_at_exp,
            'end_validity_at': end_validity_at,
            'end_validity_at_exp': end_validity_at_exp
        }

        return ccv_test_datetime_h

    @staticmethod
    # flg_mode:
    #  * inject -> prepare hash to be injected into DB
    #  * search -> prepare hash to be searched in DB (stable results)
    def _build_valid_hash(ccv_valid_dt, flg_mode):
        cc_name = 'test_inject_cc_unique_name'
        ccv_name = 'test_inject_name_{0}'.format(ccv_valid_dt['begin_at'])

        if flg_mode == 'inject':
            logging.error('>' * 200 + ' INJECT Mode')
            pdu_phy_name = 'PHYSICAL_DETECTOR_UNIT-2_DO_NOT_DELETE'
            # detector_id = -2
            detector_identifier = 'TEST_DET_CI-2'
            pdu_karabo_da = 'TEST_DAQ_DA_02'
            dev_type_name = 'UNIT_TEST_DETECTOR_TYPE-1_DO_NOT_DELETE'
            cal_name = 'CALIBRATION_TEST-1_DO_NOT_DELETE'
            param_1_val = 123.0
            param_2_val = 10.0

        elif flg_mode == 'inject_by_detector':
            logging.error('>' * 200 + ' INJECT Mode')
            pdu_phy_name = ''  # 'PHYSICAL_DETECTOR_UNIT-2_DO_NOT_DELETE'
            # detector_id = -2
            detector_identifier = 'TEST_DET_CI-2'
            pdu_karabo_da = 'TEST_DAQ_DA_02'
            dev_type_name = 'UNIT_TEST_DETECTOR_TYPE-1_DO_NOT_DELETE'
            cal_name = 'CALIBRATION_TEST-1_DO_NOT_DELETE'
            param_1_val = 123.0
            param_2_val = 10.0

        elif flg_mode == 'search':
            logging.error('>' * 200 + ' SEARCH Mode')
            pdu_phy_name = 'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE'
            # detector_id = -2
            detector_identifier = 'TEST_DET_CI-2'
            pdu_karabo_da = 'TEST_DAQ_DA_01'
            dev_type_name = 'UNIT_TEST_DETECTOR_TYPE-1_DO_NOT_DELETE'
            cal_name = 'CALIBRATION_TEST-2_DO_NOT_DELETE'
            param_1_val = 2.9
            param_2_val = 1.3

        elif flg_mode == 'search_by_detector':
            logging.error('>' * 200 + ' SEARCH Mode')
            pdu_phy_name = ''  # 'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE'
            # detector_id = -2
            detector_identifier = 'TEST_DET_CI-2'
            pdu_karabo_da = 'TEST_DAQ_DA_01'
            dev_type_name = 'UNIT_TEST_DETECTOR_TYPE-1_DO_NOT_DELETE'
            cal_name = 'CALIBRATION_TEST-2_DO_NOT_DELETE'
            param_1_val = 2.9
            param_2_val = 1.3

        else:
            logging.error('>' * 200 + ' NOT INJECT/SEARCH Mode')
            pdu_phy_name = 'PHYSICAL_DETECTOR_UNIT-3_DO_NOT_DELETE'
            # detector_id = -2
            detector_identifier = 'TEST_DET_CI-2'
            pdu_karabo_da = 'TEST_DAQ_DA_03'
            dev_type_name = 'UNIT_TEST_DETECTOR_TYPE-3_DO_NOT_DELETE'
            cal_name = 'CALIBRATION_TEST-3_DO_NOT_DELETE'
            param_1_val = 300.0
            param_2_val = 600.0

        report_h = {
            # If present, name and file_path must be unique!
            'name': 'this_is_my_1st_report.pdf',
            'file_path': '/gpfs/path/to/report/file/',
            'description': '',
        }

        detector_condition_h = {
            # 'name': '',  # If present, must be unique
            'flg_available': 1,  # [Default == 1 == True]
            'description': '',
            'parameters': [
                {
                    'parameter_name': 'PARAMETER_TEST-1_DO_NOT_DELETE',
                    'value': param_1_val,
                    'flg_logarithmic': 0,  # [Default == 0 == False]
                    'lower_deviation_value': 2,
                    'upper_deviation_value': 1,
                    'flg_available': 1,  # [Default == 0 == False]
                    'description': ''
                },
                {
                    'parameter_name': 'PARAMETER_TEST-2_DO_NOT_DELETE',
                    'value': param_2_val,
                    'flg_logarithmic': 0,  # [Default == 0 == False]
                    'lower_deviation_value': 0.1,
                    'upper_deviation_value': 0.05,
                    'flg_available': 1,  # [Default == 0 == False]
                    'description': ''
                }
            ]
        }

        cc_h = {
            'name': cc_name,  # If present, must be unique
            'detector_type_name': dev_type_name,
            'calibration_name': cal_name,
            'flg_available': 1,  # [Default == 1 == True]
            'flg_auto_approve': 1,
            'description': '',
        }

        path_to_file = 'xfel/cal/{0}/{1}/'.format(dev_type_name, pdu_phy_name)
        ccv_h = {
            'name': ccv_name,  # If present, must be unique

            # If pdu_physical_name is present,
            # detector_identifier and pdu_karabo_da are ignored
            'pdu_physical_name': pdu_phy_name,
            'detector_identifier': detector_identifier,
            'pdu_karabo_da': pdu_karabo_da,
            # end comment

            'path_to_file': path_to_file,
            'file_name': 'test_01',
            'flg_good_quality': 1,
            'begin_validity_at': ccv_valid_dt['begin_validity_at'],
            'end_validity_at': ccv_valid_dt['end_validity_at'],
            'begin_at': ccv_valid_dt['begin_at'],
            'raw_data_location': '/somewhere',
            'description': '',
            'start_idx': 0,
            'end_idx': 1,
            'data_set_name': cc_h['calibration_name']
        }

        valid_dict = {
            'report': report_h,
            'detector_condition': detector_condition_h,
            'calibration_constant': cc_h,
            'calibration_constant_version': ccv_h
        }

        return valid_dict


def init(desired_begin_at):
    global cal_test_hash
    cal_test_hash = _CalibrationTestHash(desired_begin_at)


def CalibrationTestHash(desired_begin_at):
    init(desired_begin_at)
    return cal_test_hash
