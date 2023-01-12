from methods import get_keys, getIP, create_key, login, revoke

class GenerateToken:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def getKey(self):
        login_session = login(self.email, self.password)

        if not login_session:
            return 'Incorrect Email or Password'

        ip = getIP()

        keys = get_keys()

        if len(keys) == 0:
            create = create_key(ip)
            return create

        for key in keys:
            if not key['cidrRanges'][0] == ip:
                delete = revoke(key['id'])

        if keys[0]['cidrRanges'][0] == ip:
            return keys[0]['key']




