from . import taporequest


class GetDeviceInfoMethod(taporequest.TapoRequest):
    def __init__(self, params):
        super().__init__("get_device_info", params)
