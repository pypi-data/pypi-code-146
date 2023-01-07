import hmac
import string
import secrets

alphabet = string.ascii_letters + string.digits

version = '1.0.0'
author = 'Pigeon Nation'

def new_salty_hmac(msg, key, salt, digestmod):
    msg, key, salt = msg.encode(), key.encode(), salt.encode()
    binded = msg + salt
    hm = hmac.new(key, binded, digestmod).hexdigest()
    return hm + ':' + salt.decode()

def verify_salty_hmac(mac, msg, key, digestmod):
    amsg = msg
    msg = mac
    act, salt = msg.split(':')
    wouldbe = new_salty_hmac(amsg, key, salt, digestmod)
    return hmac.compare_digest(msg, wouldbe)

def new_salt(length=16):
    password = ''.join(secrets.choice(alphabet) for i in range(length))

def test():
    msg = 'Hello, world!'
    key = 'Hello, world! is the classic way to start in a new programming language.'
    slt = 'Some SALT..........'
    dmd = 'sha256'
    mac = new_salty_hmac(msg, key, slt, dmd)
    print(verify_salty_hmac(mac, msg, key, dmd))
    
    