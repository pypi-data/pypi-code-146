from .connector import (SOAPConnector, RESTConnector)
from .conf import (
    SOAP_AUTH_TOKEN_MAX_AGE,
)

class PPL:
    """
    PPL API wrapper
    * defines both soap and rest connectors
    """

    soap_connector_instance: SOAPConnector = None
    rest_connector_instance: RESTConnector = None

    def __init__(
        self,
        rest_client_id: str = None,
        rest_client_secret: str = None,
        soap_customer_id: str = None,
        soap_password: str = None,
        soap_username: str = None,
        soap_auth_token_max_age: int = SOAP_AUTH_TOKEN_MAX_AGE,
    ) -> None:
        """
        Initialize PPL API wrapper
        * both soap and rest connectors are initialized
        * obtain all credentials and pass them to the connectors
        """
        if(soap_customer_id is not None and soap_password is not None and soap_username is not None):
            self.soap_connector_instance = SOAPConnector(
                cust_id=soap_customer_id,
                password=soap_password,
                username=soap_username,
                auth_token_max_age=soap_auth_token_max_age,
            )

        if(rest_client_id is not None and rest_client_secret is not None):
            self.rest_connector_instance = RESTConnector(
                client_id=rest_client_id,
                client_secret=rest_client_secret,
            )

    def soap_connector(self) -> SOAPConnector:
        if self.soap_connector_instance is None:
            raise Exception('SOAP connector not initialized, please provide soap credentials')
        return self.soap_connector_instance
    
    def rest_connector(self) -> RESTConnector:
        if self.rest_connector_instance is None:
            raise Exception('REST connector not initialized, please provide rest credentials')
        return self.rest_connector_instance
