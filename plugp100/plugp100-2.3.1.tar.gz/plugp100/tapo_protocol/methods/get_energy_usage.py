from . import taporequest


class GetEnergyUsageMethod(taporequest.TapoRequest):
    def __init__(self, params):
        super().__init__("get_energy_usage", params)
