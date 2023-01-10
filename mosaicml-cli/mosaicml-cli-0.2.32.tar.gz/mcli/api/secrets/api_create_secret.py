"""create_secrets SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import Optional, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_singular_mapi_request
from mcli.models.mcli_secret import Secret

__all__ = ['create_secret']

QUERY_FUNCTION = 'createSecret'
VARIABLE_DATA_NAME = 'createSecretData'
QUERY = f"""
mutation CreateSecret(${VARIABLE_DATA_NAME}: CreateSecretInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
        name
        type
        metadata
        createdAt
    }}
}}"""


@overload
def create_secret(
    secret: Secret,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> Secret:
    ...


@overload
def create_secret(
    secret: Secret,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[Secret]:
    ...


def create_secret(
    secret: Secret,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Create a secret in the MosaicML Cloud

    Arguments:
        secret (:class:`~mcli.models.mcli_secret.Secret`): A
            :class:`~mcli.models.mcli_secret.Secret` object to create
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`create_secret` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.mcli_secret.Secret` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    variables = {
        VARIABLE_DATA_NAME: secret.mapi_data,
    }
    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Secret,
        variables=variables,
    )
    if not future:
        return response.result(timeout=timeout)
    else:
        return response
