from bin.process.io.io import Io


class MuteIo(Io):
    def text(self, message: str) -> None:
        pass

    def title(self, message: str) -> None:
        pass

    def success(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass

    def warning(self, message: str) -> None:
        pass
