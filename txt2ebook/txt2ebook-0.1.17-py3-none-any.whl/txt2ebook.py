# pylint: disable=no-value-for-parameter
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

"""txt2ebook/tte is a cli tool to convert txt file to ebook format."""

import argparse
import logging
import sys
from typing import Optional, Sequence

from bs4 import UnicodeDammit
from langdetect import detect

from txt2ebook import __version__, setup_logger
from txt2ebook.exceptions import EmptyFileError
from txt2ebook.formats import create_format
from txt2ebook.parser import Parser

EBOOK_EXTS = ["epub", "txt"]

logger = logging.getLogger(__name__)


def run(config: argparse.Namespace) -> None:
    """Set the main application logic."""
    logger.debug(config)

    logger.info("Parsing txt file: %s", config.input_file.name)

    unicode = UnicodeDammit(config.input_file.read())
    logger.info("Detect encoding : %s", unicode.original_encoding)

    content = unicode.unicode_markup
    if not content:
        raise EmptyFileError(f"Empty file content in {config.input_file.name}")

    config.language = config.language or detect(content)
    logger.info("Detect language: %s", config.language)

    parser = Parser(content, config)
    book = parser.parse()

    if config.test_parsing or config.debug:
        book.debug(config.verbose)

    if not config.test_parsing:
        if book.toc:
            for ebook_format in config.format:
                writer = create_format(book, ebook_format, config)
                writer.write()
        else:
            logger.warning("No table of content found, not exporting")


