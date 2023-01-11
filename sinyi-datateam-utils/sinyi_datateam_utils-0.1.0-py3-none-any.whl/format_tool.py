import os
from azure.keyvault.secrets import SecretClient
from azure.identity import EnvironmentCredential
from pathlib import Path
import sqlalchemy
from sqlalchemy.engine import URL
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import requests



vault_url = os.environ['AZURE_VAULT_URL']
credential = EnvironmentCredential()
client = SecretClient(vault_url,credential=credential)


def roc_era_to_ad(roc_era):
    roc_era = roc_era.replace('-',"").replace(" ","").replace('_',"")
    if roc_era: 
        if len(roc_era) == 7 :
            year = roc_era[:-4]
            year = str(int(year)+1911)
            return year+roc_era[-4:]
        else:
            return None

class AESCrypto:
    def __init__(self):
        self.key = client.get_secret('AESCrypto-key').value.encode("utf8")
        self.iv =  client.get_secret('AESCrypto-iv').value.encode("utf8")

    def decrypt(self, text:str)-> str:
        # decrypt text
        if text:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

            decryptByts = base64.b64decode(text)
            msg = cipher.decrypt(decryptByts)
            paddingLen = msg[len(msg)-1]
        else:
            return None
        
        return msg[0:-paddingLen].decode('utf8')

    def encrypt(self,text:str):
        cipher = AES.new(self.key, AES.MODE_CBC,self.iv)
        
        text = pad(text.encode('utf-8'), AES.block_size)

        msg = cipher.encrypt(text)
        msg = base64.b64encode(msg)

        return msg.decode('utf8')


class Road8:
    road8_api_key = client.get_secret('road8-api-key').value
    url = client.get_secret('road8-host').value

    @classmethod
    def normalize(cls, address = None):
        address = address.replace('\u3000','')
        normalize_url = cls.url + '/Api/Normalization'
        params = {'key': cls.road8_api_key, 
                'zip': 'zip33', 
                'update': 0,
                'exist': 1,
                'locate':1,
                'addr' : address}
        error_json={
             'source_address': address,
             'standard_address': '',
             'update_address': '',
             'exists_address': '',
             'addrno': 0,
             'location': {'match_type': '無法定位',
                          'crs': 'EPSG:3826',
                          'x': 0,
                          'y': 0,
                          'lat': 0,
                          'lng': 0,
                          'level': 0 }
             }
        success = True
        retry = 0
        while success:
            response = requests.get(normalize_url, params=params)
            if response.status_code != 200 :
                print(response)
                return error_json
            else:
                if 'addrno' not in response.json():
                    assert retry < 5, 'Retry Road8 over 5 times, please contact service provider'
                    print('Error, response: ',response.json(), ', address: ', address)
                    retry += 1
                else:
                    success = False
                    return response.json()