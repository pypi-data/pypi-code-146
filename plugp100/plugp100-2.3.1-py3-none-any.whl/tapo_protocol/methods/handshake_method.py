from . import taporequest


class HandshakeMethod(taporequest.TapoRequest):
    def __init__(self, params):
        super().__init__("handshake", params)
