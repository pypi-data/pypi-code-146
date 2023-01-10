import json
from robertcommonbasic.basic.encrypt.rsa import *
from robertcommonbasic.basic.encrypt.aes import *
from robertcommonbasic.basic.os.file import file_hash
from robertcommonbasic.basic.file.xml import *


def test_rsa():
    secret = 'robert'
    content = json.dumps({'name': 'hello', 'value': 'world'})
    server_private_pem, server_public_pem, client_private_pem, client_public_pem = generate_rsa_key(secret)
    encrypt_content = rsa_encrypt(client_public_pem, content.encode('utf-8'), secret)
    sign_content = rsa_sign(server_private_pem, content.encode('utf-8'), secret)
    decrypt_content = rsa_decrypt(client_private_pem, encrypt_content.decode('utf-8'), secret)
    assert rsa_verify(server_public_pem, encrypt_content.decode('utf-8'), sign_content.decode('utf-8'), secret) == True


def test_dsa():
    pass


def test_aes_rsa():

    # 随机生成aes的密钥
    aes_key = f'robert20221114'
    content = json.dumps({'name': 'hello', 'value': 'world'})

    # AES加密数据
    encrypt_text = aes_encrypt(content.encode(), aes_key)

    # 生成秘钥对
    server_private_pem, server_public_pem, client_private_pem, client_public_pem = generate_rsa_key(bits=1024)

    # 使用客户端私钥对aes密钥签名
    signature = rsa_sign(client_private_pem, aes_key)

    # 使用服务端公钥加密aes密钥
    encrypt_key = rsa_encrypt(server_public_pem, aes_key)






    # 使用服务端私钥对加密后的aes密钥解密
    _aes_key = rsa_decrypt(server_private_pem, encrypt_key)

    # 使用客户端公钥验签
    result = rsa_verify(client_public_pem, _aes_key, signature)

    # 使用aes私钥解密密文
    decrypt_text = aes_decrypt(encrypt_text, _aes_key).decode()

    print()


def str_hash(content: str):
    from hashlib import sha1
    hash_sha1 = sha1()
    hash_sha1.update(content.encode())
    return hash_sha1.hexdigest()


def test_aes_rsa1():

    content = open(r'E:\Beop\Code\Study\Python\Case\casXML\test1.xml', 'r', encoding='UTF-8').read()
    xml = parse_xml_str_node(content)
    print(xml_node_to_str(xml, encoding='UTF-8') == content)
    aes_key = str_hash(content)

    # AES加密数据
    encrypt_text = aes_encrypt(content.encode(), aes_key)

    # 生成秘钥对
    server_private_pem, server_public_pem, client_private_pem, client_public_pem = generate_rsa_key(bits=1024)

    # 使用客户端私钥对aes密钥签名
    signature = rsa_sign(client_private_pem, aes_key)

    # 使用服务端公钥加密aes密钥
    encrypt_key = rsa_encrypt(server_public_pem, aes_key)

    # 使用服务端私钥对加密后的aes密钥解密
    _aes_key = rsa_decrypt(server_private_pem, encrypt_key)

    # 使用客户端公钥验签
    result = rsa_verify(client_public_pem, _aes_key, signature)

    # 使用aes私钥解密密文
    decrypt_text = aes_decrypt(encrypt_text, _aes_key).decode()


    print()


test_aes_rsa1()