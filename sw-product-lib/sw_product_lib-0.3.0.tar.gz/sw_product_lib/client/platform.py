"""platform.py."""
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib import parse

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError

from sw_product_lib.client.auth import get_authenticator
from sw_product_lib.client.transport import StrangeworksTransport
from sw_product_lib.errors.error import StrangeworksError


ALLOWED_HEADERS = {""}


class Operation:
    """Object for definining requests made to the platform."""

    def __init__(
        self,
        query: str,
        allowed_vars: Optional[List[str]] = None,
        upload_files: bool = False,
    ) -> None:
        """Initialize object.

        Accepts a GraphQL query or mutation as a string. Derives variable names used by
        the query if none were provided.

        Parameters
        ----------
        query: str
            a GraphQL query or mutation as string.
        allowed_vars: Optional[List[str]]
            list to override which variables can be sent was part of query.
        """
        self.query = gql(query)
        self.allowed_vars = (
            allowed_vars
            if allowed_vars
            else list(
                map(
                    lambda x: x.variable.name.value,
                    self.query.definitions[0].variable_definitions,
                )
            )
        )
        self.upload_files = upload_files

    def variables(
        self, values: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Define which variables are available for this operation."""
        if not self.allowed_vars:
            return values

        vars = {}
        for k, v in values.items():
            if k in self.allowed_vars and v is not None:
                vars[k] = v
        return vars


class APIName(Enum):
    """Helper class/enum for identifying available API's from the platform."""

    SDK = "sdk"
    PLATFORM = "platform"
    PRODUCT = "products"


class API:
    """Client for Platform API."""

    def __init__(
        self,
        base_url: str,
        api_id: APIName,
        api_key: Optional[str] = None,
        auth_token: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retries: int = 0,
    ) -> None:
        """Initialize platform API client.

        Provides access to the platform API methods which allows python SDK clients to
        interact with the Strangeworks platform.

        Parameters
        ----------
        base_url: str
            The URL to send the GQL queries.
        api_key: Optional[str]
            Used to obtain and refresh authorization tokens.
        id : APIName
            Identifies which of the platform APIs to use.
        auth_token: Optional[str]
            jwt token used to authorize requests to the platform APIs.
        headers: Dict[str, str]
            Additional values to set in the header for the request. The header must
            belong to ALLOWED_HEADERS.
        """
        url = parse.urljoin(base_url, api_id.value)
        self.gql_client = Client(
            transport=StrangeworksTransport(
                url=url,
                api_key=api_key,
                authenticator=get_authenticator(url),
                auth_token=auth_token,
                headers=headers,
                retries=retries,
                timeout=timeout,
            )
        )

    def execute(self, op: Operation, **kvargs):
        """Execute an operation on the platform.

        Parameters
        ----------
        op: Operation
            which request to run
        variable_values; Optional[Dict[str, Any]]
            values to send with the request
        """
        try:
            result = self.gql_client.execute(
                document=op.query,
                variable_values=op.variables(kvargs),
                upload_files=op.upload_files,
            )
            return result
        except TransportQueryError as e:
            print(f"error during query: {e}")
            raise StrangeworksError.server_error(str(e.errors[0]), e.query_id)
