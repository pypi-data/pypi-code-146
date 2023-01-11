#!/usr/bin/env python3
import requests

def is_in_china()->bool:
    """decide if the machine is in china"""
    ipinfo = requests.get('http://ipinfo.io/json').json()
    return ipinfo['country'] == 'CN'

def post_to_lark(webhook_url:str, text:str):
    msg = {'msg_type': 'text', 'content': {'text': text}}
    return requests.post(webhook_url, json=msg)

    