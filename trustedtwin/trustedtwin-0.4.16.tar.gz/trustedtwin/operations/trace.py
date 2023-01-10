"""Definition of trace operation"""
from typing import TYPE_CHECKING, Dict

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


def trace(service: "RestService") -> Dict:
    """Execute trace API operation"""
    endpoint = "trace"

    resp = service.http_client.execute_request(
        method=RESTMethod.POST,
        url_root=service.http_client.host_name,
        endpoint=endpoint,
    )

    return process_response(resp, "trace", **service.kwargs)
