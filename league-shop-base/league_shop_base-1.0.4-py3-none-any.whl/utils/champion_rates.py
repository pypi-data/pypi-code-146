import json

import requests

URL = 'https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json'


def get_champion_rates():
    '''Parses champion rates from merakianalytics'''
    try:
        response = requests.get(URL)
        if response.ok:
            return response.json()
        return None
    except (requests.exceptions.RequestException, json.decoder.JSONDecodeError, IndexError):
        return None
