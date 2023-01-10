from __future__ import annotations

import logging
import mimetypes
import re
from io import BytesIO

log = logging.getLogger(__name__)


class Image(BytesIO):
    def __init__(self, content=None, filename=None, mimetype=None):
        self.filename = filename

        # initialize BytesIO now so we can inspect it for mimetype if needed
        super().__init__(content)

        extension = mimetypes.guess_extension(mimetype if mimetype else "")
        if filename is not None:
            self.format = filename.split(".")[-1].lower()
        elif extension is not None:
            self.format = extension.split(".")[-1]
        else:
            self.format = None
            log.warning(
                "Unknown extension for this image. No filename or mimetype provided."
            )

    def save(self, filename=None, mode="wb"):
        filename = filename or self.filename
        nbytes = len(self.getvalue())
        if filename is None:
            raise ValueError("Please set a filename to save to first.")
        with open(filename, mode) as f:
            f.write(self.read())
        log.info(f"Written {len(self.getvalue()):d} bytes to {filename:s}")
        return nbytes

    def _repr_png_(self):
        if self.format == "png":
            return self.getvalue()

    def _repr_jpeg_(self):
        if self.format in ["jpeg", "jpg"]:
            return self.getvalue()

    def _repr_svg_(self):
        if self.format == "svg":
            return self.getvalue()

    @classmethod
    def from_response(cls, response):
        filename = None

        if response.headers.get("content-disposition") is not None:
            filename = re.findall(
                "filename=(.+)", response.headers.get("content-disposition")
            )[0]

        mimetype = response.headers.get("content-type")

        return cls(content=response.content, filename=filename, mimetype=mimetype)
