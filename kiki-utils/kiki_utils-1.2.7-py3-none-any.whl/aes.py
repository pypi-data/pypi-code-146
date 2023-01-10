from binascii import a2b_hex
from Cryptodome.Cipher.AES import block_size, MODE_CBC, MODE_CFB, MODE_CTR, MODE_ECB, new
from typing import Union

from .json import odumps, oloads


class AesCrypt:
    """Padding mode is PKCS7 Padding."""

    def __init__(
        self,
        key: Union[bytes, str],
        iv: Union[bytes, str] = None,
        mode=MODE_CBC,
        counter=None
    ):
        if isinstance(key, str):
            key = key.encode()

        if isinstance(iv, str):
            iv = iv.encode()

        if mode == MODE_ECB:
            self._get_aes = lambda: new(key, mode)
        elif mode == MODE_CTR:
            self._get_aes = lambda: new(key, mode, counter=counter)
        else:
            self._get_aes = lambda: new(key, mode, iv)

        if mode == MODE_CFB:
            self._pad = self._rstrip = lambda x: x
        else:
            def _pad(data: bytes):
                n = block_size - (len(data) % block_size)
                return data + (chr(n).encode() * n)

            self._pad = _pad
            self._unpad = lambda x: x[:len(x)-x[-1]]

    @staticmethod
    def _to_bytes(data: Union[bytes, dict, list, str]) -> bytes:
        if isinstance(data, bytes):
            return data

        if isinstance(data, (dict, list)):
            return odumps(data)

        return data.encode('utf-8')

    def decrypt(self, ciphertext: Union[bytes, str]) -> Union[dict, list, str]:
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode('utf-8')

        ciphertext = a2b_hex(ciphertext)
        text: bytes = self._unpad(self._get_aes().decrypt(ciphertext))

        try:
            return oloads(text)
        except:
            return text.decode()

    def encrypt(
        self,
        data: Union[bytes, dict, list, str],
        return_bytes: bool = False
    ):
        encrypted_data = self._get_aes().encrypt(self._pad(self._to_bytes(data)))
        return encrypted_data if return_bytes else encrypted_data.hex()
