from Crypto.Util.Padding import unpad, pad
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

class _ReplaceCharAt:
    def __init__(self, *args) -> None:
        string1, string2, string3 = args
        string2 = int(string2)
        self._result = string1[0:string2] + string3 + string1[string2 + len(string3):]

    def __str__(self) -> str:
        return self._result

class _Secret:
    def __init__(self, string: str) -> None:
        string1 = string[0:8]
        string2 = ''.join([string[16:24], string1, string[24:32], string[8:16]])
        for i in range(32):
            if i == 32:
                break
            if string2[i] >= '0' and string2[i] <= '9':
                char = chr((ord(string2[i][0]) - ord('0') + 5) % 10 + ord('0'))
                string2 = _ReplaceCharAt(string2, i, char)._result
            else:
                char = chr((ord(string2[i][0]) - ord('a') + 9) % 26 + ord('a'))
                string2 = _ReplaceCharAt(string2, i, char)._result
        self._result = string2

    def __str__(self) -> str:
        return self._result

class Crypto:
    def __init__(self, key: str) -> None:
        self.__key = bytearray(_Secret(key)._result, encoding='UTF-8')
        self.__iv = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def encrypt(self, string: str) -> str:
        return b64encode(
            AES.new(self.__key, 2, self.__iv).encrypt(pad(string.encode('UTF-8'), 16))
        ).decode('UTF-8')

    def decrypt(self, string: str) -> str:
        return unpad(AES.new(self.__key, 2, self.__iv).decrypt(b64decode(string.encode('UTF-8'))), 16).decode('UTF-8')