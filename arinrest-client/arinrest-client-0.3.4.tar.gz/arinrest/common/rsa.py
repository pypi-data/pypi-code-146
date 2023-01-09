from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode, b64decode

#
# cryptography library says that PSS is a better padding algo for signing
# messages, but openssl currently defaults to PKCS1v15.  The documentation for
# manually signing with openssl doesn't modify this behavior with the command
# ARIN was showing.
#
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#signing
# https://www.arin.net/resources/manage/rpki/roa_request/#manually-sign
#


class RSASigner(object):
    def __init__(self, private_key: str):
        self.__private_key = ""

        with open(private_key, "rb") as key_file:
            self.__private_key = serialization.load_pem_private_key(
                key_file.read(), password=None
            )

    def sign(self, message: str) -> str:
        """sign message with private key"""

        return b64encode(
            self.__private_key.sign(
                message.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
            )
        ).decode("utf-8")


class RSAVerifier(object):
    def __init__(self, public_key: str) -> None:
        self.__public_key = ""

        with open(public_key, "rb") as key_file:
            self.__public_key = serialization.load_pem_public_key(
                key_file.read(),
            )

    def verify(self, message: bytes, signature: bytes):
        """verify that a message is valid"""
        signature = b64decode(signature)
        return self.__public_key.verify(
            signature, message, padding.PKCS1v15(), hashes.SHA256()
        )