def build_parser(
    args: Optional[Sequence[str]] = None,
) -> argparse.ArgumentParser:
    """Generate the argument parser."""
    args = args or []

    parser = argparse.ArgumentParser(
        add_help=False,
        description=_doc(),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "input_file",
        nargs=None if sys.stdin.isatty() else "?",  # type: ignore
        type=argparse.FileType("rb"),
        default=None if sys.stdin.isatty() else sys.stdin,
        help="source text filename",
        metavar="TXT_FILENAME",
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help=(
            "converted ebook filename "
            "(default: 'TXT_FILENAME.{" + ",".join(EBOOK_EXTS) + "}')"
        ),
        metavar="EBOOK_FILENAME",
    )

    parser.add_argument(
        "-f",
        dest="format",
        default=["epub", "txt"],
        choices=EBOOK_EXTS,
        action="append",
        help="ebook format (default: '%(default)s')",
    )

    parser.add_argument(
        "-t",
        dest="title",
        default=None,
        help="title of the ebook (default: '%(default)s')",
        metavar="TITLE",
    )

    parser.add_argument(
        "-l",
        dest="language",
        default=None,
        help="language of the ebook (default: '%(default)s')",
        metavar="LANGUAGE",
    )

    parser.add_argument(
        "-a",
        dest="author",
        default=[],
        action="append",
        help="author of the ebook (default: '%(default)s')",
        metavar="AUTHOR",
    )

    parser.add_argument(
        "-c",
        dest="cover",
        default=None,
        help="cover of the ebook",
        metavar="IMAGE_FILENAME",
    )

    parser.add_argument(
        "-w",
        dest="width",
        type=int,
        default=None,
        help="width for line wrapping",
        metavar="WIDTH",
    )

    parser.add_argument(
        "-ps",
        dest="paragraph_separator",
        type=str,
        default="\n\n",
        help="paragraph separator (default: %(default)r)",
        metavar="SEPARATOR",
    )

    parser.add_argument(
        "-rd",
        dest="re_delete",
        default=[],
        action="append",
        help=("regex to delete word or phrase " "(default: '%(default)s')"),
        metavar="REGEX",
    )

    parser.add_argument(
        "-rvc",
        dest="re_volume_chapter",
        default=[],
        action="append",
        help=(
            "regex to parse volume and chapter header "
            "(default: by LANGUAGE)"
        ),
        metavar="REGEX",
    )

    parser.add_argument(
        "-rv",
        dest="re_volume",
        default=[],
        action="append",
        help=("regex to parse volume header " "(default: by LANGUAGE)"),
        metavar="REGEX",
    )

    parser.add_argument(
        "-rc",
        dest="re_chapter",
        default=[],
        action="append",
        help=("regex to parse chapter header " "(default: by LANGUAGE)"),
        metavar="REGEX",
    )

    parser.add_argument(
        "-rt",
        dest="re_title",
        default=[],
        action="append",
        help=("regex to parse title of the book " "(default: by LANGUAGE)"),
        metavar="REGEX",
    )

    parser.add_argument(
        "-ra",
        dest="re_author",
        default=[],
        action="append",
        help=("regex to parse author of the book " "(default: by LANGUAGE)"),
        metavar="REGEX",
    )

    parser.add_argument(
        "-rl",
        dest="re_delete_line",
        default=[],
        action="append",
        help="regex to delete whole line " "(default: '%(default)s')",
        metavar="REGEX",
    )

    parser.add_argument(
        "-rr",
        dest="re_replace",
        nargs=2,
        default=[],
        action="append",
        help="regex to search and replace " "(default: '%(default)s')",
        metavar="REGEX",
    )

    parser.add_argument(
        "-et",
        default="clean",
        dest="epub_template",
        help="CSS template for epub ebook (default: '%(default)s')",
        metavar="TEMPLATE",
    )

    parser.add_argument(
        "-vp",
        "--volume-page",
        default=False,
        action="store_true",
        dest="volume_page",
        help="generate each volume as separate page (only 'epub' format)",
    )

    parser.add_argument(
        "-tp",
        "--test-parsing",
        default=False,
        action="store_true",
        dest="test_parsing",
        help="test parsing for volume/chapter header",
    )

    parser.add_argument(
        "-hn",
        "--header-number",
        default=False,
        action="store_true",
        dest="header_number",
        help=(
            "convert section header from words to numbers "
            "(only zh-cn/zh-tw)"
        ),
    )

    parser.add_argument(
        "-fw",
        "--fullwidth",
        default=False,
        action="store_true",
        dest="fullwidth",
        help=(
            "convert ASCII character from halfwidth to fullwidth "
            "(only zh-cn/zh-tw)"
        ),
    )

    parser.add_argument(
        "-rw",
        "--raise-on-warning",
        default=False,
        action="store_true",
        dest="raise_on_warning",
        help="raise exception and stop parsing if there are warnings",
    )

    parser.add_argument(
        "-ob",
        "--overwrite-backup",
        default=False,
        action="store_true",
        dest="overwrite_backup",
        help="overwrite massaged and backup original TXT_FILENAME",
    )

    parser.add_argument(
        "-ow",
        "--overwrite",
        default=False,
        action="store_true",
        dest="overwrite",
        help="overwrite massaged TXT_FILENAME",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        default=0,
        action="count",
        dest="verbose",
        help="show verbosity of debugging log, use -vv, -vvv for more details",
    )
    parser.add_argument(
        "-d",
        "--debug",
        default=False,
        action="store_true",
        dest="debug",
        help="show debugging log and stacktrace",
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="show this help message and exit",
    )

    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def _doc() -> str:
    return (
        __doc__
        + "\n  website: https://github.com/kianmeng/txt2ebook"
        + "\n  issues: https://github.com/kianmeng/txt2ebook/issues"
    )


def main(args: Optional[Sequence[str]] = None):
    """Set the main entrypoint of the CLI script."""
    args = args or sys.argv[1:]
    config = argparse.Namespace()

    try:
        parser = build_parser(args)
        config = parser.parse_args(args)
        logger.debug(config)

        setup_logger(config)
        run(config)

    except Exception as error:
        logger.error(
            getattr(error, "message", str(error)),
            exc_info=getattr(config, "debug", True),
        )
        raise SystemExit(1) from None
