from loguru import logger


class MonitorException(Exception):
    def __init__(self, message: str):
        self.message = message.capitalize()
        logger.error(f"error raised: {message}")


class MissingParameter(MonitorException):
    def __init__(self, message: str):
        super().__init__(message)
