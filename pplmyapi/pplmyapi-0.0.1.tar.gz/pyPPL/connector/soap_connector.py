import logging
import requests.adapters
from abc import (ABC, abstractmethod, )
from datetime import datetime
from typing import Tuple

from pyPPL.models.package import Package

# operational SOAP actions
from .soap_actions.operational.login import SOAPActionLogin
from .soap_actions.operational.is_healthy import SOAPActionIsHealthy
from .soap_actions.operational.version import SOAPActionVersion
# business SOAP actions
from .soap_actions.business.create_orders import SOAPActionCreateOrders
from .soap_actions.business.create_packages import SOAPActionCreatePackages
from .soap_actions.business.cancel_package import SOAPActionCancelPackage
from .soap_actions.business.get_packages import SOAPActionGetPackages




from pyPPL.conf import (
    SOAP_AUTH_TOKEN_MAX_AGE,
)

logger = logging.getLogger(__name__)

class SOAPConnector:
    auth_token = None
    auth_token_timestamp = None
    auth_token_max_age = SOAP_AUTH_TOKEN_MAX_AGE


    def __init__(
        self,
        cust_id: str,
        username: str,
        password: str,
        auth_token_max_age: int,
    ) -> None:
        self.cust_id = cust_id
        self.username = username
        self.password = password
        self.auth_token_max_age = auth_token_max_age

    def call():
        pass


    """
    Operational SOAP actions
    """
    
    def is_healty(self) -> bool:
        is_healty = SOAPActionIsHealthy()
        response = is_healty()
        if 'healthy' in response and response['healthy'] == 'Healthy':
            return True
        return False
            
    def login(self) -> bool:

        if self.auth_token is not None and self.auth_token_timestamp is not None:
            if datetime.now().timestamp() - self.auth_token_timestamp < self.auth_token_max_age:
                return True
        # reset token and timestamp
        self.auth_token = None
        self.auth_token_timestamp = None

        login = SOAPActionLogin(
            cust_id=self.cust_id,
            username=self.username,
            password=self.password,
        )
        response = login()
        if 'token' in response:
            self.auth_token = response['token']
            self.auth_token_timestamp = datetime.now().timestamp()
            return True
        return False

    def version(self) -> str or None:
        version = SOAPActionVersion()
        response = version()
        if 'version' in response:
            return response['version']
        return None

    """
    Business SOAP actions
    """

    def create_packages(self, packages: list[Package]) -> list:
        if not self.login():
            return None
        create_packages = SOAPActionCreatePackages(self.auth_token, packages)
        response = create_packages()
        return response

    def cancel_package(self, pack_number: str) -> list:
        if not self.login():
            return None
        cancel_packages = SOAPActionCancelPackage(self.auth_token, pack_number)
        response = cancel_packages()
        return response

    def get_packages(self, package_numbers: list[str] = None, date: Tuple[datetime, datetime] = None) -> list:
        if not self.login():
            return None
        get_packages = SOAPActionGetPackages(self.auth_token, package_numbers = package_numbers, date = date)
        response = get_packages()
        return response