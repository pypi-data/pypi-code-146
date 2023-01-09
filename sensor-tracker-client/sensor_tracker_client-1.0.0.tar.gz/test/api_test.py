import unittest
from sensor_tracker_client import sensor_tracker_client as stc
from sensor_tracker_client.exceptions import AuthenticationError

replacement_list = ["name"]
MODEL_LIST = ["wave", 'slocum']


def get_current_glider_deployment_from_sensor_tracker():
    data_dict = get_all_glider_deployment_from_sensor_tracker()
    new_dict = []
    for glider_type, item in data_dict.items():
        for x in item:
            if not x["end_time"]:
                new_dict.append(x)
    return new_dict


def nested_object_convert_to_name(the_object):
    for key, value in the_object.items():
        if type(value) is dict:
            for replacement in replacement_list:
                if replacement in value:
                    the_object[key] = value[replacement]
                    break
    return the_object


def get_all_glider_deployment_from_sensor_tracker():
    data_dict = dict()
    for x in MODEL_LIST:
        try:
            data_list = stc.deployment.get({"model": x, "how": "contains", "depth": 1}).dict
        except Exception as e:
            msg = "Sensor Tracker Api error: {}".format(e)

            data_list = []
        replaced_data_list = []
        for data in data_list:
            replaced_data = nested_object_convert_to_name(data)
            replaced_data_list.append(replaced_data)
        data_dict[x] = replaced_data_list
    return data_dict


