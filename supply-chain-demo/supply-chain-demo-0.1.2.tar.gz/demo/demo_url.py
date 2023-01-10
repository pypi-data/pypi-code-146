import requests


URL = "https://www.xvira-malwareavrad.com/test"


def get_url():
    resp = requests.get(URL)
    print(resp.status_code)
