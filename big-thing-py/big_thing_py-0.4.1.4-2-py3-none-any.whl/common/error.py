class NotSupportError(Exception):  # 사용자 정의 에러
    def __init__(self, msg: str = ''):
        self.msg = msg

    def __str__(self):
        return 'This feature is not support yet...\n' + self.msg


class SoPTypeError(Exception):  # 사용자 정의 에러
    def __init__(self, msg: str = ''):
        self.msg = msg

    def __str__(self):
        return 'Only SoPType type is available.\n' + self.msg


class ManagerModeError(Exception):
    def __init__(self, msg: str = '') -> None:
        self.msg = msg

    def __str__(self):
        return 'Only SoPManagerMode type is available.\n' + self.msg
