from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from gql.transport.exceptions import TransportQueryError

    from vectice.api.http_error import HttpError

BAD_OR_MISSING_CREDENTIALS_ERROR_MESSAGE = "Bad or missing credentials"


class InvalidReferenceError(ValueError):
    """
    When an incorrect value type is passed at the client level.
    """

    def __init__(self, reference_type: str, value: Any) -> None:
        super().__init__(
            f"The {reference_type} reference is invalid. Please check the provided value. "
            + "it should be a string or a number. "
            + f"Provided value is {value} ({type(value)})"
        )


class MissingReferenceError(ValueError):
    """
    When a value is missing at the client level.
    """

    def __init__(self, reference_type: str, parent_reference_type: str | None = None) -> None:
        if parent_reference_type is not None:
            super().__init__(f"The {parent_reference_type} reference is required if the {reference_type} name is given")
        else:
            super().__init__(f"The {reference_type} reference is required")


class ClientErrorHandler:
    def _graphql_error_formatter(self, error: TransportQueryError):
        exception = error.errors[0]["extensions"]["exception"]  # type: ignore
        if "stacktrace" in exception:
            # try to format the message
            message = exception["stacktrace"]
            message = message[0].split(":")
            error_code = message[0]
            error_message = message[1]
            raise VecticeException(f"{error_code}: {error_message}")
        # just dump the stringified error
        raise VecticeException(repr(exception))

    def handle_code(self, e: HttpError, reference_type: str, reference: str | int):
        if e.code == 404:
            return BadReferenceFactory.get_reference(reference_type, reference)
        elif e.code == 401:
            raise ConnectionRefusedError(BAD_OR_MISSING_CREDENTIALS_ERROR_MESSAGE)
        elif e.code == 403:
            raise PermissionError(f"Missing rights to access this {reference_type}")
        else:
            raise RuntimeError(f"Can not access {reference_type}: {e.reason}")

    def handle_get_http_error(self, e: HttpError, reference_type: str, reference: str | int):
        return self.handle_code(e, reference_type, reference)

    def handle_put_http_error(self, e: HttpError, reference_type: str, reference: str | int):
        return self.handle_code(e, reference_type, reference)

    def handle_delete_http_error(self, e: HttpError, reference_type: str, reference: str | int):
        return self.handle_code(e, reference_type, reference)

    def handle_post_http_error(self, e: HttpError, reference_type: str, action: str = "create"):
        if e.code == 401:
            raise ConnectionRefusedError(BAD_OR_MISSING_CREDENTIALS_ERROR_MESSAGE)
        elif e.code == 403:
            raise PermissionError(f"Missing rights to access this {reference_type}")
        elif e.code == 400:
            raise RuntimeError(f"Can not {action} {reference_type}: {e.reason}")
        else:
            raise RuntimeError(f"Unexpected error: {e.reason}")

    def handle_post_gql_error(self, error: TransportQueryError, reference_type: str, reference: str | int):
        status_code = error.errors[0]["extensions"]["exception"]["status"]  # type: ignore[index]
        if status_code == 404:
            return BadReferenceFactory.get_reference(reference_type, reference)
        elif status_code == 401:
            raise ConnectionRefusedError(BAD_OR_MISSING_CREDENTIALS_ERROR_MESSAGE)
        elif status_code == 403:
            raise PermissionError(f"Missing rights to access this {reference_type}")
        elif status_code == 400:
            # backend always adds a "message" to the response
            message = error.errors[0]["message"]  # type: ignore
            raise VecticeException(f"{reference_type}: {message}")
        else:
            return self._graphql_error_formatter(error)


class BadReferenceFactory:
    """
    Raises the appropriate Error
    """

    @classmethod
    def get_reference(cls, reference_type: str, value: str | int):
        """
        :param reference_type:
        :param value:
        """
        if reference_type == "workspace":
            if isinstance(value, str):
                raise WorkspaceNameError(value)
            elif isinstance(value, int):
                raise WorkspaceIdError(value)
        elif reference_type == "project":
            if isinstance(value, str):
                raise ProjectNameError(value)
            elif isinstance(value, int):
                raise ProjectIdError(value)
        elif reference_type == "phase":
            if isinstance(value, str):
                raise PhaseNameError(value)
            elif isinstance(value, int):
                raise PhaseIdError(value)
        elif reference_type == "step":
            if isinstance(value, str):
                raise StepNameError(value)
            elif isinstance(value, int):
                raise StepIdError(value)
        elif reference_type == "iteration":
            if isinstance(value, int):
                raise IterationIdError(value)
            elif isinstance(value, str):
                raise IterationNameError(value)
        elif reference_type == "iteration_index":
            if isinstance(value, int):
                raise IterationIndexError(value)
        elif reference_type == "steps":
            raise NoStepsInPhaseError(value)
        else:
            raise RuntimeError(f"The value {value} of type {reference_type} is not valid!")


class VecticeException(Exception):
    def __init__(self, value):
        super().__init__(value)
        self.__suppress_context__ = True
        self.value = value


class VecticeBaseNameError(NameError):
    def __init__(self, value):
        super().__init__(value)
        self.__suppress_context__ = True
        self.value = value

    def __str__(self):
        divider = "=" * len(f"{self.__class__.__name__}: {self.value}")
        return f"\n{divider}\n{self.__class__.__name__}: {self.value}"


class WorkspaceNameError(VecticeBaseNameError):
    def __init__(self, value: str):
        super().__init__(f"The workspace with name '{value}' is unknown.")


class WorkspaceIdError(VecticeBaseNameError):
    def __init__(self, value: int):
        super().__init__(f"The workspace with id '{value}' is unknown.")


class ProjectNameError(VecticeBaseNameError):
    def __init__(self, value: str):
        super().__init__(f"The project with name '{value}' is unknown.")


class ProjectIdError(VecticeBaseNameError):
    def __init__(self, value: int):
        super().__init__(f"The project with id '{value}' is unknown.")


class PhaseNameError(VecticeBaseNameError):
    def __init__(self, value: str):
        super().__init__(f"The phase with name '{value}' is unknown.")


class PhaseIdError(VecticeBaseNameError):
    def __init__(self, value: int):
        super().__init__(f"The phase with id '{value}' is unknown.")


class StepNameError(VecticeBaseNameError):
    def __init__(self, value: str):
        super().__init__(f"The step with name '{value}' is unknown.")


class StepIdError(VecticeBaseNameError):
    def __init__(self, value: int):
        super().__init__(f"The step with id '{value}' is unknown.")


class IterationIdError(VecticeBaseNameError):
    def __init__(self, value: int):
        super().__init__(f"The iteration with id '{value}' is unknown.")


class IterationIndexError(VecticeBaseNameError):
    def __init__(self, value: int):
        super().__init__(f"The iteration with index '{value}' is unknown.")


class IterationNameError(VecticeBaseNameError):
    def __init__(self, value: str):
        super().__init__(f"The iteration with name '{value}' is unknown.")


class NoStepsInPhaseError(VecticeBaseNameError):
    def __init__(self, value: str | int):
        ref = f"with id '{value}'" if isinstance(value, int) else f"'{value}'"
        super().__init__(f"There are no steps in the phase {ref}.")
