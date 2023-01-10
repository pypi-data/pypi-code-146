#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard imports """

import concurrent.futures
import sys

import requests
from requests.adapters import HTTPAdapter, Retry
from rich.progress import Progress

from app.application import Application
from app.logz import create_logger


class Api:
    """Wrapper for interacting with the RegScale API"""

    def __init__(self, app: Application):
        """_summary_

        Args:
            api_key (_type_): _description_
        """
        logger = create_logger()
        self.app = app
        self.timeout = 10
        config = app.config
        self.config = config
        self.accept = "application/json"
        self.content_type = "application/json"
        self.logger = logger
        r_session = requests.Session()
        if "ssl_verify" in self.config:
            r_session.verify = self.config["ssl_verify"]
        if "timeout" in self.config:
            self.timeout = self.config["timeout"]
        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        # get the user's domain prefix eg https:// or http://
        domain = config["domain"]
        domain = domain[: (domain.find("://") + 3)]
        r_session.mount(
            domain,
            HTTPAdapter(
                max_retries=retries,
                pool_connections=200,
                pool_maxsize=200,
                pool_block=False,
            ),
        )
        self.session = r_session
        self.auth = None

    def get(self, url: str, headers: dict = None) -> requests.models.Response:
        """Get Request from RegScale endpoint.

        Returns:
            requests.models.Response: Requests response
        """
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
                "accept": self.accept,
                "Content-Type": self.content_type,
            }
        try:
            response = self.session.get(url=url, headers=headers, timeout=self.timeout)
        except requests.exceptions.RequestException as ex:
            self.logger.error("Unable to login to Regscale, exiting\n%s", ex)
            sys.exit(1)
        return response

    def delete(self, url: str, headers: dict = None) -> requests.models.Response:
        """Delete data from RegScale

        Args:
            url (str): _description_
            headers (dict): _description_

        Returns:
            requests.models.Response: _description_
        """
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
                "accept": self.accept,
            }
        return self.session.delete(url=url, headers=headers)

    def post(
        self,
        url: str,
        headers: dict = None,
        json: dict = None,
        data: dict = None,
        auth: tuple = None,
        files: list = None,
    ) -> requests.models.Response:
        """Post data to RegScale.
        Args:
            endpoint (str): RegScale Endpoint
            headers (dict, optional): _description_. Defaults to None.
            json (dict, optional): json data to post. Defaults to {}.

        Returns:
            requests.models.Response: Requests response
        """
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            try:
                headers = {
                    "Authorization": self.config["token"],
                }
            except KeyError as kex:
                self.config["token"] = "Please Enter Token"
                self.app.save_config(self.config)
                self.logger.error(
                    "Token not found in init.yaml, but we have added it.  Please login again\n%s",
                    kex,
                )
        if not json and data:
            response = self.session.post(
                url=url, headers=headers, data=data, files=files, timeout=self.timeout
            )
        else:
            response = self.session.post(
                url=url, headers=headers, json=json, files=files, timeout=self.timeout
            )
        self.logger.debug("URL: %s, headers: %s, data: %s", url, headers, json)
        return response

    def put(
        self, url: str, headers: dict = None, json: dict = None
    ) -> requests.models.Response:
        """Update data for a given RegScale endpoint.
        Args:
            url (str): RegScale Endpoint
            headers (dict, optional): _description_. Defaults to None.
            json (dict, optional): json data to post. Defaults to {}.

        Returns:
            requests.models.Response: Requests reponse
        """
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
            }
        response = self.session.put(
            url=url, headers=headers, json=json, timeout=self.timeout
        )
        self.logger.debug(response.text)
        return response

    def update_server(
        self,
        url: str,
        headers: dict = None,
        json_list=None,
        method="post",
        config=None,
        message="Working",
    ):
        """Concurrent Post or Put of multiple objects

        Args:
            url (str): _description_
            headers (dict): _description_
            dict_list (list): _description_

        Returns:
            _type_: _description_
        """
        if headers is None and config:
            headers = {"Accept": "application/json", "Authorization": config["token"]}
        if json_list and len(json_list) > 0:
            with Progress(transient=False) as progress:
                task = progress.add_task(message, total=len(json_list))
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=self.config["max_threads"]
                ) as executor:
                    if method.lower() == "post":
                        result_futures = list(
                            map(
                                lambda x: executor.submit(self.post, url, headers, x),
                                json_list,
                            )
                        )
                    if method.lower() == "put":
                        result_futures = list(
                            map(
                                lambda x: executor.submit(
                                    self.put, url + f"/{x['id']}", headers, x
                                ),
                                json_list,
                            )
                        )
                    if method.lower() == "delete":
                        result_futures = list(
                            map(
                                lambda x: executor.submit(
                                    self.delete, url + f"/{x['id']}", headers
                                ),
                                json_list,
                            )
                        )
                    for future in concurrent.futures.as_completed(result_futures):
                        try:
                            if future.result().status_code != 200:
                                self.logger.warning(
                                    "status code is %s", future.result().status_code
                                )
                            progress.update(task, advance=1)
                        except Exception as ex:
                            self.logger.error("e is %s, type: %s", ex, type(ex))
