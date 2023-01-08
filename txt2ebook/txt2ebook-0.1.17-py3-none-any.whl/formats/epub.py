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

"""Convert source text file into EPUB format."""

import io
import logging
import uuid
from importlib.resources import read_text
from pathlib import Path
from typing import Optional, Union

from ebooklib import epub

from txt2ebook.formats.templates import epub as template_epub
from txt2ebook.models import Book, Chapter, Volume

logger = logging.getLogger(__name__)

SPACE = "\u0020"


class EpubWriter:
    """Module for writing ebook in epub format."""

    def __init__(self, book: Book, config: dict) -> None:
        """Create a EpubWriter module.

        Args:
            book(Book): The book model which contains list of chapters and
            other settings.
            opts(dict): The configs from the command-line.

        Returns:
            None
        """
        self.book = book
        self.config = config

    def __getattr__(self, key: str) -> Optional[Union[str, bool]]:
        """Get a value of the config based on key name.

        Args:
            key(str): The key name of the config.

        Returns:
            Any: The value of a key, if found. Otherwise raise AttributeError
            exception.
        """
        if hasattr(self.config, key):
            return getattr(self.config, key)

        raise AttributeError(key)

    def write(self) -> None:
        """Generate the epub file."""
        book = epub.EpubBook()

        if self.book.title:
            book.set_title(self.book.title)

        if self.book.language:
            book.set_language(self.book.language)

        if self.book.authors:
            book.add_author(", ".join(self.book.authors))

        if self.book.cover:
            with open(self.book.cover, "rb") as image:
                book.set_cover("cover.jpg", image.read(), False)

                cover_page = self._build_cover()
                book.add_item(cover_page)
                book.toc.append(cover_page)
                book.spine.append(cover_page)

        self._build_nav(book)

        for section in self.book.toc:
            if isinstance(section, Volume):
                html_volume = self._build_volume(section)
                book.add_item(html_volume)
                book.spine.append(html_volume)

                html_chapters = []
                for chapter in section.chapters:
                    html_chapter = self._build_chapter(chapter, section)
                    book.add_item(html_chapter)
                    book.spine.append(html_chapter)
                    html_chapters.append(html_chapter)

                if self.volume_page:
                    logger.debug("Create separate volume page: %s", section)
                    book.toc.append((html_volume, html_chapters))
                else:
                    book.toc.append(
                        (epub.Section(section.title), html_chapters)
                    )

            if isinstance(section, Chapter):
                html_chapter = self._build_chapter(section)
                book.add_item(html_chapter)
                book.spine.append(html_chapter)
                book.toc.append(html_chapter)

        output_filename = self._gen_output_filename()
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        epub.write_epub(output_filename, book, {})
        logger.info("Generate EPUB file: %s", output_filename)

    def _build_nav(self, book: epub.EpubBook) -> None:
        book.add_item(epub.EpubNcx())

        try:
            logger.info("Using EPUB template: %s", self.epub_template)
            css = read_text(template_epub, f"{self.epub_template}.css")

            book_css = epub.EpubItem(
                uid="style_nav",
                file_name="style/book.css",
                media_type="text/css",
                content=css,
            )
            book.add_item(book_css)

            nav = epub.EpubNav()
            nav.add_link(
                href="style/book.css", rel="stylesheet", type="text/css"
            )
            book.add_item(nav)
            book.spine.append("nav")

        except FileNotFoundError as error:
            logger.error("Unknown EPUB template name: %s", self.epub_template)
            raise SystemExit() from error

    def _gen_id(self) -> str:
        """Generate unique id for the book.

        Ebook reader like Foliate will load configuration of each ebook by this
        id. We set this to book title so it'll load the same configuration even
        though the content have slight changes.
        """
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, self.book.title))

    def _gen_output_filename(self) -> Path:
        """Generate the output EPUB filename."""
        filename = "default"

        if self.output_file:
            filename = str(self.output_file)
        elif isinstance(
            self.input_file, (io.TextIOWrapper, io.BufferedReader)
        ):
            if self.input_file.name != "<stdin>":
                filename = self.input_file.name
        elif self.book.title:
            filename = self.book.title

        file = Path(filename)
        return Path(file.parent, file.stem).with_suffix(".epub")

    def _build_cover(self) -> epub.EpubHtml:
        """Generate the cover image."""
        html = """
            <div id="cover"">
                <img src="cover.jpg" alt="cover" />
            </div>
        """
        cover = epub.EpubHtml(
            title=self.book.structure_names["cover"],
            file_name="cover.xhtml",
            lang=self.book.language,
            content=html,
        )
        cover.add_link(
            href="style/book.css", rel="stylesheet", type="text/css"
        )
        return cover

    def _build_volume(self, volume: Volume) -> epub.EpubHtml:
        """Generate the whole volume to HTML."""
        filename = volume.title
        filename = filename.replace(SPACE, "_")

        header = volume.title
        title = volume.title.split(" ")
        if len(title) == 2:
            header = f"{title[0]}<br />{title[1]}"

        html = "<div class='volume'>"
        html = html + f"<h1 class='volume'>{header}</h1>"
        html = html + "</div>"

        epub_html = epub.EpubHtml(
            title=volume.title,
            file_name=filename + ".xhtml",
            lang=self.book.language,
            content=html,
        )
        epub_html.add_link(
            href="style/book.css", rel="stylesheet", type="text/css"
        )

        return epub_html

    def _build_chapter(
        self, chapter: Chapter, volume: Optional[Volume] = None
    ) -> epub.EpubHtml:
        """Generate the whole chapter to HTML."""
        if volume:
            filename = f"{volume.title}_{chapter.title}"
        else:
            filename = chapter.title

        filename = filename.replace(SPACE, "_")

        html = f"<h2>{chapter.title}</h2>"
        for paragraph in chapter.paragraphs:
            paragraph = paragraph.replace("\n", "")
            html = html + f"<p>{paragraph}</p>"

        epub_html = epub.EpubHtml(
            title=chapter.title,
            file_name=filename + ".xhtml",
            lang=self.book.language,
            content=html,
        )
        epub_html.add_link(
            href="style/book.css", rel="stylesheet", type="text/css"
        )

        return epub_html
