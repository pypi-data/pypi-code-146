"""Contains definitions of exceptions from TT API"""
from typing import TYPE_CHECKING, Dict
import logging

if TYPE_CHECKING:
    from trustedtwin.models.responses import TTResponse

logger = logging.getLogger("trustedtwin")

ERR_MSG_TEMPLATE = 'Error occurred for API operation: ' \
                   '"{api_operation}", sub code: "{sub_code}", reason: "{desc}", trace: "{trace}".'


class TTAPIResponseException(Exception):
    """TT API Exception response wrapper"""

    def __init__(self, response: "TTResponse", api_operation: str):
        """Override default behavior"""
        msg = ERR_MSG_TEMPLATE.format(
            api_operation=api_operation,
            sub_code=response.body.get("subcode"),
            desc=response.body.get("description", "").strip("."),
            trace=response.body.get("trace", "")
        )
        super().__init__(msg)

        self.response = response.body
        self.subcode = response.body.get("subcode", "")
        self.description = response.body.get("description", "")
        self.trace = response.body.get("trace", "")
        self.api_operation = api_operation
        self.http_code = response.http_code


class TTInternalError(
    TTAPIResponseException
):  # pylint: disable=missing-class-docstring
    pass


class TTUnauthorizedError(
    TTAPIResponseException
):  # pylint: disable=missing-class-docstring
    pass


class TTRequestError(TTAPIResponseException):  # pylint: disable=missing-class-docstring
    pass


class TTResponseTimeout(
    TTAPIResponseException
):  # pylint: disable=missing-class-docstring
    pass


class TTResourceNotFound(
    TTAPIResponseException
):  # pylint: disable=missing-class-docstring
    pass


class TTForbiddenError(
    TTAPIResponseException
):  # pylint: disable=missing-class-docstring
    pass


class TTProcessingError(
    TTAPIResponseException
):  # pylint: disable=missing-class-docstring
    pass


class TTClientException(Exception):  # pylint: disable=missing-class-docstring
    pass


def get_tt_exception(
    response: "TTResponse", api_operation: str
) -> TTAPIResponseException:
    """Raise TT exception based on returned SubCode"""
    try:
        sub_code = response.body["subcode"]
    except Exception as err:
        logger.error('Could not process response body = [%s]', response.body)
        raise TTClientException() from err

    sub_code_to_exception: Dict = {
        500000: TTInternalError,
        500001: TTInternalError,
        401000: TTUnauthorizedError,
        400314: TTRequestError,
        400141: TTRequestError,
        400415: TTRequestError,
        500159: TTResponseTimeout,
        400592: TTRequestError,
        404653: TTResourceNotFound,
        403535: TTForbiddenError,
        400358: TTRequestError,
        400589: TTRequestError,
        400897: TTRequestError,
        400979: TTRequestError,
        500314: TTProcessingError,
    }
    exc = sub_code_to_exception[sub_code]
    return exc(response, api_operation)
