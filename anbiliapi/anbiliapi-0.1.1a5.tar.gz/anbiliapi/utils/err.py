class ApiBaseException(Exception):
    """
    API 基类异常。
    """

    def __init__(self, msg: str = "出现了错误，但是未说明具体原因。"):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class ArgsException(ApiBaseException):
    """
    参数错误。
    """

    def __init__(self, msg: str):
        """
        Args:
            msg (str):   错误消息。
        """
        super().__init__(msg)
        self.msg = msg


class NetworkException(ApiBaseException):
    """
    网络错误。
    """

    def __init__(self, status: int, msg: str):
        """
        Args:
            status (int):   状态码。
            msg (str):      状态消息。
        """
        super().__init__(msg)
        self.status = status
        self.msg = f"网络错误，状态码：{status} - {msg}。"

    def __str__(self):
        return self.msg


class ResponseCodeException(ApiBaseException):
    """
    API 返回 code 错误。
    """

    def __init__(self, code: int, msg: str, raw: dict = None):
        """
        Args:
            code (int):             错误代码。
            msg (str):              错误信息。
            raw (dict, optional):   原始响应数据. Defaults to None.
        """
        super().__init__(msg)
        self.msg = msg
        self.code = code
        self.raw = raw

    def __str__(self):
        return f"接口返回错误代码：{self.code}，信息：{self.msg}。\n{self.raw}"


class ResponseException(ApiBaseException):
    """
    API 响应异常。
    """

    def __init__(self, msg: str):
        """
        Args:
            msg (str): 错误消息。
        """
        super().__init__(msg)
        self.msg = msg
