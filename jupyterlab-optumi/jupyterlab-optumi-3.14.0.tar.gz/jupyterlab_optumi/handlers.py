"""
Copyright (C) Optumi Inc - All rights reserved.

You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
"""

## Jupyter imports
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import authenticated
import nbformat, subprocess

from ._version import __version__

## Standard library imports

# Generic Operating System Services
import os, io, time, re, datetime

# Python Runtime Services
import traceback

# Internet Protocols and Support
import uuid
from urllib.error import URLError
from urllib.parse import urlencode
import requests

# Internet Data Handling
import json, mimetypes, base64

# Data Compression and Archiving
from zipfile import ZipFile, ZIP_DEFLATED

# Cryptographic Services
import hashlib

# Numeric and Mathematical Modules
import random, math

# Structured Markup Processing Tools
import html

## Other imports
from cryptography import x509
from cryptography.hazmat.backends import default_backend

## Optumi imports
import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    ServiceException,
    OptumiException,
)


## Flags
# WARNING: This flag will show error tracebacks where normally not shown, but it will cause some < 500 response codes to be 500
DEBUG = False


# This is OKTA stuff
LOGIN_SERVER = "https://olh.optumi.net:8443"
REDIRECT_URI = LOGIN_SERVER + "/redirect"
BASE_URL = "https://login.optumi.com"
AUTH_SERVER_ID = "default"
CLIENT_ID = "0oa1seifygaiUCgoA5d7"

LOGIN_WRAP_START = '<div style="position: absolute;top: 40%;width: calc(100% - 16px);"><div style="display: grid;justify-content: center;"><img style="margin: auto;" src="https://www.optumi.com/wp-content/uploads/2020/10/optumi-logo-header.png" srcset="https://www.optumi.com/wp-content/uploads/2020/10/optumi-logo-header.png 1x" width="200" height="50" alt="Optumi Logo" retina_logo_url="" class="fusion-standard-logo"><div style="text-align: center;font-size: 1.5rem">'
LOGIN_WRAP_END = "</div></div></div>"

jupyter_token = ""

login_state = None
login_pkce = None
login_token = None

jupyter_log = None

dev_version = "dev" in __version__.lower()

split_version = __version__.split(".")
jupyterlab_major = split_version[0]
optumi_major = split_version[1]
PORTAL = (
    "portal"
    + jupyterlab_major
    + (optumi_major if len(optumi_major) == 2 else "0" + optumi_major)
    + ".optumi.net"
)
PORTAL_PORT = 8443
PORTAL_DOMAIN_AND_PORT = PORTAL + ":" + str(PORTAL_PORT)

agreement = None


class VersionHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            self.write(
                json.dumps(
                    {
                        "version": __version__,
                        "userHome": optumi.core.get_user_home(),
                        "jupyterHome": optumi.core.get_app_home(),
                    }
                )
            )
        except Exception as e:
            # 401 unauthorized
            self.set_status(401)
            self.write(
                json.dumps({"message": "Encountered error while getting version"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetAgreementHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global agreement
        try:
            if agreement is None:
                response = await IOLoop.current().run_in_executor(
                    None, optumi.login.get_new_agreement
                )
                if not getattr(response, "url", False) or response.status_code != 200:
                    self.write(
                        json.dumps(
                            {
                                "message": "Encountered error while getting new user agreement",
                                "loginFailed": True,
                            }
                        )
                    )
                    jupyter_log.error(
                        optumi.logging.optumi_format_and_log(self, str(response))
                    )
                    IOLoop.current().run_in_executor(None, optumi.login.logout)
                    return
                newAgreement = len(response.content) > 0
                if newAgreement:
                    agreement = base64.decodebytes(response.content)

            self.write(agreement)
        except Exception as e:
            # We do not want to print an error here, since it can be part of normal operation
            self.set_status(200)
            self.write(
                json.dumps(
                    {
                        "message": "Encountered error while getting user information",
                        "loginFailed": True,
                    }
                )
            )
            if DEBUG:
                raise e


class CheckLoginHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global agreement
        try:
            extension_version = __version__
            response = await IOLoop.current().run_in_executor(
                None, optumi.login.exchange_versions, extension_version, "jupyterlab"
            )
            if not getattr(response, "url", False) or response.status_code != 200:
                self.write(
                    json.dumps(
                        {
                            "loginFailedMessage": response.text,
                            "message": "Version exchange failed",
                            "loginFailed": True,
                        }
                    )
                )
                jupyter_log.error(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
                IOLoop.current().run_in_executor(None, optumi.login.logout)
                return
            controller_version = response.text
            response = await IOLoop.current().run_in_executor(
                None, optumi.login.get_new_agreement
            )
            if not getattr(response, "url", False) or response.status_code != 200:
                self.write(
                    json.dumps(
                        {
                            "message": "Encountered error while getting new user agreement",
                            "loginFailed": True,
                        }
                    )
                )
                jupyter_log.error(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
                IOLoop.current().run_in_executor(None, optumi.login.logout)
                return
            newAgreement = len(response.content) > 0
            if newAgreement:
                agreement = base64.decodebytes(response.content)
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_user_information, True
            )
            self.set_status(response.status_code)
            user_information = json.loads(response.content)
            user_information["newAgreement"] = newAgreement
            user_information["message"] = "Logged in successfully"
            self.write(user_information)
        except Exception as e:
            # We do not want to print an error here, since it can be part of normal operation
            self.set_status(200)
            self.write(
                json.dumps(
                    {
                        "message": "Encountered error while getting user information",
                        "loginFailed": True,
                    }
                )
            )
            if DEBUG:
                raise e


class LoginHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global login_token
        global domain_and_port
        global agreement
        try:
            if login_token is None:
                self.set_status(401)
                self.write(json.dumps({"message": "Not authorized"}))
                return
            else:
                login_status, message = await IOLoop.current().run_in_executor(
                    None,
                    optumi.login.login_rest_server,
                    PORTAL,
                    PORTAL_PORT,
                    login_token,
                    "jupyterlab",
                )

                if dev_version:
                    jupyter_log.info(
                        optumi.logging.optumi_format_and_log(
                            self, "REST login completed"
                        )
                    )
                else:
                    optumi.logging.optumi_format_and_log(self, "REST login completed")

            # Reset the login progress
            optumi.login.set_login_progress(None)
            login_token = None
            if login_status == 1:
                ### NOTE: If we succeed logging in but fail after, we want to try to logout
                ## Exchange versions
                extension_version = __version__
                response = await IOLoop.current().run_in_executor(
                    None,
                    optumi.login.exchange_versions,
                    extension_version,
                    "jupyterlab",
                )
                if not getattr(response, "url", False) or response.status_code != 200:
                    self.write(
                        json.dumps(
                            {
                                "loginFailedMessage": response.text,
                                "message": "Version exchange failed",
                                "loginFailed": True,
                            }
                        )
                    )
                    jupyter_log.error(
                        optumi.logging.optumi_format_and_log(self, str(response))
                    )
                    IOLoop.current().run_in_executor(None, optumi.login.logout)
                    return

                controller_version = response.text

                if dev_version:
                    jupyter_log.info(
                        optumi.logging.optumi_format_and_log(
                            self, "Exchanged controller versions"
                        )
                    )
                else:
                    optumi.logging.optumi_format_and_log(
                        self, "Exchanged controller versions"
                    )

                ## Get new agreement
                response = await IOLoop.current().run_in_executor(
                    None, optumi.login.get_new_agreement
                )
                if not getattr(response, "url", False) or response.status_code != 200:
                    self.write(
                        json.dumps(
                            {
                                "loginFailedMessage": "Unable to get agreement",
                                "message": "Getting agreement failed",
                                "loginFailed": True,
                            }
                        )
                    )
                    jupyter_log.error(
                        optumi.logging.optumi_format_and_log(self, str(response))
                    )
                    IOLoop.current().run_in_executor(None, optumi.login.logout)
                    return
                newAgreement = len(response.content) > 0
                if newAgreement:
                    agreement = base64.decodebytes(response.content)

                # We should check that the versions are valid
                if dev_version:
                    jupyter_log.info(
                        optumi.logging.optumi_format_and_log(
                            self,
                            "Connected to Optumi controller version "
                            + controller_version,
                        )
                    )
                else:
                    optumi.logging.optumi_format_and_log(
                        self,
                        "Connected to Optumi controller version " + controller_version,
                    )

                ## Get user information
                response = await IOLoop.current().run_in_executor(
                    None, optumi.core.get_user_information, True
                )
                if not getattr(response, "url", False) or response.status_code != 200:
                    self.set_status(response.status_code)
                    self.write(
                        json.dumps(
                            {
                                "loginFailedMessage": "Unable to get user information",
                                "message": "Unable to get user information",
                                "loginFailed": True,
                            }
                        )
                    )
                    jupyter_log.error(
                        optumi.logging.optumi_format_and_log(self, str(response))
                    )
                    IOLoop.current().run_in_executor(None, optumi.login.logout)
                    return
                user_information = json.loads(response.content)
                user_information["newAgreement"] = newAgreement
                user_information["message"] = "Logged in successfully"
                self.write(json.dumps(user_information))
            elif login_status == -1:
                self.write(
                    json.dumps(
                        {
                            "loginFailedMessage": message,
                            "message": "Login failed with message: " + message,
                            "loginFailed": True,
                        }
                    )
                )
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(
                        self, "Login failed with message: " + message
                    )
                )
            elif login_status == -2:
                self.write(
                    json.dumps(
                        {
                            "loginFailedMessage": "Login failed",
                            "loginFailed": True,
                            "message": "Login failed due to invalid request",
                            "domainFailed": True,
                        }
                    )
                )
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, "Login failed")
                )

            if dev_version:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, "Login completed")
                )
            else:
                optumi.logging.optumi_format_and_log(self, "Login completed")

        except NotLoggedInException as e:
            self.write(
                json.dumps(
                    {
                        "message": "Not logged in",
                        "loginFailedMessage": "Unable to login",
                        "loginFailed": True,
                    }
                )
            )
        except Exception as e:
            self.set_status(401)
            self.write(
                json.dumps(
                    {
                        "loginFailedMessage": "Login failed",
                        "loginFailed": True,
                        "message": "Encountered error while handling login",
                    }
                )
            )
            IOLoop.current().run_in_executor(None, optumi.login.logout)
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    return {"code_verifier": code_verifier, "code_challenge": code_challenge}


