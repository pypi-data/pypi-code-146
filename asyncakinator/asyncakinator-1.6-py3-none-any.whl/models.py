"""
MIT License

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

import enum
import dataclasses
from .exceptions import InvalidAnswer, InvalidLanguage, InvalidTheme
from typing import TypedDict


__all__ = (
    "Answer",
    "Language",
    "Theme",
    "Guess",
)


class Answer(enum.Enum):
    """
    Represents the answer to a question.
    """

    YES = 0
    NO = 1
    I_DONT_KNOW = 2
    PROBABLY = 3
    PROBABLY_NOT = 4
    BACK = 5

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"<Answer answer={self.name}>"

    @classmethod
    def from_str(cls, answer: str) -> Answer:
        """
        Allows for the creation of an Answer from a string.


        Parameters
        ----------
        answer: :class:`str`
            The answer to convert to :class:`Answer`.

            For :attr:`Answer.YES`, the following are valid:
                ``yes``, ``y``, and ``0``.
            For :attr:`Answer.NO`, the following are valid:
                ``no``, ``n``, and ``1``.
            For :attr:`Answer.I_DONT_KNOW`, the following are valid:
                ``i dont know``, ``i don't know``, ``idk``, and ``2``.
            For :attr:`Answer.PROBABLY`, the following are valid:
                ``probably``, ``p``, and ``3``.
            For :attr:`Answer.PROBABLY_NOT`, the following are valid:
                ``probably not``, ``pn``, and ``4``.
            For :attr:`Answer.BACK`, the following are valid:
                ``back``, ``b``, and ``5``.

        Raises
        ------
        :exc:`InvalidAnswer`
            The answer you provided is not valid.

        Returns
        -------
        :class:`Answer`
        """

        answer = answer.lower()
        if answer in {"yes", "y", "0"}:
            return cls.YES
        elif answer in {"no", "n", "1"}:
            return cls.NO
        elif answer in {"i", "idk", "i dont know", "i don't know", "2"}:
            return cls.I_DONT_KNOW
        elif answer in {"probably", "p", "3"}:
            return cls.PROBABLY
        elif answer in {"probably not", "pn", "4"}:
            return cls.PROBABLY_NOT
        elif answer in {"back", "b", "5"}:
            return cls.BACK
        else:
            raise InvalidAnswer(f"Invalid answer: {answer}")


class Language(enum.Enum):
    """
    Represents the language of the game.
    """

    ENGLISH = "en"
    ARABIC = "ar"
    CHINESE = "cn"
    GERMAN = "de"
    SPANISH = "es"
    FRENCH = "fr"
    HEBREW = "il"
    ITALIAN = "it"
    JAPANESE = "jp"
    KOREAN = "kr"
    DUTCH = "nl"
    POLISH = "pl"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    TURKISH = "tr"
    INDONESIAN = "id"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"<Language language={self.value}>"

    @classmethod
    def from_str(cls, language: str) -> Language:
        """
        Create a :class:`Language` from a string.

        The short form of a language (``en`` for English, ``fr`` for French, etc.) is also accepted.

        Parameters
        ----------
        language: :class:`str`
            The language to convert to :class:`Language`.

        Raises
        ------
        :exc:`InvalidLanguage`
            The language you provided is not valid.

        Returns
        -------
        :class:`Language`
        """
        language = language.lower()
        if language in {"english", "en"}:
            return cls.ENGLISH
        elif language in {"arabic", "ar"}:
            return cls.ARABIC
        elif language in {"chinese", "cn"}:
            return cls.CHINESE
        elif language in {"german", "de"}:
            return cls.GERMAN
        elif language in {"spanish", "es"}:
            return cls.SPANISH
        elif language in {"french", "fr"}:
            return cls.FRENCH
        elif language in {"hebrew", "il"}:
            return cls.HEBREW
        elif language in {"italian", "it"}:
            return cls.ITALIAN
        elif language in {"japanese", "jp"}:
            return cls.JAPANESE
        elif language in {"korean", "kr"}:
            return cls.KOREAN
        elif language in {"dutch", "nl"}:
            return cls.DUTCH
        elif language in {"polish", "pl"}:
            return cls.POLISH
        elif language in {"portuguese", "pt"}:
            return cls.PORTUGUESE
        elif language in {"russian", "ru"}:
            return cls.RUSSIAN
        elif language in {"turkish", "tr"}:
            return cls.TURKISH
        elif language in {"indonesian", "id"}:
            return cls.INDONESIAN
        else:
            raise InvalidLanguage(f"Invalid language: {language}")


class Theme(enum.Enum):
    """
    Determines what server to use when starting a game.
    """

    CHARACTERS = 1
    OBJECTS = 2
    ANIMALS = 14

    @classmethod
    def from_str(cls, theme: str) -> Theme:
        """
        Create a :class:`Theme` from a string.

        Parameters
        ----------
        theme: :class:`str`
            The theme to convert to :class:`Theme`.

            For :attr:`Theme.CHARACTERS`, the following are valid:
                ``characters``, ``ch``, and ``c``.
            For :attr:`Theme.OBJECTS`, the following are valid:
                ``objects``, ``obj``, and ``o``.
            For :attr:`Theme.ANIMALS`, the following are valid:
                ``animals``, and ``a``.

        Raises
        ------
        :exc:`InvalidTheme`
            The theme you provided is not valid.

        Returns
        -------
        :class:`Theme`
        """
        theme = theme.lower()
        if theme in {"characters", "ch", "c"}:
            return cls.CHARACTERS
        elif theme in {"objects", "obj", "o"}:
            return cls.OBJECTS
        elif theme in {"animals", "a"}:
            return cls.ANIMALS
        else:
            raise InvalidTheme(f"Invalid theme: {theme}")


class _GuessDict(TypedDict):
    id: int
    name: str
    id_base: int
    proba: float
    description: str
    valide_contrainte: int
    ranking: int
    pseudo: str
    picture_path: str
    corrupt: int
    relative: int
    award_id: int
    flag_photo: int
    absolute_picture_path: str


@dataclasses.dataclass
class Guess:
    """
    Class representing a guess.

    Attributes
    ----------
    id: :class:`int`
        The ID of the guess.
    name: :class:`str`
        The name of the guess.
    probablility: :class:`float`
        The probability that the guess is correct.
    description: :class:`str`
        The description of the guess.
    ranking: :class:`int`
        The ranking of the guess.
    absolute_picture_path: :class:`str`
        A URL to the picture of the guess.
    """

    id: int
    name: str
    probablility: float
    description: str
    ranking: int
    absolute_picture_path: str
    _data: _GuessDict | None

    @classmethod
    def _from_dict(cls, data: _GuessDict) -> Guess:
        return cls(
            data["id"],
            data["name"],
            data["proba"],
            data["description"],
            data["ranking"],
            data["absolute_picture_path"],
            data,
        )
