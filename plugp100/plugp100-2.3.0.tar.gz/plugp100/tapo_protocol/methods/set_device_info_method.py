from . import taporequest


class SetDeviceInfoMethod(taporequest.TapoRequest):
    def __init__(self, params):
        super().__init__("set_device_info", params)
