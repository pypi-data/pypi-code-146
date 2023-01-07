#!/usr/bin/env python
import binascii
import os
import uuid
from pprint import pprint
from urllib.parse import urlparse
from ipaddress import ip_address
import socket
import typing
from datetime import datetime

from codec.diameter.diameter import Avp, DiameterHeader, Diameter
from codec.diameter.dictionary import DictionaryLayout, DefaultDictionaryLayout


def cer(host, port, xml_dict_path):
    avp_set: typing.Tuple = (
        Avp("Product-Name", "hello"),
        Avp("Origin-Realm", "zte.com.cn"),
        Avp("Origin-Host", "dmtsrv001.zte.com.cn")
    )
    dictionary_layout: DictionaryLayout = DefaultDictionaryLayout(xml_dict_path)
    header: DiameterHeader = DiameterHeader(application_id=0, command_code=257, avp_set=avp_set)
    encoded_message: bytes = Diameter(dictionary_layout).encode(header)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(encoded_message)
        data = s.recv(4096)
        print('Received', repr(data))


def s6b(host, port, xml_dict_path):
    avp_set: typing.Tuple = (
        Avp("Host-IP-Address", '10.114.0.4'),
        Avp("Host-IP-Address", ip_address('10.114.0.4')),
        Avp("Host-IP-Address", 'fde4:2c6e:55c4:105:a00:27ff:fe0b:7859'),
        Avp("Host-IP-Address", ip_address('fde4:2c6e:55c4:105:a00:27ff:fe0b:7859')),
        Avp("Served-Party-IP-Address", ip_address('10.114.0.4')),
        Avp("Served-Party-IP-Address", '10.114.0.4'),

        # https://references.mobileum.com/DiaDict/Dictionary/Framed-IP-Address.html
        # in dictionary should bed defined as type="OctetString" ?
        Avp("Framed-IP-Address", ip_address('10.114.0.4')),
        Avp("Framed-IP-Address", '10.114.0.4'),
        Avp("Framed-IP-Address", 'fde4:2c6e:55c4:105:a00:27ff:fe0b:7859'),
        Avp("Framed-IP-Address", ip_address('fde4:2c6e:55c4:105:a00:27ff:fe0b:7859')),
        Avp("Framed-IP-Address", 'fde4:2c6e:55c4:105:a00:27ff:fe0b:7859'),

        # crash !!!
        # Avp("Framed-Pool", 'pool'),

        Avp("Proxy-State", "proxy"),

        Avp("Event-Timestamp", int(datetime.now().timestamp())),
        Avp("Acct-Session-Id", "test-29091980"),
        Avp("Origin-State-Id", 1),
        Avp("Acct-Multi-Session-Id", str(uuid.uuid4())),
        Avp("Origin-Host", "dmtsrv001.zte.com.cn"),
        Avp("Origin-Realm", "zte.com.cn"),
        Avp("Redirect-Host", urlparse("aaa://host.example.com;transport=tcp")),
        Avp("Redirect-Host-Usage", "ALL_USER"),
        Avp("Redirect-Host-Usage", "UNKNOWN"),
        Avp("Redirect-Host-Usage", ""),
        Avp("Redirect-Host-Usage", None),
        Avp("3GPP-User-Location-Info", '8200f210303900f2100123a30a000000'),
        Avp("3GPP-User-Location-Info", binascii.unhexlify('8200f210303900f2100123a30a000000')),
        Avp("3GPP-User-Location-Info", 0x8200f210303900f2100123a30a000000),
        Avp("Error-Message", ""),
        Avp("WLAN-Identifier",
            (
                Avp("SSID", "etisalat-roam001"),
            )),
        Avp("EPS-Subscribed-QoS-Profile", (
            Avp("Allocation-Retention-Priority", (
                Avp("Priority-Level", 1),
            )),
        )),
    )

    dictionary_layout: DictionaryLayout = DefaultDictionaryLayout(xml_dict_path)
    header: DiameterHeader = DiameterHeader(application_id=16777250,
                                            command_flag_req=True,
                                            command_code=265,
                                            avp_set=avp_set)
    encoded_message: bytes = Diameter(dictionary_layout).encode(header)
    pprint(f'send header={header} to server as encoded_message={encoded_message}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(encoded_message)
        data = s.recv(4096)
        print('Received', repr(data))


def s6a(host, port, xml_dict_path):
    avp_set: typing.Tuple = (
        Avp("Session-Id", "2aed048b06d21aaff155d1454ac6d8de"),
        Avp("Auth-Session-State", "NO_STATE_MAINTAINED"),
        Avp("Origin-Host", "test-u0001-1-1.diamagent.mme.org"),
        Avp("Destination-Host", "enea.diamagent.org"),
        Avp("Origin-Realm", "mme.org"),
        Avp("Destination-Realm", "diamagent.org"),
        Avp("User-Name", "21910000000011"),
        Avp("Auth-Application-Id", 16777251),
        # Avp("Visited-PLMN-Id", int.from_bytes(EncodePLMN("310", "410"), byteorder="big")),
        # Avp("Visited-PLMN-Id", 1242128)
        # Avp("Visited-PLMN-Id", 1306625),
        Avp("Visited-PLMN-Id", 1245204),
        # Avp("Visited-PLMN-Id", Avp.PLMN(310, 410)),
        #   Avp("Visited-PLMN-Id", 5399),
        Avp("Requested-EUTRAN-Authentication-Info", (
            Avp("Number-Of-Requested-Vectors", 1),
        )),
        Avp("Origin-State-Id", 33818),
    )

    dictionary_layout: DictionaryLayout = DefaultDictionaryLayout(xml_dict_path)
    header: DiameterHeader = DiameterHeader(application_id=16777251,
                                            command_flag_req=True,
                                            command_code=318,
                                            avp_set=avp_set)
    encoded_message: bytes = Diameter(dictionary_layout).encode(header)
    pprint(f'send header={header} to server as encoded_message={encoded_message}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(encoded_message)
        data = s.recv(4096)
        print('Received', repr(data))


def client():
    host = '127.0.0.1'
    port = 3868
    print(os.getcwd())
    xml_dict_path: str = f'{os.getcwd()}/../../../src/unittest/python/Diameter.xml'
    #   cer(host, port, xml_dict_path)
    s6b(host, port, xml_dict_path)
    # s6a(host, port, xml_dict_path)


if __name__ == "__main__":
    client()
