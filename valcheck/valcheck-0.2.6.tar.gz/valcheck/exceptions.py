from typing import Any, Dict


class MissingFieldException(Exception):
    """Exception to be raised when a field is missing"""
    pass


class ValidationException(Exception):
    """Exception to be raised when data validation fails"""

    def __init__(self, *, error_info: Any) -> None:
        self._error_info = error_info

    @property
    def error_info(self) -> Any:
        return self._error_info

    @error_info.setter
    def error_info(self, value: Any) -> None:
        self._error_info = value

    def as_dict(self) -> Dict[str, Any]:
        return {
            "error_info": self.error_info,
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.as_dict()})"