class TestConnect(unittest.TestCase):
    def setUp(self):
        stc.basic.DEBUG = True
        # stc.basic.DEBUG_HOST = 'http://bugs.ocean.dal.ca/sensor_tracker/'
        # stc.basic.DEBUG_HOST = 'http://prod.ceotr.ca/sensor_tracker/'
        stc.basic.DEBUG_HOST = 'http://127.0.0.1:8000/'
        # stc.basic.HOST_URL = 'http://127.0.0.1:8000/'

    def test_(self):
        res = get_current_glider_deployment_from_sensor_tracker()
        print(res)

    def test_singleton(self):
        from sensor_tracker_client import sensor_tracker_client as sta2
        compare = stc == sta2
        print(compare)

    def test_general_api(self):
        # institution, project, manufacturer

        # institution
        institution_res = stc.institution.get()
        # print(institution_res.dict)
        institution_res2 = stc.institution.get({"name": "OTN"})
        # print(institution_res2.dict)

        # res2.dict or res2.dict()?
        # project
        project_res = stc.project.get()

        project_res2 = stc.project.get({"name": "Gulf of St. Lawrence Animal Tracking for OTN"})

        # manufacturer
        manufacturer_res = stc.manufacturer.get()
        manufacturer_res2 = stc.manufacturer.get({"name": "Teledyne Webb"})
        print("")

    def test_instrument_api(self):
        # instrument,
        instrument_res = stc.instrument.get()
        # "identifier", "short_name", "long_name", "serial", "manufacturer"
        instrument_res2 = stc.instrument.get({"identifier": "c"})
        # get by platform
        instrument_res3 = stc.instrument.get({"platform_name": "otn200"})
        # get by deployment

        # todo :maybe deployment_start_time
        instrument_res4 = stc.instrument.get(
            {"platform_name": "otn200", "deployment_start_time": "2017-08-02 19:37:38"})
        # get by partial time
        instrument_res5 = stc.instrument.get({"platform_name": "otn200", "deployment_start_time": "2017-08-02"})
        # should it raise error when given unexpected argument

        # instrument_res6 = stc.instrument.get(
        #         {"platform_name": "otn200", "deployment_start_time": "2017-08-02", "something": "something"})

    def test_calibration(self):
        calibration = stc.calibration.get()

    def test_calibration_event(self):
        calibration_event = stc.calibration_event.get()

    def test_instrument_on_platform(self):
        # instrument_on_platform
        instrument_on_platform_res = stc.instrument_on_platform.get()
        # get by platform
        #        "identifier", "platform_name"
        instrument_on_platform_res2 = stc.instrument_on_platform.get({"platform_name": "otn200"})
        # Default depth argument
        instrument_on_platform_res3 = stc.instrument_on_platform.get({"platform_name": "otn200", "depth": 1})
        instrument_on_platform_res4 = stc.instrument_on_platform.get({"platform_name": "otn200", "depth": 2})
        # get by instrument identifier
        instrument_on_platform_res5 = stc.instrument_on_platform.get({"identifier": "c", "depth": 1})
        print("")

    def test_sensor(self):
        # sensor
        sensor_res = stc.sensor.get({"output": True})
        # "identifier", "short_name", "long_name",
        sensor_res2 = stc.sensor.get({"identifier": "RMSe", "output": True})
        # get by deployment
        sensor_res3 = stc.sensor.get({"platform_name": "otn200", "deployment_start_time": "2017-08-02 19:37:38"})
        sensor_res4 = stc.sensor.get({"platform_name": "otn200"})
        sensor_res5 = stc.sensor.get(
            {"platform_name": "otn200", "deployment_start_time": "2017-08-02", "output": 'all'})

        print("")

    def test_sensor_on_instrument(self):
        ret = stc.sensor_on_instrument.get(
            {"platform_name": "otn200", "deployment_start_time": "2017-08-02 19:37:38", "depth": 1})
        print()

    def test_platform_type(self):
        # platform_type

        platform_type_res = stc.platform_type.get()
        # model
        platform_type_res2 = stc.platform_type.get({"model": "Mooring"})
        platform_type_res3 = stc.platform_type.get({"model": "slocum", "how": "contains"})
        platform_type_res4 = stc.platform_type.get({"model": "slocum"})
        print("")

    def test_platform(self):
        # platform

        # cache_on default as False
        stc.cache_on = True

        platform_res = stc.platform.get()
        platform_res1_2 = stc.platform.get()
        compare1 = platform_res == platform_res1_2
        # "platform_name", "serial_name"
        platform_res2 = stc.platform.get({"platform_name": "otn200"})
        platform_res2_2 = stc.platform.get({"platform_name": "otn200"})
        compare2 = platform_res2 == platform_res2_2

        # model, how
        platform_res3 = stc.platform.get({"model": "slocum", "how": "contains"})
        platform_res3_2 = stc.platform.get({"how": "contains", "model": "slocum"})
        compare3 = platform_res3 == platform_res3_2
        print("")

    def test_power(self):
        power_res = stc.power.get()
        print("")

    def test_deployment(self):
        # deployment
        # "wmo_id", "platform_name", "institution_name", "project_name", "testing_mission", "start_time", "deployment_number"
        deployment_res = stc.deployment.get({"platform_name": "otn200"})
        deployment_res2 = stc.deployment.get({"model": "Slocum Glider G\d", "how": "regex"})
        # "how": "match"(default) "contains", "regex"
        deployment_res3 = stc.deployment.get({"model": "Slocum", "how": "contains"})
        print("")

    def test_deployment_comment(self):
        # deployment_comment
        # user detail hidden
        deployment_comment = stc.deployment_comment.get(
            {"platform_name": "dal556", "depth": 1})
        deployment_comment_res2 = stc.deployment_comment.get(
            {"platform_name": "dal556", "depth": 0})
        print("")

    def test_platform_hierarchy(self):
        hierarchy_res1 = stc.deployment_hierarchy.get(
            {"platform_name": "we04", "deployment_start_time": "2015-07-28 12:46:13-03"})
        hierarchy_res2 = stc.deployment_hierarchy.get(
            {"platform_name": "HYP", "deployment_start_time": "2018-11-21 09:45:31-04"})
        print("")

    def test_deployment_comment2(self):
        # deployment_comment
        # user detail hidden
        deployment_comment = stc.deployment_comment.get(
            {"platform_name": "dal556", "depth": 1})
        deployment_comment_res2 = stc.deployment_comment.get(
            {"platform_name": "dal556", "depth": 0})

    # def test_post_functions(self):
    #     try:
    #         example1 = stc.project.post({"name": "some_project"})
    #     except AuthenticationError as e:
    #         print(1)
    #         print(e)
    #
    #     stc.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"

    # or

    # sta.authentication.username = ""
    # sta.authentication.password = ""
    # try:
    #     example2 = stc.project.post({"name": "some_project"})
    # except AuthenticationError as e:
    #     print(2)
    #     print(e)
    # stc.authentication.token = "some_token"
    # try:
    #     example3 = stc.project.post({"name": "some_project"})
    # except AuthenticationError as e:
    #     print(3)
    #     print(e)
    # print("")

    def test_get_sensor_by_pk(self):
        # haven't finish those yet
        ret = stc.sensor.get(1)

    def test_patch_to_change_instrument_on_platform(self):
        stc.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"

        res = stc.instrument_on_platform.patch(13, {"comment": "api changeed sdfsdfsd"})
        print(res)

    def test_exceptions(self):
        ...

    def test_token(self):
        stc.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"
        print(stc.authentication.token)

    def test_get_object_by_obj_pk(self):
        institution_res = stc.institution.get(1)
        print(institution_res.dict)
        sensor_res = stc.sensor.get(2)
        print(sensor_res.dict)

    def test_pk(self):
        print(stc.institution.get(1).dict)
        print(stc.project.get(1).dict)
        print(stc.manufacturer.get(1).dict)
        print(stc.instrument_on_platform.get(1).dict)
        print(stc.sensor.get(1).dict)
        print(stc.sensor_on_instrument.get(1).dict)
        print(stc.platform_type.get(1).dict)
        print(stc.power.get(1).dict)
        print(stc.deployment.get(1).dict)
        print(stc.deployment_comment.get(1).dict)
