from typing import TYPE_CHECKING, Dict, List, Optional, Union

import click
from sym.shared.cli.errors import CliError, CliErrorWithHint

from sym.flow.cli.helpers.constants import SYM_SUPPORT_EMAIL

if TYPE_CHECKING:
    # Importing here due to circular dependencies
    from sym.flow.cli.models.service_type import ServiceType


class UnexpectedError(CliError):
    def __init__(self, ex: str) -> None:
        super().__init__(f"An unexpected error occurred: {ex}")


class SSLConnectionError(CliError):
    def __init__(self, ex: str) -> None:
        super().__init__(
            f"{ex}. This is usually caused by network monitoring/limiting software on the local computer. Try disabling it. If the issue persists, please contact {SYM_SUPPORT_EMAIL}."
        )


class LoginError(CliError):
    def __init__(self, response_body) -> None:
        super().__init__(f"Error logging in: {response_body}")


class UnknownOrgError(CliError):
    def __init__(self, org_id: str) -> None:
        super().__init__(f"Unknown organization with ID: {org_id}")


class UnknownUserError(CliError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Unknown user for email: {email}")


class UnknownBotError(CliError):
    def __init__(self, username: str) -> None:
        super().__init__(f"Unknown bot: {username}")


class UserAlreadyExists(CliError):
    def __init__(self, email: str) -> None:
        super().__init__(f"A user already exists with email: {email}")


class BotAlreadyExists(CliError):
    def __init__(self, username: str) -> None:
        super().__init__(f"A bot already exists with username: {username}")


class InvalidTokenError(CliError):
    def __init__(self, raw_token) -> None:
        super().__init__(f"Unable to parse token: {raw_token}")


class NotLoggedInError(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You must be logged in to perform this action.",
            "Run `symflow login` to log in.",
        )


class InvalidExternalIdError(CliErrorWithHint):
    def __init__(self, service_type: "ServiceType", external_id: str) -> None:
        error_message = click.style(
            f"The external ID '{external_id}' is invalid for service type '{service_type.type_name}'",
            fg="red",
        )

        super().__init__(
            error_message,
            service_type.help_str,
        )


class MissingServiceError(CliErrorWithHint):
    def __init__(self, service_type: str) -> None:
        error_message = click.style(
            f"No service is registered for type {service_type}",
            fg="red",
        )

        super().__init__(
            error_message,
            f"You can create the service with `symflow services create --service-type {service_type}`",
        )


class MissingIdentityValueError(CliErrorWithHint):
    def __init__(self, identifier: str, command: str = "users") -> None:
        error_message = click.style(
            f"Identity value cannot be empty",
            fg="red",
        )

        super().__init__(
            error_message,
            f"If you want to delete the identity, run `symflow {command} delete-identity {identifier}`",
        )


class InvalidChoiceError(CliErrorWithHint):
    def __init__(self, value: str, valid_choices: List[str]) -> None:
        error_message = click.style(
            f"Invalid input: '{value}'",
            fg="red",
        )

        super().__init__(
            error_message,
            f"Try one of: {', '.join(valid_choices)}",
        )


class MissingChoicesError(CliError):
    def __init__(self) -> None:
        error_message = click.style(
            f"No choices were provided!",
            fg="red",
        )

        super().__init__(error_message)


class ReferencedObjectError(CliError):
    def __init__(self, references: Dict[str, List[str]]) -> None:
        counts = " and ".join(f"{len(refs)} {name}" for name, refs in references.items())

        error_message = click.style(
            f"Cannot perform delete because it is referenced by {counts}",
            fg="red",
        )

        super().__init__(error_message)


class InvalidExpiryError(CliErrorWithHint):
    def __init__(self, expiry: str) -> None:
        error_message = click.style(
            f"Invalid expiry input: {expiry}",
            fg="red",
        )

        super().__init__(
            error_message,
            f"Accepted values are a non-zero integer followed by s, m, d, or mo. e.g. 3d",
        )


class NonEmptyDirectoryError(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "The current directory is not empty! `symflow init` can only be run in an empty directory.",
            "Run `ls -a` to see all the files in this directory",
        )


class SymIdentityNotFound(CliError):
    def __init__(self, id: str) -> None:
        super().__init__(f"No Sym Identity found for user id {id}")


class SymAPIError(CliErrorWithHint):
    """Base exception for all API errors."""


class SymAPIUnauthorizedError(SymAPIError):
    def __init__(self, error_message: str) -> None:
        super().__init__(message="You are not authorized to perform this action.", hints=error_message)


class SymAPIRequestError(SymAPIError):
    def __init__(self, message: str, request_id: str) -> None:
        super().__init__(
            "An API error occurred!",
            message
            + click.style(
                f"\n\nPlease contact support and include your Request ID ({request_id}).\nhttps://docs.symops.com/docs/support",
                fg="white",
                bold=True,
            ),
        )


class SymAPIAggregateError(SymAPIRequestError):
    def __init__(self, errors: Union[str, List[str]], request_id: str) -> None:
        self.errors = errors if isinstance(errors, list) else [errors]
        message = "\n\n".join([error for error in self.errors])
        super().__init__(message, request_id)


class SymAPIMissingEntityError(SymAPIRequestError):
    error_codes = [404]

    def __init__(self, response_code: int, request_id: str) -> None:
        super().__init__(f"Missing entity ({response_code}).", request_id)


class SymAPIUnknownError(SymAPIRequestError):
    """Errors returned by the Sym API that we do not know how to handle."""

    def __init__(self, response_code: int, request_id: str, message: Optional[str] = None) -> None:
        if message:
            super().__init__(f"An unexpected error occurred ({response_code}): {message}", request_id)
        else:
            super().__init__(f"An unknown error with status code {response_code}.", request_id)
