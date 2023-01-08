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

import json
import re
import time
from typing import Any

import aiohttp

from .exceptions import CanNotGoBack, NotStarted
from .utils import MISSING, raise_connection_error
from .models import Answer, Language, Theme, Guess


NEW_SESSION_URL = "https://{}/new_session?callback=jQuery331023608747682107778_{}&urlApiWs={}&partner=1&childMod={}&player=website-desktop&uid_ext_session={}&frontaddr={}&constraint=ETAT<>'AV'&soft_constraint={}&question_filter={}"
ANSWER_URL = "https://{}/answer_api?callback=jQuery331023608747682107778_{}&urlApiWs={}&childMod={}&session={}&signature={}&step={}&answer={}&frontaddr={}&question_filter={}"
BACK_URL = "{}/cancel_answer?callback=jQuery331023608747682107778_{}&childMod={}&session={}&signature={}&step={}&answer=-1&question_filter={}"
WIN_URL = "{}/list?callback=jQuery331023608747682107778_{}&childMod={}&session={}&signature={}&step={}"


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.92 Chrome/81.0.4044.92 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


class Akinator:
    """
    A class that represents an async Akinator game.

    .. note::

        Some attributes will be missing before a game has started.
        Use :func:`Akinator.start` a game before accessing these attributes.
        Some attributes will be missing until a game has ended.
        Use :func:`Akinator.win` to end a game before accessing these attributes.

    Parameters
    ----------
    language: :class:`Language`
        The language to use when starting the game. If left blank, defaults to :attr:`Language.ENGLISH`.
    theme: :class:`Theme`
        The theme to use when starting the game. If left blank, defaults to :attr:`Theme.CHARACTERS`.
    child_mode: :class:`bool`
        Whether to use child mode or not. Defaults to False.

    Attributes
    ----------
    question: :class:`str`
        The question that Akinator is asking.
    progression: :class:`float`
        How far in the game you are.
    step: :class:`int`
        The question you are on, starting from 0.
    first_guess: :class:`Guess`
        A dictionary containing the first guess information.
    guesses: list[:class:`Guess`]
        A list of :class:`Guess` dictionary of guesses from greatest to least probability.

    uri: :class:`str`
        The uri that is being used.
    server: :class:`str`
        The server that is being used.
    signature: :class:`int`
        An :class:`int` that represents a game's signature.
    uid: :class:`str`
        Represents a games Unique ID, used for authentication purposes.
    frontaddr: :class:`str`
        An IP address in Base64, used for authentication purposes.
    timestamp: :class:`int`
        A POSIX timestamp that is set when :meth:`Akinator.start` is called
    session: :class:`int`
        Represents a game's session.

    Raises
    ------
    :exc:`TypeError`
        The session is not an :class:`aiohttp.ClientSession`.
    """

    def __init__(
        self,
        language: Language = Language.ENGLISH,
        theme: Theme = Theme.CHARACTERS,
        child_mode: bool = False,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        if session is not None and not isinstance(session, aiohttp.ClientSession):
            raise TypeError("session must be a aiohttp.ClientSession")

        self.language: Language = language
        self.theme: Theme = theme
        self.child_mode: bool = child_mode
        self._session: aiohttp.ClientSession = MISSING
        self._started: bool = False

        self.question: str = MISSING
        self.progression: float = 0.0
        self.step: int = 0

        self.first_guess: Guess = MISSING
        self.guesses: list[Guess] = MISSING

        self.uri: str = MISSING
        self.server: str = MISSING
        self.signature: int = MISSING
        self.uid: str = MISSING
        self.frontaddr: str = MISSING
        self.question_filter: str = MISSING
        self.timestamp: float = 0.0
        self.session: int = 0


    async def _create_session(self) -> None:
        self._session = aiohttp.ClientSession()
        self._session.headers.update(HEADERS)

    def _update(self, resp: Any) -> None:
        """Update class variables"""

        if not self._started:
            self.session = int(resp["parameters"]["identification"]["session"])
            self.signature = int(resp["parameters"]["identification"]["signature"])
            self.question = str(resp["parameters"]["step_information"]["question"])
            self.progression = float(resp["parameters"]["step_information"]["progression"])
            self.step = int(resp["parameters"]["step_information"]["step"])
        else:
            self.question = str(resp["parameters"]["question"])
            self.progression = float(resp["parameters"]["progression"])
            self.step = int(resp["parameters"]["step"])

    def _parse_response(self, response: Any) -> Any:
        """Parse the JSON response and turn it into a Python object"""

        return json.loads(",".join(response.split("(")[1::])[:-1])

    async def _get_session_info(self) -> None:
        """Get uid and frontaddr from akinator.com/game"""

        info_regex = re.compile("var uid_ext_session = '(.*)'\\;\\n.*var frontaddr = '(.*)'\\;")

        async with self._session.get("https://en.akinator.com/game") as w:
            match = info_regex.search(await w.text())
            if not match:
                return

        self.uid, self.frontaddr = match.groups()[0], match.groups()[1]

    async def _auto_get_region(self, language: Language, theme: Theme) -> dict[str, str]:
        """Automatically get the uri and server from akinator.com for the specified language and theme"""

        server_regex = re.compile(
            '[{"translated_theme_name":"[\s\S]*","urlWs":"https:\\\/\\\/srv[0-9]+\.akinator\.com:[0-9]+\\\/ws","subject_id":"[0-9]+"}]'
        )

        uri = f"{language}.akinator.com"
        default_return = {"uri": uri, "server": MISSING}
        async with self._session.get(f"https://{uri}") as w:
            match = server_regex.search(await w.text())
            if match is None:
                return default_return
        parsed = json.loads(match.group().split("'arrUrlThemesToPlay', ")[-1])
        server = MISSING
        server = next((i for i in parsed if i["subject_id"] == str(theme.value)), MISSING)["urlWs"]

        if server not in ["https://srv12.akinator.com:9398/ws"]:
            return {"uri": uri, "server": server}
        return default_return

    async def start(
        self,
        language: Language | None = None,
        theme: Theme | None = None,
        child_mode: bool | None = None,
    ) -> str:
        """
        Starts a new game. This should be called before any other method.


        Parameters
        ----------
        language: :class:`Language` | :class:`None`
            The language to use when starting the game. If :class:`None`, the language specified in the constructor will be used.
        theme: :class:`Theme` | :class:`None`
            The theme to use when starting the game. If :class:`None`, the theme specified in the constructor will be used.
        child_mode: :class:`bool`
            Whether or not to use child mode. If True, the game will be more "child-friendly". If :class:`None`, the child mode specified in the constructor will be used.

        Returns
        -------
        :class:`str`
            The first question that Akinator is asking.
        """
        if self._session is MISSING:
            await self._create_session()

        if language is not None:
            self.language = language
        if theme is not None:
            self.theme = theme
        if child_mode is not None:
            self.child_mode = child_mode

        self.timestamp = time.time()

        region_info = await self._auto_get_region(self.language, self.theme)
        self.uri, self.server = region_info["uri"], region_info["server"]

        soft_constraint = "ETAT%3D%27EN%27" if self.child_mode else ""
        self.question_filter = "cat%3D1" if self.child_mode else ""
        await self._get_session_info()

        async with self._session.get(
            NEW_SESSION_URL.format(
                self.uri,
                self.timestamp,
                self.server,
                str(self.child_mode).lower(),
                self.uid,
                self.frontaddr,
                soft_constraint,
                self.question_filter,
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._started = True
            self._update(resp)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def answer(self, answer: Answer) -> str:
        """
        Answers the current question accessed with :attr:`Akinator.question`, and returns the next question.

        Parameter
        ---------
        answer: :class:`Answer`
            The answer to the current question.

            .. note::

                Calling this method with :attr:`Answer.BACK` will call :meth:`Akinator.back` for you.

        Raises
        ------
        :exc:`NoMoreQuestions`
            There are no more questions to be asked. Call :meth:`Akinator.win` to get the results.
        :exc:`CanNotGoBack`
            The Akinator game is on the first question, so it can't go back anymore.
        :exc:`NotStarted`
            Occurs when you try to answer a question before starting the game.

        Returns
        -------
        :class:`str`
            The next question that Akinator asks.
        """

        if self._started is False:
            raise NotStarted("Game has not started!")

        if answer == Answer.BACK:
            return await self.back()

        async with self._session.get(
            ANSWER_URL.format(
                self.uri,
                self.timestamp,
                self.server,
                str(self.child_mode).lower(),
                self.session,
                self.signature,
                self.step,
                str(answer.value),
                self.frontaddr,
                self.question_filter,
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def back(self) -> str:
        """
        Go back to the previous question.

        .. note::

            :meth:`Akinator.answer` will call this method for you if you pass in :attr:`Answer.BACK`.
            It is recommended that you use that for better experience.

        Raises
        ------
        :exc:`CanNotGoBack`
            The Akinator game is on the first question, so it can't go back anymore.
        :exc:`NotStarted`
            Occurs when you try to answer a question before starting the game.

        Returns
        -------
        :class:`str`
            The previous question that Akinator asked.
        """

        if self._started is False:
            raise NotStarted("Game has not started!")

        if self.step == 0:
            raise CanNotGoBack("You were on the first question and couldn't go back any further")

        async with self._session.get(
            BACK_URL.format(
                self.server,
                self.timestamp,
                str(self.child_mode).lower(),
                self.session,
                self.signature,
                self.step,
                self.question_filter,
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def win(self) -> Guess:
        """
        Get Akinator's current guesses based on the responses to the questions thus far.

        This function will set:

        :attr:`Akinator.first_guess`
            The first guess that is returned
        :attr:`Akinator.guesses`
            A list of guesses from greatest to lowest probablity

        .. note::

            It is recommended that you call this function when `Akinator.progression` is above 85.0,
            because by then, Akinator will most likely narrowed the guesses down to one.

        Raises
        ------
        :exc:`NotStarted`
            Occurs when you try to answer a question before starting the game.

        Returns
        -------
        :class:`Guess`
            The first guess that Akinator has. Also set in :attr:`Akinator.first_guess`.
        """

        if self._started is False:
            raise NotStarted("Game has not started!")

        async with self._session.get(
            WIN_URL.format(
                self.server,
                self.timestamp,
                str(self.child_mode).lower(),
                self.session,
                self.signature,
                self.step,
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self.first_guess = Guess._from_dict(resp["parameters"]["elements"][0]["element"])
            self.guesses = [Guess._from_dict(x["element"]) for x in resp["parameters"]["elements"]]
            return self.first_guess
        else:
            return raise_connection_error(resp["completion"])

    async def end(self) -> Guess:
        """
        Alias to :meth:`Akinator.win`.
        """
        return await self.win()

    async def close(self) -> None:
        """
        Closes the aiohttp ClientSession.

        .. caution::

            If you specified your own ClientSession, this may interrupt what you are doing with the session.
        """
        if self._session is not MISSING and self._session.closed is False:
            await self._session.close()

        self._session = MISSING
        self._started = False