def generate_state():
    randomCharset = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ret = ""
    for i in range(64):
        ret += randomCharset[random.randint(0, len(randomCharset) - 1)]
    return ret


last_login_time = None


class OauthLoginHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global login_state
        global login_pkce
        global last_login_time

        now = time.time()
        if last_login_time != None and now - last_login_time < 0.5:
            raise Exception("Blocking rapid logins")
        last_login_time = now

        if dev_version:
            jupyter_log.info(
                optumi.logging.optumi_format_and_log(self, "OAUTH login initiated")
            )
        else:
            optumi.logging.optumi_format_and_log(self, "OAUTH login initiated")

        try:
            login_pkce = generate_pkce()
            login_state = {
                "state": generate_state(),
                "origin": self.request.protocol + "://" + self.request.host,
                "token": jupyter_token,
            }

            data = {
                "client_id": CLIENT_ID,
                "response_type": "code",
                "scope": "openid",
                "redirect_uri": REDIRECT_URI,
                "state": json.dumps(login_state),
                "code_challenge_method": "S256",
                "code_challenge": login_pkce["code_challenge"],
            }
            url_data = urlencode(data)
            url = BASE_URL + "/oauth2/" + AUTH_SERVER_ID + "/v1/authorize?" + url_data

            self.redirect(url)
        except Exception as e:
            self.set_status(401)
            self.write(json.dumps({"message": "Encountered error setting login state"}))
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class OauthCallbackHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global login_state
        global login_pkce
        global login_token
        try:
            code = self.get_argument("code")
            state = json.loads(self.get_argument("state"))

            if json.dumps(login_state, sort_keys=True) != json.dumps(
                state, sort_keys=True
            ):
                raise Exception("State does not match expected state in oauth callback")

            ## Exchange code for access and id token

            url = "https://dev-68278524.okta.com/oauth2/" + AUTH_SERVER_ID + "/v1/token"

            payload = {
                "client_id": CLIENT_ID,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
                "code": code,
                "code_verifier": login_pkce["code_verifier"],
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            # Reset these so they can't be used again
            login_state = None
            login_pkce = None

            login_token = response.text

            optumi.login.set_login_progress("Allocating...")

            # # # If we want to access parts of the token here, we can do so like this:
            # # json.loads(token)
            # # print(token['access_token'])
            # # print(token['id_token'])

            self.write(
                LOGIN_WRAP_START
                + "You have successfully logged into Optumi and you can close this tab"
                + LOGIN_WRAP_END
            )
        except Exception as e:
            self.set_status(401)
            self.write(
                json.dumps(
                    {"message": "Encountered error while handling oauth callback"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class SignAgreementHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            timeOfSigning = data["timeOfSigning"]
            hashOfSignedAgreement = optumi.utils.hash_string(agreement)
            response = await IOLoop.current().run_in_executor(
                None, optumi.login.sign_agreement, timeOfSigning, hashOfSignedAgreement
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"message": "Encountered error signing agreement"}))
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetUserInformationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            includeAll = data["includeAll"]
            timestamp = data["timestamp"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_user_information, includeAll, timestamp
            )
            self.write(response.content)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error getting user information"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class SetUserInformationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            param = data["param"]
            value = data["value"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.set_user_information, param, value
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error setting user information"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class LogoutHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, optumi.login.logout)
            self.set_status(response.status_code)
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"message": "Encountered error while logging out"}))
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class PreviewNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbConfig = data["nbConfig"]
            includeExisting = data["includeExisting"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.preview_notebook, nbConfig, includeExisting
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while previewing notebook"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class SetupNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data["name"]
            timestamp = data["timestamp"]
            notebook = data["notebook"]
            nbConfig = data["nbConfig"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.setup_notebook, name, timestamp, notebook, nbConfig
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while setting up notebook"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class LaunchNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            requirementsFile = data.get(
                "requirementsFile"
            )  # we use .get() for params that are not required
            paths = data.get("paths")
            expanded = (
                [] if paths is None else [optumi.utils.normalize_path(f) for f in paths]
            )
            hashes = [optumi.utils.hash_file(f) for f in expanded]
            stats = [os.stat(f) if os.path.isfile(f) else None for f in expanded]
            creationTimes = [
                datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z"
                if stat != None
                else str(None)
                for stat in stats
            ]
            lastModificationTimes = [
                datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"
                if stat != None
                else str(None)
                for stat in stats
            ]
            sizes = [str(stat.st_size) if stat else str(None) for stat in stats]
            uuid = data["uuid"]
            timestamp = data["timestamp"]
            IOLoop.current().run_in_executor(
                None,
                optumi.core.launch_notebook,
                requirementsFile,
                hashes,
                paths,
                creationTimes,
                lastModificationTimes,
                sizes,
                uuid,
                timestamp,
            )
            self.write(
                json.dumps(
                    {
                        "message": "success",
                        "hashes": hashes,
                        "files": paths,
                        "filesmod": lastModificationTimes,
                        "filessize": sizes,
                    }
                )
            )
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while launching notebook"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetLaunchStatusHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data["uuid"]
            json_map = await IOLoop.current().run_in_executor(
                None, optumi.core.get_launch_status, uuid
            )
            if json_map == {}:
                self.set_status(204)  # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while getting launch status"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetUploadProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            keys = data["keys"]
            json_map = await IOLoop.current().run_in_executor(
                None, optumi.core.get_upload_progress, keys
            )
            if json_map == {}:
                self.set_status(204)  # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting upload progress"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetCompressionProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            keys = data["keys"]
            json_map = await IOLoop.current().run_in_executor(
                None, optumi.core.get_compression_progress, keys
            )
            if json_map == {}:
                self.set_status(204)  # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting compression progress"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetLoginProgressHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            login_progress = await IOLoop.current().run_in_executor(
                None, optumi.login.get_login_progress
            )
            if login_progress == None:
                self.set_status(204)  # 204 No content
            else:
                self.write(login_progress)
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting login progress"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class StopNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data["workload"]
            response = await IOLoop.current().run_in_executor(
                None,
                optumi.core.stop_notebook,
                workload,
                None,  # Remove the second argument when we move to 3.14
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while stopping notebook"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class TeardownNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data["workload"]
            response = await IOLoop.current().run_in_executor(
                None,
                optumi.core.teardown_notebook,
                workload,
                None,  # Remove the second argument when we move to 3.14
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while tearing down notebook"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetMachinesHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_machines
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while getting machines"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetWorkloadsHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_workloads
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while getting workloads"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetNotebookConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKey = data["nbKey"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_notebook_config, nbKey
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting notebook config"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class SetNotebookConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKey = data["nbKey"]
            nbConfig = data["nbConfig"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.set_notebook_config, nbKey, nbConfig
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while setting notebook config"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class PullPackageUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKeys = data["nbKeys"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.pull_package_update, nbKeys
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while pulling package update"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class PushPackageUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKey = data["nbKey"]
            label = data.get("label")
            paths = data.get("paths")
            expanded = (
                [] if paths is None else [optumi.utils.normalize_path(f) for f in paths]
            )
            hashes = [optumi.utils.hash_file(f) for f in expanded]
            update = data["update"]
            response = await IOLoop.current().run_in_executor(
                None,
                optumi.core.push_package_update,
                nbKey,
                label,
                hashes,
                paths,
                update,
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while pulling package update"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class PullWorkloadConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data["workload"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.pull_workload_config, workload
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while pulling workload config"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class PushWorkloadConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data["workload"]
            nbConfig = data["nbConfig"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.push_workload_config, workload, nbConfig
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while pushing workload config"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetDataConnectorsHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, get_data_connectors)
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting data connectors"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class AddDataConnectorHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            dataService = data["dataService"]
            name = data["name"]
            info = data["info"]
            response = await IOLoop.current().run_in_executor(
                None, add_data_connector, dataService, name, info
            )
            self.write(json.dumps({"message": response.text}))
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while adding data connector"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class RemoveDataConnectorHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data["name"]
            response = await IOLoop.current().run_in_executor(
                None, remove_data_connector, name
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while removing data connector"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetIntegrationsHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_integrations
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting environment variables"}
                )
            )
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG:
                raise e


class AddIntegrationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data["name"]
            info = data["info"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.add_integration, name, info, False
            )
            self.write(json.dumps({"message": response.text}))
            if response.status_code >= 300:
                jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while adding environment variable"}
                )
            )
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG:
                raise e


class RenameIntegrationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            oldName = data["oldName"]
            newName = data["newName"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.rename_integration, oldName, newName
            )
            self.write(json.dumps({"message": response.text}))
            if response.status_code >= 300:
                jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while renaming environment variable"}
                )
            )
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG:
                raise e


class RemoveIntegrationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data["name"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.remove_integration, name
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while removing environment variable"}
                )
            )
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG:
                raise e


class PushWorkloadInitializingUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data["uuid"]
            update = data["update"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.push_workload_initializing_update, uuid, update
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {
                        "message": "Encountered error while pushing workload status update"
                    }
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class PullWorkloadStatusUpdatesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuids = data["uuids"]
            lastInitializingLines = data["lastInitializingLines"]
            lastPreparingLines = data["lastPreparingLines"]
            lastRunningLines = data["lastRunningLines"]
            response = await IOLoop.current().run_in_executor(
                None,
                optumi.core.pull_workload_status_updates,
                uuids,
                lastInitializingLines,
                lastPreparingLines,
                lastRunningLines,
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {
                        "message": "Encountered error while pulling workload status update"
                    }
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class PullModuleStatusUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workloadUUIDs = data["workloadUUIDs"]
            moduleUUIDs = data["moduleUUIDs"]
            lastUpdateLines = data["lastUpdateLines"]
            lastOutputLines = data["lastOutputLines"]
            lastMonitorings = data.get(
                "lastMonitorings"
            )  # we use .get() for params that are not required
            lastPatches = data["lastPatches"]
            response = await IOLoop.current().run_in_executor(
                None,
                optumi.core.pull_module_status_updates,
                workloadUUIDs,
                moduleUUIDs,
                lastUpdateLines,
                lastOutputLines,
                lastMonitorings,
                lastPatches,
            )
            self.write(response.content)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while pulling module status update"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class ListFilesHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.list_files
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"message": "Encountered error while listing files"}))
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class DeleteFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            hashes = data["hashes"]
            paths = data["paths"]
            creationTimes = data["creationTimes"]
            directory = data["directory"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.delete_files, hashes, paths, creationTimes, directory
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"message": "Encountered error while listing files"}))
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class CancelProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            key = data["key"]
            IOLoop.current().run_in_executor(None, optumi.core.cancel_progress, key)
            self.write(json.dumps({"message": "success"}))
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while canceling uploading files"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class UploadFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            key = data["key"]
            paths = [optumi.utils.normalize_path(path) for path in data["paths"]]
            compress = data["compress"]
            storageTotal = data["storageTotal"]
            storageLimit = data["storageLimit"]
            autoAddOnsEnabled = data["autoAddOnsEnabled"]
            IOLoop.current().run_in_executor(
                None,
                optumi.core.upload_files,
                key,
                paths,
                compress,
                storageTotal,
                storageLimit,
                autoAddOnsEnabled,
            )
            self.write(json.dumps({"message": "success"}))
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while uploading files"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class DownloadFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            key = data["key"]
            hashes = data["hashes"]
            paths = data["paths"]
            sizes = data["sizes"]
            overwrite = data["overwrite"]
            directory = data.get(
                "directory"
            )  # We use .get() for values that might be null
            response = await IOLoop.current().run_in_executor(
                None,
                optumi.core.download_files,
                key,
                hashes,
                paths,
                sizes,
                overwrite,
                directory,
            )
            # We only expect a response if something went wrong
            if response != None:
                raise response
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while saving notebook output file"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetNotebookOutputFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workloadUUID = data["workloadUUID"]
            moduleUUID = data["moduleUUID"]
            key = data["key"]
            paths = data["paths"]
            sizes = data["sizes"]
            overwrite = data["overwrite"]
            directory = data.get(
                "directory"
            )  # We use .get() for values that might be null
            response = await IOLoop.current().run_in_executor(
                None,
                optumi.core.get_notebook_output_files,
                workloadUUID,
                moduleUUID,
                key,
                paths,
                sizes,
                overwrite,
                directory,
            )
            # We only expect a response if something went wrong
            if response != None:
                raise response
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while saving notebook output file"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetDownloadProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            keys = data["keys"]
            json_map = await IOLoop.current().run_in_executor(
                None, optumi.core.get_download_progress, keys
            )
            if json_map == {}:
                self.set_status(204)  # No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting download progress"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetBalanceHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            startTime = data["startTime"]
            endTime = data["endTime"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_balance, startTime, endTime
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while getting total billing"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetDetailedBillingHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            startTime = data["startTime"]
            endTime = data["endTime"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_detailed_billing, startTime, endTime
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while getting total billing"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class DeleteMachineHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data["uuid"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.delete_machine, uuid
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while deleting machine"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class CreatePortalHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            redirect = data["redirect"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.create_portal, redirect
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while creating portal"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class CreateCheckoutHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            items = data["items"]
            redirect = data["redirect"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.create_checkout, items, redirect
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while creating checkout"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class CancelSubscriptionHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.cancel_subscription
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while canceling subscription"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class GetConnectionTokenHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            forceNew = data["forceNew"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.get_connection_token, forceNew
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps(
                    {"message": "Encountered error while getting connection token"}
                )
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class RedeemSignupCodeHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            signupCode = data["signupCode"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.redeem_signup_code, signupCode
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while redeeming signup code"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class SendVerificationCodeHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            phoneNumber = data["phoneNumber"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.send_verification_code, phoneNumber
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while sending signup code"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class CheckVerificationCodeHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            code = data["code"]
            phoneNumber = data["phoneNumber"]
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.check_verification_code, phoneNumber, code
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while checking signup code"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class ClearPhoneNumberHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(
                None, optumi.core.clear_phone_number
            )
            self.write(response.text)
            if response.status_code >= 300:
                jupyter_log.info(
                    optumi.logging.optumi_format_and_log(self, str(response))
                )
        except (ConnectionError, URLError, NotLoggedInException) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({"message": str(e)}))
            jupyter_log.warning(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e
        except Exception as e:
            self.set_status(500)
            self.write(
                json.dumps({"message": "Encountered error while clearing_phone_number"})
            )
            jupyter_log.error(optumi.logging.optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


def setup_handlers(server_app):
    global jupyter_token
    global jupyter_log

    jupyter_token = server_app.token

    jupyter_log = server_app.log

    if dev_version:
        jupyter_log.info(
            optumi.logging.optumi_format_and_log(None, "Optumi extension started")
        )
    else:
        optumi.logging.optumi_format_and_log(None, "Optumi extension started")

    web_app = server_app.web_app
    base_url = web_app.settings["base_url"]

    optumi.core.update_path(web_app.settings["server_root_dir"])

    host_pattern = ".*$"
    web_app.add_handlers(
        host_pattern,
        [
            (url_path_join(base_url, "/optumi/version"), VersionHandler),
            (url_path_join(base_url, "/optumi/get-agreement"), GetAgreementHandler),
            (url_path_join(base_url, "/optumi/login"), LoginHandler),
            (url_path_join(base_url, "/optumi/check-login"), CheckLoginHandler),
            (url_path_join(base_url, "/optumi/oauth-callback"), OauthCallbackHandler),
            (url_path_join(base_url, "/optumi/oauth-login"), OauthLoginHandler),
            (url_path_join(base_url, "/optumi/sign-agreement"), SignAgreementHandler),
            (
                url_path_join(base_url, "/optumi/get-user-information"),
                GetUserInformationHandler,
            ),
            (
                url_path_join(base_url, "/optumi/set-user-information"),
                SetUserInformationHandler,
            ),
            (url_path_join(base_url, "/optumi/logout"), LogoutHandler),
            (
                url_path_join(base_url, "/optumi/preview-notebook"),  # preview-workload
                PreviewNotebookHandler,
            ),
            (
                url_path_join(base_url, "/optumi/setup-notebook"),
                SetupNotebookHandler,
            ),  # setup-workload
            (
                url_path_join(base_url, "/optumi/launch-notebook"),
                LaunchNotebookHandler,
            ),  # launch-workload
            (
                url_path_join(base_url, "/optumi/get-login-progress"),
                GetLoginProgressHandler,
            ),
            (
                url_path_join(base_url, "/optumi/get-launch-status"),
                GetLaunchStatusHandler,
            ),
            (
                url_path_join(base_url, "/optumi/get-compression-progress"),
                GetCompressionProgressHandler,
            ),
            (
                url_path_join(base_url, "/optumi/get-upload-progress"),
                GetUploadProgressHandler,
            ),
            (
                url_path_join(base_url, "/optumi/stop-notebook"),
                StopNotebookHandler,
            ),  # stop-workload
            (
                url_path_join(base_url, "/optumi/teardown-notebook"),  # remove-workload
                TeardownNotebookHandler,
            ),
            (url_path_join(base_url, "/optumi/get-machines"), GetMachinesHandler),
            (url_path_join(base_url, "/optumi/get-workloads"), GetWorkloadsHandler),
            (
                url_path_join(base_url, "/optumi/get-notebook-config"),
                GetNotebookConfigHandler,
            ),
            (
                url_path_join(base_url, "/optumi/set-notebook-config"),
                SetNotebookConfigHandler,
            ),
            (
                url_path_join(base_url, "/optumi/pull-package-update"),
                PullPackageUpdateHandler,
            ),
            (
                url_path_join(base_url, "/optumi/push-package-update"),
                PushPackageUpdateHandler,
            ),
            (
                url_path_join(base_url, "/optumi/get-integrations"),
                GetIntegrationsHandler,
            ),
            (url_path_join(base_url, "/optumi/add-integration"), AddIntegrationHandler),
            (
                url_path_join(base_url, "/optumi/rename-integration"),
                RenameIntegrationHandler,
            ),
            (
                url_path_join(base_url, "/optumi/remove-integration"),
                RemoveIntegrationHandler,
            ),
            (
                url_path_join(base_url, "/optumi/push-workload-initializing-update"),
                PushWorkloadInitializingUpdateHandler,
            ),
            (
                url_path_join(base_url, "/optumi/pull-workload-status-updates"),
                PullWorkloadStatusUpdatesHandler,
            ),
            (
                url_path_join(base_url, "/optumi/pull-workload-config"),
                PullWorkloadConfigHandler,
            ),
            (
                url_path_join(base_url, "/optumi/push-workload-config"),
                PushWorkloadConfigHandler,
            ),
            (
                url_path_join(base_url, "/optumi/pull-module-status-updates"),
                PullModuleStatusUpdateHandler,
            ),
            (url_path_join(base_url, "/optumi/upload-files"), UploadFilesHandler),
            (url_path_join(base_url, "/optumi/cancel-progress"), CancelProgressHandler),
            (
                url_path_join(base_url, "/optumi/delete-files"),
                DeleteFilesHandler,
            ),  # remove-files
            (url_path_join(base_url, "/optumi/list-files"), ListFilesHandler),
            (url_path_join(base_url, "/optumi/download-files"), DownloadFilesHandler),
            (
                url_path_join(base_url, "/optumi/get-notebook-output-files"),
                GetNotebookOutputFilesHandler,
            ),
            (
                url_path_join(base_url, "/optumi/get-download-progress"),
                GetDownloadProgressHandler,
            ),
            (url_path_join(base_url, "/optumi/get-balance"), GetBalanceHandler),
            (
                url_path_join(base_url, "/optumi/get-detailed-billing"),
                GetDetailedBillingHandler,
            ),
            (
                url_path_join(base_url, "/optumi/delete-machine"),
                DeleteMachineHandler,
            ),  # release-machine
            (url_path_join(base_url, "/optumi/create-portal"), CreatePortalHandler),
            (url_path_join(base_url, "/optumi/create-checkout"), CreateCheckoutHandler),
            (
                url_path_join(base_url, "/optumi/cancel-subscription"),
                CancelSubscriptionHandler,
            ),
            (
                url_path_join(base_url, "/optumi/get-connection-token"),
                GetConnectionTokenHandler,
            ),
            (
                url_path_join(base_url, "/optumi/redeem-signup-code"),
                RedeemSignupCodeHandler,
            ),
            (
                url_path_join(base_url, "/optumi/send-verification-code"),
                SendVerificationCodeHandler,
            ),
            (
                url_path_join(base_url, "/optumi/check-verification-code"),
                CheckVerificationCodeHandler,
            ),
            (
                url_path_join(base_url, "/optumi/clear-phone-number"),
                ClearPhoneNumberHandler,
            ),
        ],
    )
