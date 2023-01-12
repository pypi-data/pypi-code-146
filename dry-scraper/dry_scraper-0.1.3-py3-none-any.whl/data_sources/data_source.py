import os

import requests
from abc import ABC
from typing import ClassVar


class DataSource(ABC):
    """
    Abstract class that represents an online data source.

    ...

    Attributes
    ----------
    _content : str
        string representation of raw data retrieved by fetch_content()
    _url : str
        fully qualified URL location of data source, completed on instantiation
    _url_stub : ClassVar[str]
        partial URL location of data source
    _extension : ClassVar[str]
        file extension to be used when writing the raw data source to disk e.g. json, HTM

    Methods
    -------
    fetch_content():# -> Self:
        fetch content from self.url and store response in self.content
    write_content():# -> Self:
        write self.content to path and extension specified by the object
    """

    _content: str
    _url: str
    _url_stub: ClassVar[str]
    _extension: ClassVar[str]

    @property
    def content(self) -> str | None:
        return getattr(self, "_content", None)

    @content.setter
    def content(self, value: str) -> None:
        self._content = value

    @property
    def url(self) -> str | None:
        return getattr(self, "_url", None)

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    @property
    def url_stub(self) -> str:
        return self._url_stub

    @property
    def extension(self) -> str:
        return self._extension

    def fetch_content(self):  # -> Self:
        """
        Use requests.get to retrieve file at URL and store response in self.content

        Returns:
            self
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.content = response.text
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        return self

    def write_content(self, path: str, filename: str):  # -> Self:
        """Write content to {path}/{filename}.{self.extension}

        Args:
            filename (str): desired filename
            path (str): path to save location
        """
        full_path = os.path.join(path, f"{filename}.{self.extension}")
        try:
            with open(full_path, "w") as f:
                f.write(self.content)
        except OSError as e:
            print(f"Failed to write to {full_path}.")
            print(e)
        except Exception as e:
            print(e)
        return self
