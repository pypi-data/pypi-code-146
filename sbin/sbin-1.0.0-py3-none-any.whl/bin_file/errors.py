class BinFileNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class BinFileParsingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
