from http import HTTPStatus
from typing import Optional


class ApiException(Exception):
    def __init__(
        self,
        request,
        message: str,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        to_sentry: Optional[bool] = True,
        previous: Exception = None
    ):
        super().__init__(message)

        self._request = request
        self._status_code = status_code
        self._message = message
        self._previous = previous

        try:
            import sentry_sdk
        except ImportError:
            print("No sentry module found.")
        else:
            if to_sentry:
                with sentry_sdk.push_scope() as scope:
                    for key, value in self.__dict__.items():
                        scope.set_extra(key, value)
                    sentry_sdk.capture_exception(self)

    @property
    def request(self):
        return self._request

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def previous(self) -> Exception:
        return self._previous

    @property
    def payload(self) -> dict:
        result = {
            'message': self.message,
            'code': self.status_code
        }

        return result
