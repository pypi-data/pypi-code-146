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

"""Parse source text file into a book model."""

import argparse
import logging
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, List, Tuple, Union
from unicodedata import numeric

import cjkwrap
import regex as re

from txt2ebook.models import Book, Chapter, Volume
from txt2ebook.tokenizer import Tokenizer

logger = logging.getLogger(__name__)

# Unicode integer in hexadecimal for these characters.
FULLWIDTH_EXCLAMATION_MARK = 0xFF01
EXCLAMATION_MARK = 0x21
TILDE = 0x7E

# Mapping table for halfwidth ASCII characters to its fullwidth equivalent.
#
# Fullwidth is a text character that occupies two alphanumeric characters
# in monospace font.
#
# See Halfwidth and Fullwidth Forms in Unicode (https://w.wiki/66Ps) and
# Unicode block (https://w.wiki/66Pt).
HALFWIDTH_FULLWIDTH_MAP = {}
for i, j in enumerate(range(EXCLAMATION_MARK, TILDE + 1)):
    HALFWIDTH_FULLWIDTH_MAP[j] = FULLWIDTH_EXCLAMATION_MARK + i


@dataclass
class Parser:
    """Parser class to massage and parse a text content."""

    raw_content: str = field()
    config: argparse.Namespace = field()

    def __init__(self, raw_content: str, config: argparse.Namespace) -> None:
        """Set the constructor for the Parser."""
        self.raw_content = raw_content
        self.config = config

        config_lang = config.language.replace("-", "_")
        self.langconf = import_module(f"txt2ebook.languages.{config_lang}")

    def __getattr__(self, key: str) -> Any:
        """Get a value of the config based on key name.

        Args:
            key(str): The key name of the config.

        Returns:
            Any: The value of a key, if found. Otherwise raise AttributeError
            exception.
        """
        if hasattr(self.config, key):
            return getattr(self.config, key)

        if hasattr(self.langconf, key):
            return getattr(self.langconf, key)

        raise AttributeError(key)

    def parse(self) -> Book:
        """Parse the content into volumes (optional) and chapters.

        Returns:
          txt2ebook.models.Book: The Book model.
        """
        massaged_content = self.massage()
        tokenizer = Tokenizer(massaged_content, self.config)

        (book_title, authors, tags, toc) = self.parse_tokens(tokenizer)

        book = Book(
            title=book_title,
            language=self.language,
            authors=authors,
            tags=tags,
            cover=self.cover,
            raw_content=self.raw_content,
            massaged_content=massaged_content,
            toc=toc,
            structure_names=self.STRUCTURE_NAMES,
        )

        stats = book.stats()
        logger.info("Found volumes: %s", stats["Volume"])
        logger.info("Found chapters: %s", stats["Chapter"])

        return book

    def words_to_nums(self, words: str, length: int) -> str:
        """Convert header from words to numbers.

        For example, `第一百零八章` becomes `第108章`.

        Args:
            words(str): The line that contains section header in words.
            length(int): The number of left zero-padding to prepend.

        Returns:
            str: The formatted section header.
        """
        if not self.header_number:
            return words

        # left pad the section number if found as halfwidth integer
        match = re.match(rf"第([{self.HALFWIDTH_NUMS}]*)", words)
        if match and match.group(1) != "":
            header_nums = match.group(1)
            return words.replace(
                header_nums, str(header_nums).rjust(length, "0")
            )

        # left pad the section number if found as fullwidth integer
        match = re.match(rf"第([{self.FULLWIDTH_NUMS}]*)", words)
        if match and match.group(1) != "":
            header_nums = match.group(1)
            return words.replace(
                header_nums, str(header_nums).rjust(length, "０")
            )

        match = re.match(rf"第([{self.NUMS_WORDS}]*)", words)
        if not match:
            return words

        if match and match.group(1) == "":
            return words

        header_nums = 0
        header_words = match.group(1)
        for word_grp in re.findall("..?", header_words):
            if len(word_grp) == 2:
                # 零 or 十
                if numeric(word_grp[0]) == 0.0 or numeric(word_grp[0]) == 10.0:
                    header_nums += int(
                        numeric(word_grp[0]) + numeric(word_grp[1])
                    )
                else:
                    header_nums += int(
                        numeric(word_grp[0]) * numeric(word_grp[1])
                    )
            else:
                header_nums += int(numeric(word_grp))

        padded_header_nums = str(header_nums).rjust(length, "0")
        if self.fullwidth:
            padded_header_nums = padded_header_nums.translate(
                HALFWIDTH_FULLWIDTH_MAP
            )

        replaced_words = words.replace(header_words, padded_header_nums)

        logger.debug(
            "Convert header to numbers: %s -> %s",
            words[:10],
            replaced_words[:10],
        )
        return replaced_words

    def parse_tokens(self, tokenizer: Tokenizer) -> Tuple:
        """Parse the tokens and organize into book structure."""
        toc: List[Union[Volume, Chapter]] = []
        book_title = ""
        authors = []
        tags = []
        current_volume = Volume("")
        current_chapter = Chapter("")

        tokens = tokenizer.tokens
        stats = tokenizer.stats()

        # Show chapter tokens by default if no volume tokens
        chapter_verbosity = 0
        paragraph_verbosity = 1
        if bool(stats.get("VOLUME_CHAPTER")) or bool(stats.get("VOLUME")):
            chapter_verbosity = 2
            paragraph_verbosity = 3

        for token in tokens:
            if (
                token.type not in ["CHAPTER", "PARAGRAPH"]
                or (
                    token.type == "CHAPTER"
                    and self.verbose >= chapter_verbosity
                )
                or (
                    token.type == "PARAGRAPH"
                    and self.verbose >= paragraph_verbosity
                )
            ):
                logger.debug(repr(token))

            if token.type == "TITLE":
                book_title = token.value

            if token.type == "AUTHOR":
                authors.append(token.value)

            if token.type == "TAG":
                tags.append(token.value)

            if token.type == "VOLUME_CHAPTER":
                [volume, chapter] = token.value

                volume_title = self.words_to_nums(volume.value, 2)
                if current_volume.title != volume_title:
                    current_volume = Volume(title=volume_title)
                    toc.append(current_volume)

                chapter_title = self.words_to_nums(
                    chapter.value, len(str(stats.get("VOLUME_CHAPTER")))
                )
                if current_chapter.title != chapter_title:
                    current_chapter = Chapter(title=chapter_title)
                    if isinstance(toc[-1], Volume):
                        toc[-1].add_chapter(current_chapter)

            if token.type == "VOLUME":
                volume_title = self.words_to_nums(
                    token.value, len(str(stats.get("VOLUME")))
                )
                if current_volume.title != volume_title:
                    current_volume = Volume(title=volume_title)
                    toc.append(current_volume)

            if token.type == "CHAPTER":
                chapter_title = self.words_to_nums(
                    token.value, len(str(stats.get("CHAPTER")))
                )
                if current_chapter.title != chapter_title:
                    current_chapter = Chapter(title=chapter_title)

                    if toc and isinstance(toc[-1], Volume):
                        toc[-1].add_chapter(current_chapter)
                    else:
                        toc.append(current_chapter)

            if token.type == "PARAGRAPH":
                if toc and isinstance(toc[-1], Volume):
                    toc[-1].chapters[-1].add_paragraph(token.value)

                if toc and isinstance(toc[-1], Chapter):
                    toc[-1].add_paragraph(token.value)

        # Use authors if set explicitly from command line.
        if self.config.author:
            authors = self.config.author

        if self.config.title:
            book_title = self.config.title

        logger.info("Found or set book title: %s", book_title)
        logger.info("Found or set authors: %s", repr(authors))
        logger.info("Found or set categories: %s", repr(tags))

        return (book_title, authors, tags, toc)

    def massage(self) -> str:
        """Massage the txt content.

        Returns:
            str: The formatted book content
        """
        content = self.raw_content

        content = Parser.to_unix_newline(content)

        if self.fullwidth:
            logger.info("Convert halfwidth ASCII characters to fullwidth")
            content = content.translate(HALFWIDTH_FULLWIDTH_MAP)

        if self.re_delete:
            content = self.do_delete_regex(content)

        if self.re_replace:
            content = self.do_replace_regex(content)

        if self.re_delete_line:
            content = self.do_delete_line_regex(content)

        if self.width:
            content = self.do_wrapping(content)

        return content

    def get_regex(self, metadata: str) -> Union[List, str]:
        """Get the regex by the book metadata we want to parse and extract.

        Args:
            metadata(str): The type of the regex for each parser by language.

        Returns:
            List | str: The regex or list of regexs of the type.
        """
        regexs = getattr(self, f"re_{metadata}")
        if regexs:
            return regexs if metadata == "replace" else "|".join(regexs)

        return getattr(self, f"DEFAULT_RE_{metadata.upper()}")

    @staticmethod
    def to_unix_newline(content: str) -> str:
        """Convert all other line ends to Unix line end.

        Args:
            content(str): The formatted book content.

        Returns:
            str: The formatted book content.
        """
        return content.replace("\r\n", "\n").replace("\r", "\n")

    def do_delete_regex(self, content: str) -> str:
        """Remove words/phrases based on regex.

        Args:
            content(str): The formatted book content.

        Returns:
            str: The formatted book content.
        """
        for delete_regex in self.get_regex("delete"):
            content = re.sub(
                re.compile(rf"{delete_regex}", re.MULTILINE), "", content
            )
        return content

    def do_replace_regex(self, content: str) -> str:
        """Replace words/phrases based on regex.

        Args:
            content(str): The formatted book content.

        Returns:
            str: The formatted book content.
        """
        regex = self.get_regex("replace")
        if isinstance(regex, list):
            for search, replace in regex:
                content = re.sub(
                    re.compile(rf"{search}", re.MULTILINE),
                    rf"{replace}",
                    content,
                )

        return content

    def do_delete_line_regex(self, content: str) -> str:
        """Delete whole line based on regex.

        Args:
            content(str): The formatted book content.

        Returns:
            str: The formatted book content.
        """
        for delete_line_regex in self.get_regex("delete_line"):
            content = re.sub(
                re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
                "",
                content,
            )
        return content

    def do_wrapping(self, content: str) -> str:
        """Wrap or fill CJK text.

        Args:
            content (str): The formatted book content.

        Returns:
            str: The formatted book content.
        """
        logger.info("Wrapping paragraph to width: %s", self.width)

        paragraphs = []
        # We don't remove empty line and keep all formatting as it.
        for paragraph in content.split("\n"):
            paragraph = paragraph.strip()

            lines = cjkwrap.wrap(paragraph, width=self.width)
            paragraph = "\n".join(lines)
            paragraphs.append(paragraph)

        wrapped_content = "\n".join(paragraphs)
        return wrapped_content
