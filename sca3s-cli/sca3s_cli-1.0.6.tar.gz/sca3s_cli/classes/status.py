from enum import IntEnum


class Status(IntEnum):
    """
    Class to define status codes for use with the OKException class.
    """

    @staticmethod
    def dict(status: IntEnum, data=None) -> dict:
        if data is None:
            return {
                'status': status
            }
        data['status'] = status
        return data

    # Global Success Code
    SUCCESS = 0

    # Config File Codes
    CONFIG_NOT_FOUND = 1000
    ENVIRONMENT_NOT_FOUND = 1001
    CONFIG_PARSE_ERROR = 1002
