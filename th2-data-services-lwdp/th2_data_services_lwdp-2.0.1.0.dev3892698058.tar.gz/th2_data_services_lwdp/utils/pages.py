from typing import Dict
from th2_data_services_lwdp.commands import http


class Page:
    def __init__(self, data: Dict):  # noqa
        """Page Constructor.

        Args:
            data (Dict): Page Data
        """
        id_ = data.pop("id")
        data["book"] = id_["book"]
        data["name"] = id_["name"]
        self.data = data
        self.book = data["book"]
        self.name = data["name"]
        self.comment = data["comment"]
        self.start_timestamp = data["started"]
        self.end_timestamp = data["ended"]
        self.updated = data["updated"]
        self.removed = data["removed"]

    def __str__(self):  # noqa
        return str(self.data)

    def __repr__(self):  # noqa
        return self.__str__()


def _get_page_object(book_id, page, data_source) -> Page:  # noqa
    if isinstance(page, str):
        if book_id is None:
            raise Exception("If page name is passed then book_id should be passed too!")
        else:
            return data_source.command(http.GetPageByName(book_id, page))
    elif isinstance(page, Page):
        return page
    else:
        raise Exception("Wrong type. page should be Page object or string (page name)!")


class PageNotFound(Exception):
    def __init__(self, name: str, book: str):
        """Exception for the case when the page was not found in data source.

        Args:
            name: Page Name
            book: Book ID
        """
        self._name = name
        self._book = book

    def __str__(self):
        return f"Unable to find the page with name '{self._name}' in book '{self._book}'."
