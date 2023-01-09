"""CalibrationClient class"""

import logging
from time import gmtime
from time import strftime

from .apis import (
    CalibrationApi, CalibrationConstantApi, CalibrationConstantVersionApi,
    ConditionApi, ParameterApi, DetectorApi, DetectorTypeApi,
    PhysicalDetectorUnitApi, ReportApi,
    UserApi,
)
from .common.util import Util
from .modules import (
    Calibration, CalibrationConstant, CalibrationConstantVersion,
    Condition, Parameter, Detector, DetectorType, PhysicalDetectorUnit,
    Report,
)


class CalibrationClient(CalibrationApi,
                        CalibrationConstantApi,
                        CalibrationConstantVersionApi,
                        ConditionApi, ParameterApi,
                        DetectorApi, DetectorTypeApi, PhysicalDetectorUnitApi,
                        ReportApi, UserApi):

    # The parent classes define methods to make requests to different parts
    # of the API, e.g. .get_calibration_constant_version_by_id_api()
    # They all inherit from .common.base.Base which handles the oauth session.

    # Wrapper methods which may make several API calls: -------------------

    def set_calibration_constant(self, condition, cc_h):
        logging.debug('condition: {0}'.format(condition))
        logging.debug('calibration_constant: {0}'.format(cc_h))

        #
        calibration_name = cc_h['calibration_name']
        resp = Calibration.get_by_name(self, calibration_name)
        calibration_id = resp['data']['id']

        detector_type_name = cc_h['detector_type_name']
        resp = DetectorType.get_by_name(self, detector_type_name)
        detector_type_id = resp['data']['id']

        condition_name = condition['name']
        condition_id = condition['id']

        # Generate unique name if it doesn't exist
        cc_name_01 = '{0}_{1}'.format(detector_type_name, calibration_name)
        cc_name_uk = '{0}_{1}'.format(cc_name_01[:40], condition_name)
        cc_name = Util.get_opt_hash_val(cc_h, 'name', cc_name_uk)

        #
        cc_desc = Util.get_opt_hash_val(cc_h, 'description')
        cc_flg_auto_approve = Util.val_to_api_bool(cc_h['flg_auto_approve'])
        cc_flg_avail = Util.get_opt_hash_val(cc_h, 'flg_available', 'true')

        cal_cc = {
            'name': cc_name,
            'calibration_id': str(calibration_id),
            'detector_type_id': str(detector_type_id),
            'condition_id': str(condition_id),
            'flg_auto_approve': cc_flg_auto_approve,
            'flg_available': cc_flg_avail,
            'description': cc_desc
        }
        logging.debug('Built Calibration CC: {0}'.format(cal_cc))

        #
        # SET cc from dictionary
        #
        return CalibrationConstant.set_from_dict(self, cal_cc)

    def get_physical_detector_unit(self, cal_dict):
        #
        # Expected keys:
        #
        # MODE: by_physical_detector_unit_name
        # 1) cal_dict['pdu_physical_name']
        #
        #   -- OR --
        #
        # MODE: by_detector_id_and_karabo_da
        # 2) cal_dict['detector_identifier']
        # 2) cal_dict['pdu_karabo_da']
        #
        if 'pdu_physical_name' in cal_dict.keys():
            if cal_dict['pdu_physical_name'] == '' or \
                    cal_dict['pdu_physical_name'] is None:
                mode = 'by_detector_id_and_karabo_da'
            else:
                mode = 'by_physical_detector_unit_name'
        else:
            mode = 'by_detector_id_and_karabo_da'

        # Taking action accordingly to the mode
        if mode == 'by_physical_detector_unit_name':
            pdu_physical_name = cal_dict['pdu_physical_name']
            logging.debug(
                'phy_det_unit.physical_name: {0}'.format(pdu_physical_name))
            logging.debug('detector_identifier: NOT_EVALUATED')
            logging.debug('phy_det_unit.karabo_da: NOT_EVALUATED')

            resp = PhysicalDetectorUnit.get_by_name(self, pdu_physical_name)

            if resp['success']:
                physical_detector_unit = resp['data']

                success_msg = 'phy_det_unit.id: {0}'.format(
                    physical_detector_unit['id'])
                logging.debug(success_msg)

                success_msg = 'phy_det_unit.detector_type_id: {0}'.format(
                    physical_detector_unit['detector_type_id'])
                logging.debug(success_msg)

                success_msg = 'phy_det_unit.karabo_da: {0}'.format(
                    physical_detector_unit['karabo_da'])
                logging.debug(success_msg)
            else:
                error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
                logging.error(error_msg)
                return resp

        else:
            #
            # Get detector_id from detector_identifier
            #
            det_identifier = cal_dict['detector_identifier']
            phy_det_unit_karabo_da = cal_dict['pdu_karabo_da']

            logging.debug('phy_det_unit.physical_name: None')
            logging.debug('detector_identifier: {0}'.format(det_identifier))
            logging.debug(
                'phy_det_unit.karabo_da: {0}'.format(phy_det_unit_karabo_da))

            resp = Detector.get_by_identifier(self, det_identifier)
            if resp['success']:
                detector_id = resp['data']['id']

                success_msg = 'detector_id: {0}'.format(detector_id)
                logging.debug(success_msg)
            else:
                error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
                logging.error(error_msg)
                return resp

            #
            # Get physical_detector_unit_id
            #   from detector_id AND physical_detector_unit.karabo_da
            #
            resp = PhysicalDetectorUnit.get_all_by_detector_and_karabo_da(
                self, detector_id, phy_det_unit_karabo_da)

            if resp['success']:
                physical_detector_unit = resp['data'][0]

                success_msg = 'phy_det_unit.id: {0}'.format(
                    physical_detector_unit['id'])
                logging.debug(success_msg)

                success_msg = 'phy_det_unit.detector_type_id: {0}'.format(
                    physical_detector_unit['detector_type_id'])
                logging.debug(success_msg)

                success_msg = 'phy_det_unit.karabo_da: {0}'.format(
                    physical_detector_unit['karabo_da'])
                logging.debug(success_msg)
            else:
                error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
                logging.error(error_msg)
                return resp

        return physical_detector_unit

    def set_calibration_constant_version(self, calibration_constant_id,
                                         ccv_h, report_id):
        logging.debug('calib_const_id: {0}'.format(calibration_constant_id))
        logging.debug('Calibration Constant Version Dict: {0}'.format(ccv_h))
        logging.debug('report_id: {0}'.format(report_id))

        # Generate unique name if it doesn't exist
        datetime_str = strftime('%Y%m%d_%H%M%S', gmtime())
        cc_name_uk = '{0}_sIdx={1}'.format(datetime_str, ccv_h['start_idx'])
        cc_name = Util.get_opt_hash_val(ccv_h, 'name', cc_name_uk)

        #
        ccv_desc = Util.get_opt_hash_val(ccv_h, 'description')
        ccv_flg_good_quality = Util.val_to_api_bool(ccv_h['flg_good_quality'])
        ccv_flg_deployed = Util.get_opt_hash_val(ccv_h, 'flg_deployed',
                                                 def_val='true')

        physical_detector_unit = self.get_physical_detector_unit(ccv_h)

        cal_ccv = {
            'name': cc_name,
            'file_name': ccv_h['file_name'],
            'path_to_file': ccv_h['path_to_file'],
            'data_set_name': ccv_h['data_set_name'],
            'calibration_constant_id': str(calibration_constant_id),
            'physical_detector_unit_id': str(physical_detector_unit['id']),
            'flg_deployed': ccv_flg_deployed,
            'flg_good_quality': ccv_flg_good_quality,
            'begin_validity_at': ccv_h['begin_validity_at'],
            'end_validity_at': ccv_h['end_validity_at'],
            'begin_at': ccv_h['begin_at'],
            'start_idx': ccv_h['start_idx'],
            'end_idx': ccv_h['end_idx'],
            'raw_data_location': ccv_h['raw_data_location'],
            'report_id': str(report_id),
            'description': ccv_desc
        }
        logging.debug('Built Calibration CCV: {0}'.format(cal_ccv))

        #
        # Create new ccv from dictionary
        #
        return CalibrationConstantVersion.create_from_dict(self, cal_ccv)

    def set_condition_from_dict(self, detector_condition):
        cal_cond = self.get_condition_from_dict(detector_condition)

        return Condition.set_condition_from_dict(self, cal_cond)

    def search_condition_from_dict(self, event_at, detector_condition):
        cal_cond = self.get_condition_from_dict(detector_condition)

        cond = Condition(self,
                         cal_cond['name'],
                         cal_cond['flg_available'],
                         event_at,
                         cal_cond['parameters_conditions_attributes'],
                         cal_cond['description'])

        resp = cond.get_expected()
        if resp['success']:
            return resp
        else:
            resp = cond.get_possible()

            if resp['success']:
                # This method returns several conditions over time
                # ordered by the closest condition creation datetime,
                # compared with the desired event datetime!
                # The closest condition is received in the first position!
                resp['data'] = resp['data'][0]

            return resp

    def search_possible_conditions_from_dict(self,
                                             event_at,
                                             detector_condition):
        cal_cond = self.get_condition_from_dict(detector_condition)

        cond = Condition(self,
                         cal_cond['name'],
                         cal_cond['flg_available'],
                         event_at,
                         cal_cond['parameters_conditions_attributes'],
                         cal_cond['description'])

        resp = cond.get_possible()
        # This method returns several conditions over time
        # ordered by the closest condition creation datetime,
        # compared with the desired event datetime!

        return resp

    def get_condition_from_dict(self, detector_condition):
        parameters_conditions = []

        for param in detector_condition['parameters']:
            param_name = param['parameter_name']
            param_desc = Util.get_opt_hash_val(param, 'description')

            resp = Parameter.get_by_name(self, param_name)
            param_id = resp['data']['id']

            parameter_condition = {
                'parameter_id': str(param_id),
                'value': str(param['value']),
                'lower_deviation_value': str(param['lower_deviation_value']),
                'upper_deviation_value': str(param['upper_deviation_value']),
                'flg_available': Util.val_to_api_bool(param['flg_available']),
                'description': str(param_desc)
            }

            logging.debug('Build parameter_condition hash successfully')
            parameters_conditions.append(parameter_condition)

        def_cond_name = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        condition_name = Util.get_opt_hash_val(detector_condition, 'name',
                                               def_val=def_cond_name)

        condition_flg_avail = Util.get_opt_hash_val(detector_condition,
                                                    'flg_available',
                                                    def_val='true')
        condition_desc = Util.get_opt_hash_val(detector_condition,
                                               'description')

        #
        cal_cond = {
            'name': condition_name,
            'flg_available': condition_flg_avail,
            'description': condition_desc,
            'parameters_conditions_attributes': parameters_conditions
        }
        logging.debug('Build condition successfully: {0}'.format(cal_cond))

        return cal_cond

    def set_report(self, report_h):
        logging.debug('* report_h == {0}'.format(report_h))

        rep_name = report_h['name']
        rep_path = report_h['file_path']
        rep_flg_available = True
        rep_description = Util.get_opt_hash_val(report_h, 'description')

        resp = Report.get_by_name_and_file_path(self, rep_name, rep_path)

        if resp['success']:
            report = resp['data']

            if report != []:
                report_id = report['id']

                success_msg = 'FOUND report_id: {0}'.format(report_id)
                logging.debug(success_msg)

                return resp

        # In case no data found
        report = Report(self, rep_name, rep_path,
                        rep_flg_available, rep_description)

        resp = report.set()

        if resp['success']:
            report = resp['data']
            report_id = report['id']

            success_msg = 'CREATED report_id: {0}'.format(report_id)
            logging.debug(success_msg)

            return resp

        else:
            error_msg = '{0} >> {1}'.format(resp['info'],
                                            resp['app_info'])
            logging.error(error_msg)
            return resp

    def get_all_phy_det_units_from_detector(self, det_retrieve_h):
        logging.debug('* det_retrieve_h == {0}'.format(det_retrieve_h))

        det_identifier = det_retrieve_h['detector_identifier']
        pdu_snapshot_at = Util.get_opt_hash_val(det_retrieve_h, 'pdu_snapshot_at')

        # accepts legacy parameter name (snapshot_at)
        if pdu_snapshot_at == '':
            pdu_snapshot_at = Util.get_opt_hash_val(det_retrieve_h, 'snapshot_at')

        resp = self.get_all_phy_det_units_from_detector_int(det_identifier,
                                                            pdu_snapshot_at)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        return resp

    def get_all_phy_det_units_from_detector_int(self, detector_identifier,
                                                pdu_snapshot_at):
        #
        # Get detector_id from detector_identifier
        #
        logging.debug('* det_identifier == {0}'.format(detector_identifier))
        logging.debug('* pdu_snapshot_at == {0}'.format(pdu_snapshot_at))

        resp = Detector.get_by_identifier(self, detector_identifier)
        if resp['success']:
            detector_id = resp['data']['id']

            success_msg = 'detector_id == {0}'.format(detector_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # get_all_by_detector
        resp = PhysicalDetectorUnit.get_all_by_detector(self, detector_id,
                                                        pdu_snapshot_at)
        if resp['success']:
            all_phy_det_units = resp['data']

            phy_det_unit_id_0 = all_phy_det_units[0]['id']
            detector_type_id_0 = all_phy_det_units[0]['detector_type_id']
            detector_id_0 = all_phy_det_units[0]['detector_id']

            success_msg = 'phy_det_unit_id_0 == {0}'.format(phy_det_unit_id_0)
            logging.debug(success_msg)
            success_msg = 'det_type_id_0 == {0}'.format(detector_type_id_0)
            logging.debug(success_msg)
            success_msg = 'detector_id_0 == {0}'.format(detector_id_0)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        return resp

    def inject_new_calibration_constant_version(self, inject_h):
        logging.debug('Calibration injection hash is: {0}'.format(inject_h))

        # Separate the inject_h into its main elements
        if 'report' in inject_h:
            inj_report_info = inject_h['report']
        else:
            inj_report_info = {}

        inj_detector_condition = inject_h['detector_condition']
        inj_cal_const = inject_h['calibration_constant']
        inj_cal_const_version = inject_h['calibration_constant_version']

        # set_condition
        resp = self.set_condition_from_dict(inj_detector_condition)

        if resp['success']:
            condition = resp['data']
            condition_id = condition['id']

            success_msg = 'condition_id: {0}'.format(condition_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # set_calibration_constant
        resp = self.set_calibration_constant(condition, inj_cal_const)
        if resp['success']:
            report = resp['data']
            cc_id = report['id']

            success_msg = 'condition_id: {0}'.format(cc_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Create Report entity only if received
        report_id = ''

        if inj_report_info != {}:
            resp = self.set_report(inj_report_info)
            if resp['success']:
                report = resp['data']
                report_id = report['id']

                success_msg = 'report_id: {0}'.format(report_id)
                logging.debug(success_msg)
            else:
                error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
                logging.error(error_msg)
                return resp

        # create_calibration_constant_version
        resp = self.set_calibration_constant_version(
            cc_id, inj_cal_const_version, report_id
        )

        if resp['success']:
            cal_calibration_constant_version = resp['data']
            ccv_id = cal_calibration_constant_version['id']

            success_msg = 'condition_id: {0}'.format(ccv_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # In case of success
        return resp

    def retrieve_calibration_constant_version(self, retrieve_h):
        logging.debug('Calibration retrieve hash is: {0}'.format(retrieve_h))

        # Retrieve the desired retrieve Strategy
        # OPTIONS:
        #   - pdu_closest_by_time (default)
        #   - pdu_prior_in_time
        #   - detector_closest_by_time
        if 'strategy' in retrieve_h:
            ret_strategy = retrieve_h['strategy']
        else:
            ret_strategy = 'pdu_closest_by_time'

        # Call proper method depending on the desired 'Strategy'
        if ret_strategy == 'pdu_prior_in_time':
            resp = self.retrieve_calibration_constant_version_by_pdu(
                ret_strategy, retrieve_h)

        elif ret_strategy == 'detector_closest_by_time':
            resp = self.retrieve_calibration_constant_version_by_detector(
                ret_strategy, retrieve_h)

        # if ret_strategy == '' or
        #    ret_strategy is None or
        #    ret_strategy == 'pdu_closest_by_time':
        else:
            resp = self.retrieve_calibration_constant_version_by_pdu(
                ret_strategy, retrieve_h)

        return resp

    def retrieve_calibration_constant_version_by_pdu(self,
                                                     ret_strategy,
                                                     retrieve_h):
        logging.debug('CCV retrieve strategy: {0}'.format(ret_strategy))
        logging.debug('Calibration retrieve hash is: {0}'.format(retrieve_h))

        # Retrieve the desired retrieve Strategy
        # OPTIONS:
        #  - pdu_closest_by_time (default)
        #  - pdu_prior_in_time
        #  - detector_closest_by_time [ERROR! <= Not available in this method!]

        # Separate the inject_h into its main elements
        ret_detector_condition = retrieve_h['detector_condition']

        # Calculate necessary values
        calibration_name = retrieve_h['calibration_name']
        event_at = Util.get_opt_hash_val(retrieve_h, 'measured_at')
        snapshot_at = Util.get_opt_hash_val(retrieve_h, 'snapshot_at')

        # get_condition a valid condition
        resp = self.search_possible_conditions_from_dict(
            event_at, ret_detector_condition
        )

        if resp['success']:
            conditions = resp['data']

            condition_ids = []
            for condition in conditions:
                condition_ids.append(condition['id'])

            success_msg = 'condition_ids: {0}'.format(condition_ids)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Get Calibration ID
        resp = Calibration.get_by_name(self, calibration_name)
        if resp['success']:
            calibration = resp['data']
            calibration_id = calibration['id']

            success_msg = 'condition_id: {0}'.format(calibration_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Get PhysicalDetectorUnit ID and DetectorType ID
        physical_detector_unit = self.get_physical_detector_unit(retrieve_h)

        phy_det_unit_id = physical_detector_unit['id']
        detector_type_id = physical_detector_unit['detector_type_id']

        # Get CalibrationConstant ID
        resp = CalibrationConstant.get_all_by_conditions(self,
                                                         calibration_id,
                                                         detector_type_id,
                                                         condition_ids)
        if resp['success']:
            calibration_constants = resp['data']

            cc_ids = []
            for cc in calibration_constants:
                cc_ids.append(cc['id'])

            success_msg = 'calibration_constant_ids: {0}'.format(cc_ids)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Debug IDs
        logging.debug('* ret_strategy == {0}'.format(ret_strategy))
        logging.debug('* condition_ids == {0}'.format(condition_ids))
        logging.debug('* calibration_id == {0}'.format(calibration_id))
        logging.debug('* phy_det_unit_id == {0}'.format(phy_det_unit_id))
        logging.debug('* detector_type_id == {0}'.format(detector_type_id))
        logging.debug('* calibration_constant_ids == {0}'.format(cc_ids))

        # Get calibration_constant_version
        if ret_strategy == 'pdu_prior_in_time':
            # resp = CalibrationConstantVersion.get_by_uk(self,
            resp = CalibrationConstantVersion.get_prior_in_time(self,
                                                                cc_ids,
                                                                phy_det_unit_id,
                                                                event_at,
                                                                snapshot_at)

        elif ret_strategy == 'detector_closest_by_time':
            error_msg = 'Strategy "detector_closest_by_time" not available ' \
                        'in retrieve_calibration_constant_version'
            logging.error(error_msg)
            return resp

        # if ret_strategy == '' or
        #    ret_strategy is None or
        #    ret_strategy == 'pdu_closest_by_time':
        else:
            resp = CalibrationConstantVersion.get_closest_by_time(
                self,
                cc_ids, phy_det_unit_id,
                event_at, snapshot_at)

        if resp['success']:
            calibration_constant_version = resp['data']
            ccv_id = calibration_constant_version['id']

            success_msg = 'calibration_constant_version_id: {0}'.format(ccv_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # In case of success
        return resp

    def retrieve_calibration_constant_version_by_detector(self,
                                                          ret_strategy,
                                                          retrieve_h):
        logging.debug('CCV retrieve strategy: {0}'.format(ret_strategy))
        logging.debug('Calibration retrieve hash is: {0}'.format(retrieve_h))

        # Retrieve the desired retrieve Strategy
        # OPTIONS:
        #  - pdu_closest_by_time  [ERROR! <= Not available in this method!]
        #  - pdu_prior_in_time [ERROR! <= Not available in this method!]
        #  - detector_closest_by_time (default)

        # Separate the inject_h into its main elements
        ret_detector_condition = retrieve_h['detector_condition']

        # Calculate necessary values
        calibration_name = retrieve_h['calibration_name']
        event_at = Util.get_opt_hash_val(retrieve_h, 'measured_at')
        snapshot_at = Util.get_opt_hash_val(retrieve_h, 'snapshot_at')

        # get_condition a valid condition
        resp = self.search_possible_conditions_from_dict(
            event_at, ret_detector_condition
        )

        if resp['success']:
            conditions = resp['data']

            condition_ids = []
            for condition in conditions:
                condition_ids.append(condition['id'])

            success_msg = 'condition_ids: {0}'.format(condition_ids)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Get Calibration ID
        resp = Calibration.get_by_name(self, calibration_name)
        if resp['success']:
            calibration = resp['data']
            calibration_id = calibration['id']

            success_msg = 'calibration_id: {0}'.format(calibration_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        #
        # Get detector_id from detector_identifier
        #
        det_identifier = retrieve_h['detector_identifier']
        logging.debug('* detector_identifier == {0}'.format(det_identifier))

        resp = self.get_all_phy_det_units_from_detector_int(det_identifier,
                                                            snapshot_at)

        if resp['success']:
            all_phy_det_units = resp['data']

            phy_det_unit_id_0 = all_phy_det_units[0]['id']
            detector_type_id = all_phy_det_units[0]['detector_type_id']
            detector_id = all_phy_det_units[0]['detector_id']

            success_msg = 'all_phy_det_units == {0}'.format(all_phy_det_units)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Get CalibrationConstant ID
        resp = CalibrationConstant.get_all_by_conditions(self,
                                                         calibration_id,
                                                         detector_type_id,
                                                         condition_ids)
        if resp['success']:
            calibration_constants = resp['data']

            cc_ids = []
            for cc in calibration_constants:
                cc_ids.append(cc['id'])

            success_msg = 'calibration_constant_ids: {0}'.format(cc_ids)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Debug IDs
        logging.debug('* ret_strategy == {0}'.format(ret_strategy))
        logging.debug('* condition_ids == {0}'.format(condition_ids))
        logging.debug('* calibration_id == {0}'.format(calibration_id))
        logging.debug('* detector_type_id == {0}'.format(detector_type_id))
        logging.debug('* detector_id == {0}'.format(detector_id))
        logging.debug('* calibration_constant_ids == {0}'.format(cc_ids))
        logging.debug('* phy_det_units == {0}'.format(all_phy_det_units))

        # Get calibration_constant_version
        if ret_strategy == 'pdu_prior_in_time':
            error_msg = 'Strategy "pdu_prior_in_time" not available' \
                        'in retrieve_calibration_constant_version_by_detector'
            logging.error(error_msg)
            return resp

        elif ret_strategy == 'pdu_closest_by_time':
            error_msg = 'Strategy "pdu_closest_by_time" not available in' \
                        ' retrieve_calibration_constant_version_by_detector'
            logging.error(error_msg)
            return resp

        # if ret_strategy == '' or
        #    ret_strategy is None or
        #    ret_strategy == 'detector_closest_by_time':
        else:
            karabo_da = Util.get_opt_hash_val(retrieve_h, 'pdu_karabo_da')
            logging.debug('* karabo_da == {0}'.format(karabo_da))

            resp = CalibrationConstantVersion.get_closest_by_time_by_detector(
                self,
                cc_ids, detector_id, karabo_da,
                event_at, snapshot_at)

        if resp['success']:
            # Override resp['data'] to return an object, instead of an Array
            # as returned by all the other scenarios
            resp['data'] = resp['data'][0]
            calibration_constant_version = resp['data']
            ccv_id = calibration_constant_version['id']

            success_msg = 'calibration_constant_version_id: {0}'.format(ccv_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # In case of success
        return resp

    def retrieve_all_calibration_constant_versions(self, retrieve_h):
        logging.debug('Calibration retrieve hash is: {0}'.format(retrieve_h))

        # Separate the inject_h into its main elements
        ret_detector_condition = retrieve_h['detector_condition']

        # Calculate necessary values
        calibration_name = retrieve_h['calibration_name']
        event_at = Util.get_opt_hash_val(retrieve_h, 'measured_at')
        snapshot_at = Util.get_opt_hash_val(retrieve_h, 'snapshot_at')

        # get_condition a valid condition
        resp = self.search_possible_conditions_from_dict(
            event_at, ret_detector_condition,
        )

        if resp['success']:
            conditions = resp['data']

            condition_ids = []
            for condition in conditions:
                condition_ids.append(condition['id'])

            success_msg = 'condition_ids: {0}'.format(condition_ids)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Get Calibration ID
        resp = Calibration.get_by_name(self, calibration_name)
        if resp['success']:
            calibration = resp['data']
            calibration_id = calibration['id']

            success_msg = 'condition_id: {0}'.format(calibration_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Get PhysicalDetectorUnit ID and DetectorType ID
        physical_detector_unit = self.get_physical_detector_unit(retrieve_h)

        phy_det_unit_id = physical_detector_unit['id']
        detector_type_id = physical_detector_unit['detector_type_id']

        # Get CalibrationConstant ID
        resp = CalibrationConstant.get_all_by_conditions(self,
                                                         calibration_id,
                                                         detector_type_id,
                                                         condition_ids)
        if resp['success']:
            calibration_constants = resp['data']

            cc_ids = []
            for cc in calibration_constants:
                cc_ids.append(cc['id'])

            success_msg = 'calibration_constant_ids: {0}'.format(cc_ids)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Debug IDs
        logging.debug('* condition_ids == {0}'.format(condition_ids))
        logging.debug('* calibration_id == {0}'.format(calibration_id))
        logging.debug('* phy_det_unit_id == {0}'.format(phy_det_unit_id))
        logging.debug('* detector_type_id == {0}'.format(detector_type_id))
        logging.debug('* calibration_constant_ids == {0}'.format(cc_ids))

        # Get all calibration_constant_versions
        resp = CalibrationConstantVersion.get_all_versions(self,
                                                           cc_ids,
                                                           phy_det_unit_id,
                                                           event_at,
                                                           snapshot_at)
        if resp['success']:
            success_msg = 'response successful!'
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # In case of success
        return resp

    def update_calibration_constant_version(self, update_h):
        logging.debug('Calibration update hash is: {0}'.format(update_h))

        # Calculate necessary values
        ccv_id = update_h['ccv_id']

        # Get calibration_constant_version
        resp = CalibrationConstantVersion.get_by_id(self, ccv_id)
        if resp['success']:
            ccv = resp['data']
            success_msg = 'retrieve_constant_version_id: {0}'.format(ccv_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # Update calibration_constant_version
        # set parameters from DB
        ccv_pars = {k: v for k, v in ccv.items() if
                    (not isinstance(v, dict) and k != 'id' and k!= 'created_at')}
        ccv_pars['calibration_constant_id'] = ccv['calibration_constant']['id']
        ccv_pars['physical_detector_unit_id'] = ccv['physical_detector_unit'][
            'id']

        # Update parameters
        updatable = ['description', 'end_idx', 'start_idx', 'begin_at',
                     'end_validity_at', 'begin_validity_at',
                     'flg_good_quality', 'flg_deployed']

        for key in updatable:
            if key in update_h:
                ccv_pars[key] = update_h[key]

        new_ccv = CalibrationConstantVersion(
            calibration_client=self,
            **ccv_pars)

        new_ccv.id = ccv_id
        resp = new_ccv.update()

        if resp['success']:
            success_msg = 'update_constant_version_id: {0}'.format(ccv_id)
            logging.debug(success_msg)
        else:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # In case of success
        return resp
