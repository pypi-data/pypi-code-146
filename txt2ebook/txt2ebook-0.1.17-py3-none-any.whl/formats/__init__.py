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

"""Packpage of different e-book formats."""

import argparse
from typing import Union

import txt2ebook.models.book
from txt2ebook.formats.epub import EpubWriter
from txt2ebook.formats.txt import TxtWriter
from txt2ebook.helpers import load_class, to_classname
from txt2ebook.models import Book


def create_format(
    book: txt2ebook.models.book.Book,
    ebook_format: str,
    config: argparse.Namespace,
) -> Union[TxtWriter, EpubWriter]:
    """Create ebook formatter by format using factory function.

    Args:
        book(txt2ebook.models.book.Book): The book model which contains
        metadata and table of contents of volumes and chapters.
        ebook_format(str): The ebook format.
        config(argparse.Namespace): The configs from the command-line.

    Returns:
        TxtWriter | EpubWriter
    """
    class_name = to_classname(ebook_format, "Writer")
    klass = load_class("txt2ebook.formats", class_name)
    formatter = klass(book, config)
    return formatter


__all__ = [
    "Book",
    "EpubWriter",
    "TxtWriter",
]
