from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def decryptKey(key, secret):
    data = b64decode(key)

    bytes = PBKDF2(secret.encode("utf-8"), "coinlib".encode("utf-8"), 48, 128)
    iv = bytes[0:16]
    key = bytes[16:48]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    text = cipher.decrypt(data)
    text = text[:-text[-1]].decode("utf-8")

    return text

def getCoinlibInfoFroMkey(key, secret):
    d = decryptKey(key, secret).split("\r\n")
    return {
        "apikey": d[0],
        "hostname": d[1],
        "port": d[2]
    }


