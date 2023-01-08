class ApiBase:
    def __init__(self, deeper) -> None:
        self.deeper = deeper
        self.refUrl = self.deeper.hostIp
