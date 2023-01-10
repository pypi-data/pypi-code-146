class ApiException(Exception):
    # message, status code
    def __init__(self, message: str, status_code: int):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"IntelliProve Api Exception: {self.message} with status code {self.status_code}."


class ApiNotFoundException(ApiException):
    def __init__(self):
        super().__init__("Not found", 404)


class ApiForbiddenException(ApiException):
    def __init__(self):
        super().__init__("Forbidden", 403)


class ApiErrorException(ApiException):
    def __init__(self, status_code: int = 500):
        super().__init__("Server error", status_code)


class ApiResultNotAvailable(ApiException):
    def __init__(self, uuid: str):
        super().__init__(f"Results for video with uuid {uuid} not available yet", 204)
        self.uuid = uuid
