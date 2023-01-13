from enum import Enum

class sandbox_srv(Enum):
    host = "103.186.30.211";username = "ubuntu";port = 22
    privatekey = "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"

class sandbox_telegram(Enum):
    apiToken = '5185237177:AAEk7zIbz8kGaxOGDjippGFrcI7gVc88AUE'
    chatID = '1585168334'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

class sandbox_evernote(Enum):
    dev_token = "S=s1:U=96d22:E=18c96faefc8:C=1853f49c3c8:P=1cd:A=en-devtoken:V=2:H=ca2043a91654f81f91e1470ceddbe37c"
    notestore_url = "https://sandbox.evernote.com/shard/s1/notestore" 
    # expires : 23 December 2023, 06:01

class sandbox_airtable(Enum):
    base_id = 'appWS0BciG06ueMxR'
    api_key = 'keySm6amfV0UJ3F6n'
    table_name = 'PROJECTS'

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class production_srv(Enum):
    host = "103.186.30.211";username = "ubuntu";port = 22
    privatekey = "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"

class production_telegram(Enum):
    apiToken = '5185237177:AAEk7zIbz8kGaxOGDjippGFrcI7gVc88AUE'
    chatID = '1585168334'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

class production_evernote(Enum):
    dev_token = "S=s1:U=96d46:E=18d00c2add8:C=185a91181d8:P=1cd:A=en-devtoken:V=2:H=b22335f090732d928e5cda1d35f0bf4c"
    notestore_url = "https://sandbox.evernote.com/shard/s1/notestore"
    # expires : 12 January 2024, 18:59
class production_airtable(Enum):
    base_id = 'app0wbnpAs2sfs7HD'
    api_key = 'keyCRu6OEi7Xaxq3m'
    table_name = 'MPS'

