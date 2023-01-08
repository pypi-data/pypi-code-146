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


class InputError(ValueError):
    """Raised when the user inputs an invalid answer"""

    pass


class InvalidAnswer(InputError):
    """Raised when the user inputs an invalid answer"""

    pass


class InvalidLanguage(InputError):
    """Raised when the user inputs an invalid language"""

    pass


class InvalidTheme(InputError):
    """Raised when the user inputs an invalid theme"""

    pass


class ConnectionFailure(Exception):
    """Raised if the Akinator API fails to connect for some reason."""

    pass


class TimedOut(ConnectionFailure):
    """Raised if the Akinator session times out"""

    pass


class NoMoreQuestions(ConnectionFailure):
    """Raised if the Akinator API runs out of questions to ask. This will happen if "Akinator.step" is at 79"""

    pass


class ServerDown(ConnectionFailure):
    """Raised if Akinator's servers are down for the region you're running on."""

    pass


class TechnicalServerError(ConnectionFailure):
    """Raised if Akinator's servers had a technical error."""

    pass


class NotStarted(Exception):
    """Raised when the user tries to do something before starting the game."""

    pass


class CanNotGoBack(Exception):
    """Raised when the user is on the first question and tries to go back further."""

    pass
