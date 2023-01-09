import unittest
from sensor_tracker_client import sensor_tracker_client as sta

from sensor_tracker_client.authentication import authentication


class TestConnect(unittest.TestCase):

    def setUp(self):
        sta.basic.RAISE_REQUEST_ERROR = False
        sta.basic.DEBUG = True

    def test_successful_GET_request(self):
        sta.cache_on = False
        res = sta.sensor.get({"depth": 1, "something": 3})
        res2 = sta.deployment.get({"model": "wave", "how": "contains"})
        print()
        # print(sta.__dict__)
        # sta.deployment = 's'
        # print(sta.deployment.a)

        # if res:
        #     print(res.content)

    def test_authentication(self):
        sta.authentication.username = "xling"
        sta.authentication.password = "123321qweewq"

        print(authentication.get_post_header())

    def test_post(self):
        a = sta
        # sta.authentication.username="xling"
        # sta.authentication.password = "123321qweewq"
        sta.authentication.token = "1537ded79296862c889ffe368b9decc3b9c2afe1"
        res = sta.institution.post({
            "name": "fsdvf",
            "url": "vdfvdf",
            "street": "vdfvd",
            "city": "vdfdf",
            "province": "vervs",
            "postal_code": "verfvdvsvs",
            "country": "vervsf",
            "contact_name": "vervsf",
            "contact_phone": "verfvs",
            "contact_email": "veer"
        })
        print(res)

    def test_cache(self):
        sta.cache_on = True
        res2 = sta.deployment.get({"model": "wave", "how": "contains"})
        print(res2)
        res3 = sta.deployment.get({"model": "wave", "how": "contains"})
        print(res3)
        res4 = sta.deployment.get({"how": "contains", "model": "wave"})
        print(res2 is res3 and res2 is res4)

    def test_get_large_data(self):
        sta.cache_on = True
        res2 = sta.sensor.get({"identifier": "c_fin"})
        res3 = sta.sensor.get({"identifier": "c_fin", "depth": 0})
        print(res2 is res3)
        print(res2.dict == res3.dict)

    def test_data_factory(self):
        sta.cache_on = True
        ret = sta.sensor.get()
        print(ret.dict)

    def test_get_sensor(self):
        res = sta.sensor.get({"identifier": "Motor on Tme"})
        print(res.dict)

    def test_get_instrument_by_platform_name_start_time(self):
        dep_obj = sta.instrument.get({"platform_name": "cabot", "start_time": "2019-05-26 13:59:48"})
        print(dep_obj.dict)

    def test_get_deployment_by_different_time_format(self):
        dep_obj = sta.deployment.get({"platform_name": "cabot", "start_time": "2019-05-26 13:59:48"})
        print(dep_obj.dict)
        dep_obj = sta.deployment.get({"platform_name": "cabot", "start_time": "2019-05-26"})
        print(dep_obj.dict)

    def test_get_sensor_by_platform_name_start_time(self):
        ...
