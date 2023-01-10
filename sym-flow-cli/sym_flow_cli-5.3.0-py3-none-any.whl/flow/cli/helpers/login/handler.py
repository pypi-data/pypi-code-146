import urllib.parse as parse
from http.server import BaseHTTPRequestHandler
from typing import ClassVar, Type

from ...helpers.global_options import GlobalOptions


class AuthHTTPRequestHandler(BaseHTTPRequestHandler):

    options: ClassVar[GlobalOptions]
    state: ClassVar[str]
    auth_code: ClassVar[str]
    error_message: ClassVar[str]

    def log_message(self, format, *args):
        ...

    def do_GET(self):
        parsed = parse.urlparse(self.path)
        qs = parse.parse_qs(parsed.query)

        if qs.get("error_description"):
            error_message = qs["error_description"][0]
        elif not qs.get("code"):
            error_message = "Missing code in query"
        elif not qs.get("state"):
            error_message = "Missing state in query"
        elif not qs["state"][0] == self.__class__.state:
            self.__class__.options.dprint(f"Invalid state. Found: {qs['state'][0]}, expected: {self.__class__.state}.")
            error_message = "Invalid state"
        else:
            error_message = None

        if error_message:
            query = parse.urlencode({"message": error_message})
            self.send_response(301)
            self.send_header("Location", f"https://static.symops.com/cli/error?{query}")
            self.end_headers()
            self.__class__.error_message = error_message
            return

        self.send_response(301)
        self.send_header("Location", "https://static.symops.com/cli/login")
        self.end_headers()

        self.__class__.auth_code = qs["code"][0]


def make_handler(options: GlobalOptions, state: str) -> Type[AuthHTTPRequestHandler]:
    class Handler(AuthHTTPRequestHandler):
        ...

    Handler.options = options
    Handler.state = state
    return Handler
