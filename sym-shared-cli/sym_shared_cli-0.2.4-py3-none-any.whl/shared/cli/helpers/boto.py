import re
from functools import wraps

from botocore.exceptions import ClientError, ConnectionError, ProfileNotFound

from sym.shared.cli.errors import (
    BotoError,
    CliError,
    ErrorPatterns,
    OfflineError,
    raise_if_match,
)

UnauthorizedError = re.compile(r"UnauthorizedOperation")


def make_intercept_boto_errors(matches: ErrorPatterns):
    def intercept_boto_errors(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ConnectionError as err:
                raise OfflineError() from err
            except ClientError as err:
                if UnauthorizedError.search(str(err)):
                    raise BotoError(
                        err,
                        f"Does your user role have permission to {err.operation_name}?",
                    )

                raise_if_match(matches, str(err))

                raise CliError(str(err)) from err
            except ProfileNotFound as err:
                raise BotoError(
                    err,
                    "AWS profile specified could not be found. "
                    "Please check your `AWS_PROFILE` environment variable and "
                    "your credentials file (default: $HOME/.aws/credentials).",
                )

        return wrapped

    return intercept_boto_errors
