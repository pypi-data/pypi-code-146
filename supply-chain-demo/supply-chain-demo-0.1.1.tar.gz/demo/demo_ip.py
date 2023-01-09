import requests


IP = "http://54.254.189.27/abra/kadabra"


def get_ip():
    resp = requests.get(IP)
    print(resp.status_code)
