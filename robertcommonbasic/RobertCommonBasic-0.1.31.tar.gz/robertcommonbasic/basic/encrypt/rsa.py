
from base64 import b64encode, b64decode
from Cryptodome.Hash import SHA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Cryptodome.PublicKey import RSA

from typing import Optional, Union


# 生成密钥对
def generate_rsa_key(secret: Optional[str] = None, bits: int = 4096, pcks: int = 8, protection: str = 'scryptAndAES128-CBC') -> tuple:
    key_pair = RSA.generate(bits)
    server_private_pem = key_pair.exportKey(passphrase=secret, pkcs=pcks, protection=protection)
    server_public_pem = key_pair.publickey().exportKey(passphrase=secret, pkcs=pcks, protection=protection)
    client_private_pem = key_pair.exportKey(passphrase=secret, pkcs=pcks, protection=protection)
    client_public_pem = key_pair.publickey().exportKey(passphrase=secret, pkcs=pcks, protection=protection)
    return server_private_pem, server_public_pem, client_private_pem, client_public_pem


# rsa加密
def rsa_encrypt(client_public_pem: bytes, content: Union[bytes, str], secret: Optional[str] = None) -> bytes:
    if isinstance(content, str):
        content = content.encode('utf-8')
    return b64encode(PKCS1_OAEP.new(RSA.importKey(client_public_pem, passphrase=secret)).encrypt(content))


# rsa签名
def rsa_sign(server_private_pem: bytes, content: Union[bytes, str], secret: Optional[str] = None) -> bytes:
    if isinstance(content, str):
        content = content.encode('utf-8')

    signer = Signature_pkcs1_v1_5.new(RSA.importKey(server_private_pem, passphrase=secret))
    digest = SHA.new()
    digest.update(content)
    sign = signer.sign(digest)
    return b64encode(sign)  # 签名


# rsa解密
def rsa_decrypt(client_private_pem: str, encrypt_content: Union[bytes, str], secret: Optional[str] = None):
    if isinstance(encrypt_content, str):
        encrypt_content = encrypt_content.encode('utf-8')
    cipher = PKCS1_OAEP.new(RSA.importKey(client_private_pem, passphrase=secret))
    return cipher.decrypt(b64decode(encrypt_content)).decode('utf-8')  # 加密后的内容


# rsa验签
def rsa_verify(server_public_pem: str, decrypt_content: Union[bytes, str], sign_content: Union[bytes, str], secret: Optional[str] = None):
    if isinstance(decrypt_content, str):
        decrypt_content = decrypt_content.encode('utf-8')
    if isinstance(sign_content, str):
        sign_content = sign_content.encode('utf-8')
    verifier = Signature_pkcs1_v1_5.new(RSA.importKey(server_public_pem, passphrase=secret))
    digest = SHA.new()
    digest.update(decrypt_content)
    return verifier.verify(digest, b64decode(sign_content))
