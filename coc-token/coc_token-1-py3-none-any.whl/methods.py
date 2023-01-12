import requests
s = requests.Session()

def getIP():
    data = requests.get('https://myexternalip.com/raw')
    return data.text

def login(email, password):
    payload = {
        'email':email,
        'password':password
    }
    response = s.post('https://developer.clashofclans.com/api/login', json=payload).json()
    if response['status']['message'] == 'ok':
        return True
    return False
    

def get_keys():
    response = s.post('https://developer.clashofclans.com/api/apikey/list').json()
    if response['status']['message'] == 'ok':
        return response['keys']
    return False

def create_key(ip):
    payload = {
        'name':'self',
        'description':ip,
        'cidrRanges':ip
    }
    response = s.post('https://developer.clashofclans.com/api/apikey/create', json=payload).json()
    if response['status']['message'] == 'ok':
        return response['key']['key']
    return False

def revoke(id):
    payload = {
        'id':id
    }
    response = s.post('https://developer.clashofclans.com/api/apikey/revoke', json=payload).json()
    if response['status']['message'] == 'ok':
        return True
    return False