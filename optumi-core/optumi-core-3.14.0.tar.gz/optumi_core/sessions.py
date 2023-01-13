##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

from ._version import __version__

from requests import Session
from .exceptions import NotLoggedInException, OptumiException, NoAgreementException


dev_version = "dev" in __version__.lower()

session = None


class CustomSession(Session):
    def request(self, method, url, **kwargs):
        response = super().request(method, url, **kwargs)
        if (not url.endswith("/login")) and response.url.endswith("/login"):
            raise NotLoggedInException()
        if response.status_code >= 400:
            text = response.text
            if text == "User has not signed the Terms & Conditions of Service":
                raise NoAgreementException()
            raise OptumiException(text if (text != None and len(text) > 0) else None)
        return response


def get_session():
    global session
    if session is None:
        session = CustomSession()
        if dev_version:
            print("Creating session")
        return session
    else:
        if dev_version:
            print("Re-using session")
        return session
