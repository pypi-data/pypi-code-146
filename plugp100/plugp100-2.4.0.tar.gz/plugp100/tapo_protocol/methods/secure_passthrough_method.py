from . import taporequest


class SecurePassthroughMethod(taporequest.TapoRequest):
    def __init__(self, params):
        super().__init__("securePassthrough", {"request": params})
