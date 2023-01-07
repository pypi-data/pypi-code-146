"""@Author: Rayane AMROUCHE

Http Sources Handling.
"""

import json

from typing import Any

import requests  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource

REQUEST_PARAMS = [
    "url",
    "data",
    "json",
    "params",
    "headers",
    "cookies",
    "files",
    "auth",
    "timeout",
    "allow_redirects",
    "proxies",
    "hooks",
    "stream",
    "verify",
    "cert",
    "data_type",
    "request_type",
]


class HttpSource(DataSource):
    """Inherited Data Source Class for http sources."""

    @staticmethod
    def show_schema() -> None:
        """Get source metadata schema."""
        schema = {
            "source_type": "http",
            "request_type": "get",
            "data_type": "json | text | ...",
            "url": "http_uri",
            "args": {"requests_get|post_argument_keyword": "value_for_this_argument"},
        }
        print(json.dumps(schema, indent=4))

    @staticmethod
    def read_source(
        request_type: str = "get",
        data_type: str = "text",
        session: requests.Session = None,
        close_session: bool = True,
        **kwargs: Any
    ) -> Any:
        """Http source reader.

        Args:
            request_type (str, optional): Type of request. Defaults to "get".
            data_type (str, optional): Type of data output. Defaults to "text".
            session (requests.Session, optional): Http session. Defaults to None.
            close_session (bool, optional): If true the session will be closed after the
                request. Defaults to True.

        Raises:
            Exception: Raised if the type of request is not handled.

        Returns:
            Any: Data from source.
        """
        if not session:
            session = requests.Session()
        if request_type == "get":
            data = session.get(**kwargs)
        elif request_type == "post":
            data = session.post(**kwargs)
        else:
            raise Exception("Request type not handled")
        if close_session:
            session.close()

        if data_type == "json":
            data = data.json()
        elif data_type == "text":
            data = data.text
        return data

    def read(self, source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        self.load_source(source_info, **kwargs)

        args = {}
        for param in REQUEST_PARAMS:
            if param in source_info:
                args[param] = source_info[param]
            if "args" in source_info and param in source_info["args"]:
                if param in args and isinstance(source_info[param], dict):
                    args[param].update(source_info["args"][param])
                else:
                    args[param] = source_info["args"][param]
                del source_info["args"][param]
        data = self.read_source(**args)

        self.logger.info("Read data from '%s'.", args["url"])

        return data
