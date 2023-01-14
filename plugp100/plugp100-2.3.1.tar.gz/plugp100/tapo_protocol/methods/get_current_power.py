from . import taporequest


class GetCurrentPowerMethod(taporequest.TapoRequest):
    def __init__(self, params):
        super().__init__("get_current_power", params)
