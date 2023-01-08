# Copyright (C) 2021,2022,2023 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Parse source text file into tokens."""

import argparse
import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, Dict, List

from txt2ebook import log_or_raise_on_warning

logger = logging.getLogger(__name__)


@dataclass
class Token:
    """Token class to store metadata of token."""

    type: str = field(repr=True)
    value: Any = field(repr=False)
    line_no: int = field(repr=True, default=0)

    def __repr__(self) -> str:
        """Return the string representation of Tokenizer for debugging purpose.

        Returns:
          str: Debugging string for logging
        """
        # pylint: disable=bad-option-value,consider-using-f-string
        return "{}(type='{}', line_no='{}', value='{}')".format(
            self.__class__.__name__, self.type, self.line_no, self.value[0:10]
        )


@dataclass
class Tokenizer:
    """Tokenizer class to parse text content."""

    raw_content: str = field(repr=False)
    config: argparse.Namespace = field(repr=False)
    tokens: List[Token] = field(default_factory=List, repr=False)
    lineno_lookup: Dict = field(default_factory=Dict, repr=False)

    def __init__(self, raw_content: str, config: argparse.Namespace) -> None:
        """Set the constructor for the Tokenizer."""
        self.raw_content = raw_content
        self.config = config

        config_lang = config.language.replace("-", "_")
        self.langconf = import_module(f"txt2ebook.languages.{config_lang}")

        lookupcontent = raw_content[:]
        lineno_lookup = {}
        for lineno, line in enumerate(lookupcontent.splitlines(), start=1):
            lineno_lookup[line[:10]] = lineno
        self.lineno_lookup = lineno_lookup

        self.tokens = self.parse()

    def __getattr__(self, key: str) -> Any:
        """Get a value of the config based on key name.

        Args:
            key(str): The key attribute name of the config, language config,
            and current class.

        Returns:
            Any: The value of a key, if found. Otherwise raise AttributeError
            exception.
        """
        if key in ["tokens", "lineno_lookup"]:
            return getattr(self, key)

        if hasattr(self.config, key):
            return getattr(self.config, key)

        if hasattr(self.langconf, key):
            return getattr(self.langconf, key)

        raise AttributeError(f"invalid config key: '{key}'!")

    def __repr__(self) -> str:
        """Return the string representation of Tokenizer for debugging purpose.

        Returns:
          str: Debugging string for logging
        """
        # pylint: disable=bad-option-value,consider-using-f-string
        return "{}(raw_content='{}', stats='{}')".format(
            self.__class__.__name__, self.raw_content[:5], self.stats()
        )

    def parse(self) -> List:
        """Parse the content into tokens.

        Returns:
          List: The list of tokens.
        """
        # Remove the trailing separator at end of file.
        separator = self.paragraph_separator.encode("utf-8").decode(
            "unicode_escape"
        )
        content = self.raw_content.rstrip(separator)

        lines = content.split(separator)

        if len(lines) <= 1:
            msg = (
                f"Cannot split content by {repr(self.paragraph_separator)}. "
                "Check if content have newline with spaces."
            )
            log_or_raise_on_warning(msg, self.config.raise_on_warning)

        tokens: List[Token] = []
        for line in lines:
            self._tokenize_line(line, tokens)

        return tokens

    def stats(self) -> Counter:
        """Returns the statistics count for the parsed tokens.

        Returns:
          Counter: Counting statistic of parsed tokens.
        """
        stats = Counter(token.type for token in self.tokens)
        logger.debug("Token stats: %s", repr(stats))
        return stats

    def _tokenize_line(self, line: str, tokens: List) -> None:
        """Tokenize each line after we split by paragraph separator."""
        _ = (
            self._tokenize_header(line, tokens)
            or self._tokenize_metadata(line, tokens)
            or self._tokenize_paragraph(line, tokens)
        )

    def _tokenize_metadata(self, line: str, tokens: List) -> bool:
        """Tokenize the metadata of the book.

        Metadata at the top of the file was grouped and separate as single
        newline. By default, the content, or paragraph was separated by two
        newlines. Hence, we have to group it into one token.

        Also, we can split the metadata line as these lines can also contains
        chapter content, which can also contains newlines.
        """
        re_title = f"^{self.DEFAULT_RE_TITLE}"
        if self.config.re_title:
            re_title = self.config.re_title[0]

        re_author = f"\n{self.DEFAULT_RE_AUTHOR}"
        if self.config.re_author:
            re_author = self.config.re_author[0]

        token_type_regex_map = [
            ("TITLE", re_title),
            ("AUTHOR", re_author),
            ("TAG", f"\n{self.DEFAULT_RE_TAG}"),
        ]

        token = None
        for token_type, regex in token_type_regex_map:
            match = re.search(regex, line)
            if match:
                token_value = match.group(1).strip()
                token = Token(
                    token_type, token_value, self._lineno(token_value)
                )
                tokens.append(token)

        return bool(token)

    def _tokenize_header(self, line: str, tokens: List) -> bool:
        """Tokenize section headers.

        Note that we parse in such sequence: chapter, volume, volume_chapter to
        prevent unnecessary calls as we've more chapters than volumes.
        """
        return (
            self._tokenize_chapter(line, tokens)
            or self._tokenize_volume_chapter(line, tokens)
            or self._tokenize_volume(line, tokens)
        )

    def _tokenize_volume_chapter(self, line: str, tokens: List) -> bool:
        line = self._validate_section_header("volume chapter", line)
        token = None

        re_volume_chapter = (
            rf"^{self.DEFAULT_RE_VOLUME}\s*{self.DEFAULT_RE_CHAPTER}"
        )
        if self.config.re_volume_chapter:
            re_volume_chapter = self.config.re_volume_chapter[0]

        match = re.search(re_volume_chapter, line)
        if match:
            volume = match.group(1).strip()
            chapter = match.group(2).strip()
            token = Token(
                "VOLUME_CHAPTER",
                [
                    Token("VOLUME", volume, self._lineno(volume)),
                    Token("CHAPTER", chapter, self._lineno(chapter)),
                ],
            )
            tokens.append(token)

        return bool(token)

    def _tokenize_volume(self, line: str, tokens: List) -> bool:
        line = self._validate_section_header("volume", line)
        token = None

        re_volume = rf"^{self.DEFAULT_RE_VOLUME}$"
        if self.config.re_volume:
            re_volume = "(" + "|".join(self.config.re_volume) + ")"

        match = re.search(re_volume, line)
        if match:
            volume = match.group(1).strip()
            token = Token("VOLUME", volume, self._lineno(volume))
            tokens.append(token)

        return bool(token)

    def _tokenize_chapter(self, line: str, tokens: List) -> bool:
        line = self._validate_section_header("chapter", line)
        token = None

        re_chapter = rf"^{self.DEFAULT_RE_CHAPTER}$"
        if self.config.re_chapter:
            re_chapter = "(" + "|".join(self.config.re_chapter) + ")"

        match = re.search(re_chapter, line)
        if match:
            chapter = match.group(1).strip()
            token = Token("CHAPTER", chapter, self._lineno(chapter))
            tokens.append(token)

        return bool(token)

    def _tokenize_paragraph(self, line: str, tokens: List) -> bool:
        tokens.append(Token("PARAGRAPH", line, self._lineno(line)))
        return True

    def _validate_section_header(self, header_type: str, line: str) -> str:
        if line.startswith("\n"):
            log_or_raise_on_warning(
                f"Found newline before {header_type} header: {repr(line)}",
                self.config.raise_on_warning,
            )
            line = line.lstrip("\n")
        return line

    def _lineno(self, text: str) -> int:
        """Find the line no of the string within the file or raw content."""
        return self.lineno_lookup.get(text[:10], 0)
