from . import taporequest

class SetLightingMethod(taporequest.TapoRequest):
    def __init__(self, params):
        super().__init__("set_lighting_effect", params)