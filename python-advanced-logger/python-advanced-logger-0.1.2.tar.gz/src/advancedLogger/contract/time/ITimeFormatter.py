class ITimeFormatter:

    def get(self) -> str:
        raise NotImplemented

    def convert(self, time: float) -> str:
        raise NotImplemented
