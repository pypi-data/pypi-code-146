import logging
from typing import Optional

import grpc

# This list may expand but the important constraints are that it does not
# contain __SEPARATION_CHARACTER__ and that it doesn't allow for url trickery
# when sending id's to RBAC.
#
# For __SEPARATION_CHARACTER__ - we combine two or more id's with no logic for
# escaping which guarantees the combination is unique if and only if we exclude
# __SEPARATION_CHARACTER__. Otherwise we can get into the situation where a project
# named P* containing a model M is mapped to id P**M and a project named P
# containing a model *M is mapped to P**M.
valid_name_chars = set(
    [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b',
        'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
        '4', '5', '6', '7', '8', '9', '_', '-', ' '
    ]
)

allowed_characters_description = "A-Z, a-z, 0-9, _, -, ' '"


def ensure_valid_identifier(
    to_check: str,
    context,
    ignore_empty: bool = False,
    logger: Optional[logging.Logger] = None,
    raise_value_error: bool = False
):
    """Ensures identifier is valid for consumption by artifact repo.

    Args:
        to_check: identifier to check.
        context: context to set errors.
        ignore_empty: whether to allow for empty strings.
        logger: logger.
        raise_value_error: whether to instead of setting context, just throw a ValueError.
    """
    if to_check or (not ignore_empty):
        for c in to_check:
            if not c in valid_name_chars:
                error_msg = f"Identifier '{to_check}' contained an illegal character: '{c}'. Allowed characters are: {allowed_characters_description}"
                if logger is not None:
                    logger.warning(error_msg)
                if raise_value_error:
                    raise ValueError(error_msg)
                else:
                    context.abort(grpc.StatusCode.INVALID_ARGUMENT, error_msg)
