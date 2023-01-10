from __future__ import annotations

import html
import logging
import re
import zipfile
from io import BytesIO

log = logging.getLogger(__name__)


class ZipFile(zipfile.ZipFile):
    def __init__(self, content=None, filename=None):
        self._content = content
        super().__init__(BytesIO(self._content))
        self.filename = filename
        self.format = filename.split(".")[-1].lower()

    def save(self, filename=None, mode="wb"):
        filename = filename or self.filename
        nbytes = len(self._content)
        with open(filename, mode) as f:
            f.write(self._content)
        log.info(f"Written {nbytes:d} bytes to {filename:s}")
        return nbytes

    def _repr_html_(self):
        return (
            html.escape(repr(self))
            + "<ul><li>"
            + "</li><li>".join(map(lambda x: html.escape(repr(x)), self.filelist))
            + "</li></ul>"
        )

    @classmethod
    def from_response(cls, response):
        filename = re.findall(
            "filename=(.+)", response.headers.get("content-disposition")
        )[0]
        return cls(content=response.content, filename=filename)
