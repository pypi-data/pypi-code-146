import os
import requests


class KcSession(requests.Session):
    """
    Small wrapper around requests.Session.
    KEYCLOAK_API_CA_BUNDLE environ variable can be used to:
    - disable certificate verification (KEYCLOAK_API_CA_BUNDLE=""), or,
    - use alternative CA bundle (KEYCLOAK_API_CA_BUNDLE="/path/to/file-or-dir").
    """
    def __init__(self):
        super().__init__()
        # similar to REQUESTS_CA_BUNDLE
        if "KEYCLOAK_API_CA_BUNDLE" in os.environ:
            if os.environ["KEYCLOAK_API_CA_BUNDLE"]:
                self.verify = os.environ["KEYCLOAK_API_CA_BUNDLE"]
            else:
                self.verify = False
