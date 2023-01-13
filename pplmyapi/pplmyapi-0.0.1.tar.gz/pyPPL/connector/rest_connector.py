import logging
import requests
import requests.adapters

from pyPPL.models import Package
from .rest_actions.get_labels import RESTActionGetLabels

from pyPPL.conf import (LabelReturnChanel, LabelSettingModel, )

from base64 import b64decode

import os

from pyPPL.conf import (
    REST_OAUTH2_TOKEN_URL,
    REST_GRANT_TYPE,
    # REST_CLIENT_ID,
    # REST_CLIENT_SECRET,
)

logger = logging.getLogger(__name__)

class RESTConnector:
    TOKEN_URL = REST_OAUTH2_TOKEN_URL
    GRANT_TYPE = REST_GRANT_TYPE
    client_id = None
    client_secret = None
    
    ACCESS_TOKEN = None

    def __init__(
        self,
        client_id: str,
        client_secret: str,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.get_access_token()
        


    def get_access_token(self):
        if self.ACCESS_TOKEN is not None:
            return self.ACCESS_TOKEN
        response = requests.post(
            self.TOKEN_URL,
            data = {
                'grant_type': self.GRANT_TYPE,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'myapi2',
            }
        )
        if response.status_code != 200:
            return None
        self.ACCESS_TOKEN = response.json()['access_token']
        
        if self.session is not None:
            self.session.headers.update({'Authorization': f'Bearer {self.ACCESS_TOKEN}'})
        return self.ACCESS_TOKEN


    def call():
        pass


    """
    REST methods
    """
    
    def get_labels(self, 
        packages: list[Package] = [], 
        return_chanel_type: LabelReturnChanel = LabelReturnChanel.HTTP,
        return_chanel_address: str = None,
        return_chanel_format: LabelSettingModel = LabelSettingModel.PDF,
        return_chanel_dpi: int = 300,
        file_path = None,
        file_name = None
    ) -> dict:
        """
        Get labels for packages
        :param packages: list of packages
        :param return_chanel_type: return chanel type
        :param return_chanel_address: return chanel address
        :param return_chanel_format: return chanel format
        :param return_chanel_dpi: return chanel dpi (300-1200)
        """

        if not packages or len(packages) == 0:
            raise Exception('No packages provided')

        # get labels for packages - call api
        
        get_labels = RESTActionGetLabels(
            token = self.get_access_token(),
            packages = packages,
            return_chanel_type = return_chanel_type,
            return_chanel_address = return_chanel_address,
            return_chanel_format = return_chanel_format,
            return_chanel_dpi = return_chanel_dpi,
            session = self.session,
        )
        
        response = get_labels()

        if file_path and file_name and return_chanel_type == LabelReturnChanel.HTTP:
            # Base64 to PDF: https://base64.guru/developers/python/examples/decode-pdf
            
            # Create a file path if it does not exist
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            
            out_path = os.path.join(file_path, file_name)

            b64 = response['labels'][0]
            bytes = b64decode(b64, validate=True)

            # Perform a basic validation to make sure that the result is a valid PDF file
            # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
            # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
            if bytes[0:4] != b'%PDF':
                raise ValueError('Missing the PDF file signature')

            # Write the PDF contents to a local file
            f = open(out_path, 'wb')
            f.write(bytes)
            f.close()

        return response
