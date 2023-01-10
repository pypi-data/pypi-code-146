#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, validator
from dateutil.parser import parse


# IFD = InfluxDB_Modeling
def convert_to_unixtime(date):
    # print(f'date : {type(date)}')
    if isinstance(date, float):
        date = str(datetime.fromtimestamp(float(date)))
        # print(date)
    elif isinstance(date, int):
        date = str(date)

    try:
        return datetime.timestamp(parse(date))
    except ValueError as e:
        # print(f'error: {e}')
        if "out of range" in str(e) or 'unknown string format' in str(e).lower():
            return datetime.timestamp(parse(str(datetime.fromtimestamp(float(date)))))
        else:
            err_msg = f'Check input datetime type (input {date} / type is {type(date)})'
            raise err_msg


def convert_string_null(data):
    if isinstance(data, str):
        return data.replace(' ', '_')


class IFDCommon(BaseModel):
    name: str = None
    uuid: str = None
    resource: str = None
    item: str = None
    time: float

    @validator("time", pre=True, always=True)
    def convert_time(cls, value):
        return convert_to_unixtime(value) or datetime.timestamp(datetime.now())


class IFDTags(IFDCommon):
    organization: str = None
    service: str = None
    region: str = None


class IFDResource(IFDCommon):
    dns_time: float = None
    data_time: float = None
    handshake_time: float = None
    data_received_time: float = None
    total_response_time: float = None

    @validator("dns_time", pre=True, always=True)
    def convert_dns_time(cls, value):
        return convert_to_unixtime(value) if value else datetime.timestamp(datetime.now())

    @validator("handshake_time", pre=True, always=True)
    def convert_handshake_time(cls, value):
        return convert_to_unixtime(value) if value else datetime.timestamp(datetime.now())

    @validator("data_time", pre=True, always=True)
    def convert_data_time(cls, value):
        return convert_to_unixtime(value) if value else datetime.timestamp(datetime.now())

    @validator("data_received_time", pre=True, always=True)
    def convert_data_received_time(cls, value):
        return convert_to_unixtime(value) if value else datetime.timestamp(datetime.now())

    @validator("total_response_time", pre=True, always=True)
    def convert_total_response_time(cls, value):
        return convert_to_unixtime(value) if value else datetime.timestamp(datetime.now())


class IFDEvent(IFDCommon):
    message: str = None
    level: str = None


def test_code():
    data_a = {
        'name': 'test_user',
        'uuid': requests.get('http://20.20.6.89:8800/temp/uuid/').text,
        'time': '20220920122150',
        'level': 'debug'
    }

    IFD = IFDEvent(**data_a)
    print(f'1= {IFD.time}')
    print(f'1= {IFD.level}')
    print(f'1= {IFD.name}')
    print(f'1= {IFD.uuid}\n\n')

    data_b = {
        'name': 'test_user',
        'uuid': requests.get('http://20.20.6.89:8800/temp/uuid/').text,
        'time': '1663644110.0',
        'level': 'debug'
    }
    IFD2 = IFDEvent(**data_b)
    print(f'2 = {IFD2.time}')
    print(f'2 = {IFD2.level}')
    print(f'2 = {IFD2.name}')
    print(f'2 = {IFD2.uuid}\n\n')

    data_c = {
        'name': 'test_user',
        'uuid': requests.get('http://20.20.6.89:8800/temp/uuid/').text,
        'time': 1663644110.0,
        'level': 'debug'
    }
    IFD3 = IFDEvent(**data_c)
    print(f'3 = {IFD3.time}')
    print(f'3 = {IFD3.level}')
    print(f'3 = {IFD3.name}')
    print(f'3 = {IFD3.uuid}\n\n')

    data_d = {
        'name': 'test_user',
        'uuid': requests.get('http://20.20.6.89:8800/temp/uuid/').text,
        'time': 20220920122150,
        'level': 'debus@@Sg'
    }

    IFD4 = IFDEvent(**data_d)
    print(f'4 = {IFD4.time}')
    print(f'4 = {IFD4.level}')
    print(f'4 = {IFD4.name}')
    print(f'4 = {IFD4.uuid}\n\n')

    data_e = {
        'name': 'test_user',
        'uuid': requests.get('http://20.20.6.89:8800/temp/uuid/').text,
        'time': 1663644110.123333,
        'total_response_time': '202209201604'
    }

    IFD5 = IFDResource(**data_e)
    print(f'5 = {IFD5.time}')
    print(f'5 = {IFD5.name}')
    print(f'5.total_response_time = {IFD5.total_response_time}')
    print(f'5.data_time = {IFD5.data_time}')
    print(f'5 = {IFD5.uuid}\n\n')


if __name__ == '__main__':
    test_code()
