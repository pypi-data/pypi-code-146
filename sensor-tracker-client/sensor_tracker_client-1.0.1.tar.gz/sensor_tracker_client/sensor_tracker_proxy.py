# more customize tool for CEOTR group
import logging
from .sensor_tracker_client import SensorTrackerClient

stc = SensorTrackerClient()

replacement_list = ["name"]
logger = logging.getLogger(__name__)


def nested_object_convert_to_name(the_object):
    for key, value in the_object.items():
        if type(value) is dict:
            for replacement in replacement_list:
                if replacement in value:
                    the_object[key] = value[replacement]
                    break
    return the_object


class SensorTrackerClientProxy:
    SLOCUM = "slocum"
    WAVE = "wave"
    SETTING = None

    def __init__(self, sensor_t_c, host=None):
        self.host = host
        self.stc = sensor_t_c
        if host:
            self.stc.HOST = self.host

    @property
    def HOST(self):
        return self.stc.basic.HOST

    def get_api(self, model, parameter):
        try:
            api_data = getattr(stc, model).get(parameter).dict
            return api_data
        except Exception as e:
            msg = "Sensor Tracker Api error: {}".format(e)
            logger.error(msg)
            return []

    def _get_deployment_by_type(self, platform_type, current=False):
        parameter = {"model": platform_type, "how": "contains", "depth": 1}
        data_dict = self.get_api("deployment", parameter)
        replaced_data_list = []
        for x in data_dict:
            replaced_data = nested_object_convert_to_name(x)
            if replaced_data["start_time"] and (not current or replaced_data["et_utc"]):
                replaced_data_list.append(replaced_data)
        return replaced_data_list

    def get_wave_deployment(self, current=False):
        return self._get_deployment_by_type("wave", current)

    def get_slocum_deployment(self, current=False):
        return self._get_deployment_by_type("slocum", current)

    def get_glider_deployment(self, current=False):
        return {"slocum": self.get_slocum_deployment(current), "wave": self.get_wave_deployment(current)}
