from io import BytesIO
from uuid import uuid4
from sys import hexversion
from codecs import getencoder
from mimetypes import guess_type
from urllib import request, error, parse


class MultipartFormDataEncoder(object):

    def __init__(self):
        self.boundary = uuid4().hex

    @classmethod
    def u(cls, string):

        if hexversion < 0x03000000 and isinstance(string, str):
            string = string.decode("utf-8")

        if hexversion >= 0x03000000 and isinstance(string, bytes):
            string = string.decode("utf-8")

        return string

    def iter(self, fields, files):

        encoder = getencoder("utf-8")

        for (key, value) in fields:

            key = self.u(key)

            yield encoder(f"--{self.boundary}\r\n")
            yield encoder(self.u(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'))

            if isinstance(value, int) or isinstance(value, float):
                value = str(value)

            yield encoder(self.u(f"{value}\r\n"))

        for (key, filename, filedata) in files:

            key = self.u(key)
            filename = self.u(filename)

            yield encoder(f"--{self.boundary}\r\n")
            yield encoder(self.u(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'))
            yield encoder(f"Content-Type: {guess_type(filename)[0] or 'application/octet-stream'}\r\n\r\n")

            buffer = filedata.read()

            yield buffer, len(buffer)
            yield encoder("\r\n")

        yield encoder(f"--{self.boundary}--\r\n")

    def encode(self, fields, files):

        try:

            body = BytesIO()

            for chunk, chunk_len in self.iter(fields, files):
                body.write(chunk)

            return "multipart/form-data; boundary={}".format(self.boundary), body.getvalue()

        except Exception as e:
            if self.errors is True: print(f"[FORM]: {repr(e)}")
