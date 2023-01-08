#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

"""Miscellaneous helper functions."""
from typing import Any, Dict, List, Union

from modalic.config import Conf


def all_equal_list(iterator: List[Any]) -> bool:
    r"""Checks list if all elements are equal.

    :param iterator: Input list object.
    :returns: The consistent element if all elements in the list are equal otherwise None.
    """
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    if all(first == x for x in iterator):
        return first
    else:
        return None


def validate_kwargs(
    kwargs: Dict[Any, Any],
    allowed_kwargs: Dict[str, str],
    error_message="Keyword argument not understood:",
) -> None:
    r"""Checks that all keyword arguments are in the set of allowed keys.

    :param kwargs: Keyword arguments to be checked.
    :param allowed_kwargs: Keyword arguments that should pass.
    """
    for kwarg in kwargs:
        if kwarg not in allowed_kwargs:
            raise TypeError(error_message, kwarg)


def validate_config(conf: Union[dict, Conf]) -> None:
    r"""Checks if Conf object is a valid type."""
    if not isinstance(conf, dict) or not isinstance(conf, Conf):
        raise TypeError(f"Type of Conf `{type(conf)}` is not valid.")
