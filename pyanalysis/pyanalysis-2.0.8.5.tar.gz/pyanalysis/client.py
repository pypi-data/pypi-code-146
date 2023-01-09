import json
import time
from base64 import b64decode

import logzero
import requests


class PaClient:
    def request(
        self, method, path, params: dict = None, _is_token_check_request: bool = False
    ):
        if not _is_token_check_request:
            self.logger.debug(f"{method} request {self._base + path}: {params}")
            self.check_token()
        else:
            self.logger.debug(
                f"{method} request {self._base + path} for user {params['username']}"
            )
        if params is None:
            params = dict()

        if method == "GET":
            return self._session.get(self._base + path, params=params)
        elif method == "POST":
            return self._session.post(self._base + path, json=params)
        else:
            raise NotImplementedError

    def check_token(self):
        if self._token_expire_time - time.time() < 30:  # less than 30s
            if not self.username or not self.password:  # logon using token only
                raise Exception(
                    "Cannot extend the session - login and password are required"
                )
            r = self.request(
                "POST",
                "login/sign-in",
                {"username": self.username, "password": self.password},
                _is_token_check_request=True,
            )
            if r.status_code == 200:
                token = r.json().get("data")
                if token:
                    self._session.headers["Authorization"] = f"Bearer {token}"
                    expire_time = json.loads(b64decode(token.split(".")[1] + "=="))[
                        "expires"
                    ]
                    self._token_expire_time = expire_time
                    return True
                raise Exception(
                    "Failed to get token. Something went wrong with the service"
                )
            if 400 <= r.status_code < 500:
                raise Exception("Failed to get token. Check your login/password")
            else:
                raise Exception("Failed to get token. Probably the service is down")
        return True

    def __init__(
        self,
        username: str = None,
        password: str = None,
        token: str = None,
        logger_level=logzero.WARNING,
    ):
        self._session = requests.session()
        self._base = "https://pyanalysis.ptsecurity.tech/api/v2/"
        self.logger = logzero.setup_logger(level=logger_level)
        self.username = None
        self.password = None
        self._token_expire_time = -1

        if username and password:
            self.username = username
            self.password = password
        elif token:
            self._session.headers["Authorization"] = f"Bearer {token}"
            expire_time = json.loads(b64decode(token.split(".")[1] + "=="))["expires"]
            self._token_expire_time = expire_time
        else:
            raise Exception("You should pass (username, password) or token")

        self.check_token()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def __del__(self):
        self._session.close()

    def edit_password(self, new_password):
        resp = self.request("GET", "user/edit", {"password": new_password}).json()
        return resp

    def health(self):
        resp = self.request("GET", "pyanalysis/health").json()
        if resp.get("detail") == "Service is ok":
            return True
        else:
            raise Exception(resp.get("detail"))

    def me(self):
        resp = self.request("POST", "user/me").json()
        return resp

    def find_package(
        self,
        package_name: str,
        package_ver: str = None,
        wait_task_completion: bool = False,
    ):
        data = {"package_name": package_name}
        if package_ver:
            data["package_ver"] = package_ver
        resp = self.request("GET", "pyanalysis/package", data).json()
        if not wait_task_completion:
            return resp
        # fixme: sometimes we need more than one try to properly analyze new package
        tries = 3
        while tries:
            tries -= 1
            if resp.get("status") != "Wait":
                return resp
            status = "Unknown"
            waits = 10
            while status not in ("Finished", "Crashed"):
                self.logger.debug(
                    f"Status {package_name} {package_ver} {resp.get('task_id')} - {status}"
                )
                time.sleep(10)
                status = self.analysis_status(resp.get("task_id"))
                waits -= 1

            resp = self.request("GET", "pyanalysis/package", data).json()
        if resp.get("status") != "Wait":
            return resp
        raise Exception("Cannot analyze the package. Please contact the developers")

    def analysis_status(self, task_id: str):
        status = self.request(
            "GET", "pyanalysis/task-tree", {"origin_id": task_id}
        ).text
        """
        #  None of the tasks in Finished or Crashed state
        RUNNING = "Running"
        #  All the tasks are finished OR no tasks are found
        FINISHED = "Finished"
        #  One of the task in tree is in crashed state
        CRASHED = "Crashed"
        """
        return status

    def kb_package(
        self,
        package_name: str,
        package_ver: str = None,
    ):
        data = {"package_name": package_name}
        if package_ver:
            data["package_ver"] = package_ver
        resp = self.request("GET", "pyanalysis/knowledge/package", data).json()
        return resp

    def kb_package_versions(self, package_name: str):
        data = {"package_name": package_name}
        resp = self.request("GET", "pyanalysis/knowledge/package_versions", data).json()
        return resp

    def kb_package_history(self, package_name: str):
        data = {"package_name": package_name}
        resp = self.request("GET", "pyanalysis/knowledge/package_history", data).json()
        return resp

    def kb_file_meta(self, file_sha256: str):
        # simple sanity check
        if len(file_sha256) != 64 or not all(
            i in "0123456789abcdef" for i in file_sha256
        ):
            raise Exception("Invalid hash")

        resp = self.request(
            "GET", "pyanalysis/knowledge/file_meta", {"file_sha256": file_sha256}
        ).json()
        return resp

    def kb_file_bytes(self, file_sha256: str):
        # simple sanity check
        if len(file_sha256) != 64 or not all(
            i in "0123456789abcdef" for i in file_sha256
        ):
            raise Exception("Invalid hash")

        resp = self.request(
            "GET", "pyanalysis/knowledge/file", {"file_sha256": file_sha256}
        ).json()
        return b64decode(resp["data"])

    def kb_file_releases(self, file_sha256: str):
        # simple sanity check
        if len(file_sha256) != 64 or not all(
            i in "0123456789abcdef" for i in file_sha256
        ):
            raise Exception("Invalid hash")

        resp = self.request(
            "GET", "pyanalysis/knowledge/file_releases", {"file_sha256": file_sha256}
        ).json()
        return resp
