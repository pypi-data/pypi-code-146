import asyncio
import json
import time
from base64 import b64decode

import aiohttp
import logzero


class PaClient:
    async def request(
        self, method, path, params: dict = None, _is_token_check_request: bool = False
    ):
        if not _is_token_check_request:
            self.logger.debug(f"{method} request {self._base + path}: {params}")
            await self.check_token()
        else:
            self.logger.debug(
                f"{method} request {self._base + path} for user {params['username']}"
            )
        if params is None:
            params = dict()

        if method == "GET":
            return await self._session.get(self._base + path, params=params)
        elif method == "POST":
            return await self._session.post(self._base + path, json=params)
        else:
            raise NotImplementedError

    async def check_token(self):
        if self._token_expire_time - time.time() < 30:  # less than 30s
            if not self.username or not self.password:  # logon using token only
                raise Exception(
                    "Cannot extend the session - login and password are required"
                )
            r = await self.request(
                "POST",
                "login/sign-in",
                {"username": self.username, "password": self.password},
                _is_token_check_request=True,
            )
            if r.status == 200:
                token = (await r.json()).get("data")
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
            if 400 <= r.status < 500:
                raise Exception(
                    f"Failed to get token. Check your login/password: {r.status}"
                )
            else:
                raise Exception(
                    f"Failed to get token. Probably the service is down: {r.status}"
                )
        return True

    def __init__(
        self,
        username: str = None,
        password: str = None,
        token: str = None,
        logger_level=logzero.WARNING,
    ):
        self._session = aiohttp.ClientSession()
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._session.close()

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._session.close())
            else:
                loop.run_until_complete(self._session.close())
        except Exception:
            pass

    async def edit_password(self, new_password):
        resp = await self.request("GET", "user/edit", {"password": new_password})
        resp = await resp.json()
        return resp

    async def health(self):
        resp = await self.request("GET", "pyanalysis/health")
        resp = await resp.json()
        if resp.get("detail") == "Service is ok":
            return True
        else:
            raise Exception(resp.get("detail"))

    async def me(self):
        resp = await self.request("POST", "user/me")
        resp = await resp.json()
        return resp

    async def find_package(
        self,
        package_name: str,
        package_ver: str = None,
        wait_task_completion: bool = True,
    ):
        data = {"package_name": package_name}
        if package_ver:
            data["package_ver"] = package_ver
        resp = await self.request("GET", "pyanalysis/package", data)
        resp = await resp.json()
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
            while status not in ("Finished", "Crashed") and waits:
                self.logger.debug(
                    f"Status {package_name} {package_ver} {resp.get('task_id')} - {status}"
                )
                time.sleep(6)
                status = self.analysis_status(resp.get("task_id"))
                waits -= 1

            resp = await self.request("GET", "pyanalysis/package", data)
            resp = await resp.json()
        if resp.get("status") != "Wait":
            return resp
        raise Exception("Cannot analyze the package. Please contact the developers")

    async def analysis_status(self, task_id: str):
        resp = await self.request("GET", "pyanalysis/task-tree", {"origin_id": task_id})
        """
        #  None of the tasks in Finished or Crashed state
        RUNNING = "Running"
        #  All the tasks are finished OR no tasks are found
        FINISHED = "Finished"
        #  One of the task in tree is in crashed state
        CRASHED = "Crashed"
        """
        return resp.text

    async def kb_package(
        self,
        package_name: str,
        package_ver: str = None,
    ):
        data = {"package_name": package_name}
        if package_ver:
            data["package_ver"] = package_ver
        resp = await self.request("GET", "pyanalysis/knowledge/package", data)
        resp = await resp.json()
        return resp

    async def kb_package_versions(
        self,
        package_name: str,
    ):
        data = {"package_name": package_name}
        resp = await self.request("GET", "pyanalysis/knowledge/package_versions", data)
        resp = await resp.json()
        return resp

    async def kb_package_history(
        self,
        package_name: str,
    ):
        data = {"package_name": package_name}
        resp = await self.request("GET", "pyanalysis/knowledge/package_history", data)
        resp = await resp.json()
        return resp

    async def kb_file_meta(self, file_sha256: str):
        # simple sanity check
        if len(file_sha256) != 64 or not all(
            i in "0123456789abcdef" for i in file_sha256
        ):
            raise Exception("Invalid hash")

        resp = await self.request(
            "GET", "pyanalysis/knowledge/file_meta", {"file_sha256": file_sha256}
        )
        resp = await resp.json()
        return resp

    async def kb_file_bytes(self, file_sha256: str):
        # simple sanity check
        if len(file_sha256) != 64 or not all(
            i in "0123456789abcdef" for i in file_sha256
        ):
            raise Exception("Invalid hash")

        resp = await self.request(
            "GET", "pyanalysis/knowledge/file", {"file_sha256": file_sha256}
        )
        resp = await resp.json()
        return b64decode(resp["data"])

    async def kb_file_releases(self, file_sha256: str):
        # simple sanity check
        if len(file_sha256) != 64 or not all(
            i in "0123456789abcdef" for i in file_sha256
        ):
            raise Exception("Invalid hash")

        resp = await self.request(
            "GET", "pyanalysis/knowledge/file_releases", {"file_sha256": file_sha256}
        )
        resp = await resp.json()
        return resp
