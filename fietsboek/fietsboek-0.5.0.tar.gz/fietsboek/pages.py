"""Module containing logic to support "static" pages."""
import enum
import re
from pathlib import Path
from typing import List, Optional

import markdown
from pyramid.request import Request


class PageException(Exception):
    """Exception that is raised when parsing a :class:`Page` fails."""


class UserFilter(enum.Enum):
    """Filter that determines to which users a page should be shown."""

    LOGGED_IN = enum.auto()
    """Shows the page only to logged in users."""

    LOGGED_OUT = enum.auto()
    """Shows the page only to logged in users."""

    EVERYONE = enum.auto()
    """Shows the page to everyone."""


class Page:
    """Represents a loaded page.

    :ivar slug: The page's slug (URL identifier)
    :vartype slug: str
    :ivar content: The page's content as HTML.
    :vartype content: str
    :ivar link_name: The name of the site to show in the menu.
    :vartype link_name: str
    :ivar locale_filter: An (optional) pattern that determines whether the page
        should be shown to certain locales only.
    :vartype locale_filter: Optional[List[re.Pattern]]
    :ivar user_filter: A filter that determines if the page should be shown to
        certain users only.
    :vartype user_filter: UserFilter
    :ivar menu_index: The index in the menu.
    :vartype menu_index: int
    """

    def __init__(
        self,
        slug: str,
        title: str,
        content: str,
        link_name: str,
        locale_filter: Optional[List[re.Pattern]] = None,
        user_filter: UserFilter = UserFilter.EVERYONE,
        menu_index: int = 0,
    ):
        # pylint: disable=too-many-arguments
        self.slug = slug
        self.title = title
        self.content = content
        self.link_name = link_name
        self.locale_filter = locale_filter
        self.user_filter = user_filter
        self.menu_index = menu_index

    def matches(self, request: Request) -> bool:
        """Checks whether the page matches the given request regarding the
        locale and user filters.

        :param request: The request to check against.
        :return: Whether the page matches the user.
        """
        if self.user_filter == UserFilter.LOGGED_IN and not request.identity:
            return False
        if self.user_filter == UserFilter.LOGGED_OUT and request.identity:
            return False

        if self.locale_filter is not None:
            return any(
                lfilter.match(request.localizer.locale_name) for lfilter in self.locale_filter
            )

        return True

    @classmethod
    def parse(cls, text: str) -> "Page":
        """Parses a :class:`Page` from the given textual source.

        This populates all metadata with the metadata from the file.

        :raises PageException: If there are missing metadata fields.
        :param text: Source to parse.
        :return: The parsed page.
        """
        # Pylint doesn't know about the Markdown extensions:
        # pylint: disable=no-member
        parser = markdown.Markdown(extensions=["meta"])
        content = parser.convert(text)

        title = parser.Meta.get("title", [""])[0]  # type: ignore
        if not title:
            raise PageException("Missing `title`")

        link_name = parser.Meta.get("link-name", [""])[0]  # type: ignore
        if not link_name:
            raise PageException("Missing `link-name`")

        slug = parser.Meta.get("slug", [""])[0]  # type: ignore
        if not slug:
            raise PageException("Missing `slug`")

        locale_filter: Optional[List[re.Pattern]]
        try:
            locale_filter = list(map(re.compile, parser.Meta.get("locale", [])))  # type: ignore
        except re.error as exc:
            raise PageException("Invalid locale regex") from exc
        if not locale_filter:
            locale_filter = None

        filter_map = {
            "logged-in": UserFilter.LOGGED_IN,
            "logged-out": UserFilter.LOGGED_OUT,
            "everyone": UserFilter.EVERYONE,
        }
        user_filter = filter_map.get(
            parser.Meta.get("show-to", ["everyone"])[0].lower()  # type: ignore
        )
        if user_filter is None:
            raise PageException("Invalid `show-to` filter")

        try:
            menu_index = int(parser.Meta.get("index", ["0"])[0])  # type: ignore
        except ValueError as exc:
            raise PageException("Invalid value for `index`") from exc

        return Page(slug, title, content, link_name, locale_filter, user_filter, menu_index)


class Pages:
    """A class that loads static pages from paths and providing easy access for
    other parts of Fietsboek."""

    def __init__(self):
        self.collection = []

    def load_file(self, path: Path):
        """Load a page from a file.

        :param path: The path of the file to load.
        :raises PageException: If the page is malformed.
        """
        source = path.read_text()
        try:
            page = Page.parse(source)
        except PageException as exc:
            raise PageException(f"Error reading `{path}`: {exc}") from None
        # The following could be done "more efficiently", but bisect.insort
        # only supports the key argument starting from Python 3.10. Since we
        # assume that the amount of pages is (very) anyway, and the pages are
        # loaded at application startup, it is not worth trying to come up with
        # clever solutions here. Just do the ovious thing and re-sort the list
        # after every insertion.
        self.collection.append(page)
        self.collection.sort(key=lambda page: page.menu_index)

    def load_directory(self, path: Path):
        """Load a directory full of pages.

        This attemps to load and file in the given directory ending with ".md".

        :param path: The path of the directory to load.
        :raises PageException: If a page is malformed.
        """
        for child in path.glob("*.md"):
            self.load_file(child)

    def find(self, slug: str, request: Optional[Request] = None) -> Optional[Page]:
        """Finds the page matching the given slug.

        If a request is given, the filtering based on locale/logged in state is applied.

        If multiple pages are found, the first found one is returned. If no
        page is found, ``None`` is returned.

        :param slug: The slug of the page:
        :param request: The request to filter against.
        :return: The page, if any is found.
        """
        for page in self.collection:
            if page.slug == slug and (request is None or page.matches(request)):
                return page
        return None

    def pre_menu_items(self, request: Request) -> List[Page]:
        """Return all items that should appear before Fietsboek's main menu.

        :param request: The request to filter against.
        :return: A list of menu entries to show.
        """
        return [page for page in self.collection if page.menu_index < 0 and page.matches(request)]

    def post_menu_items(self, request: Request) -> List[Page]:
        """Return all items that should appear after Fietsboek's main menu.

        :param request: The request to filter against.
        :return: A list of menu entries to show.
        """
        return [page for page in self.collection if page.menu_index > 0 and page.matches(request)]
