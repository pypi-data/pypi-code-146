"""
MIT License

Copyright (c) 2019 NinjaSnail1080
Copyright (c) 2022 - 2023 avizum

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import Any, NoReturn


from .exceptions import (
    ConnectionFailure,
    TimedOut,
    NoMoreQuestions,
    ServerDown,
    TechnicalServerError,
)


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()


def raise_connection_error(response: str) -> NoReturn:
    """Raise the proper error if the API failed to connect"""
    if response == "KO - SERVER DOWN":
        raise ServerDown("Akinator's servers are down in this region. Try again later or use a different language")

    elif response == "KO - TECHNICAL ERROR":
        raise TechnicalServerError(
            "Akinator's servers have had a technical error. Try again later or use a different language"
        )

    elif response == "KO - TIMEOUT":
        raise TimedOut("Your Akinator session has timed out")
    elif response in {"KO - ELEM LIST IS EMPTY", "WARN - NO QUESTION"}:
        raise NoMoreQuestions('"Akinator.step" reached 79. No more questions.')
    else:
        raise ConnectionFailure(f"An unknown error has occured. Server response: {response}")
