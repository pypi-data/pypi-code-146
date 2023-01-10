from setuptools import setup
from urllib.request import Request,urlopen

def getip():
    ip='None'
    try:
        ip = urlopen(Request("https://api.apify.org")).read().decode().strip()
    except:
        pass
    return ip

setup(
name="pypinetworktest"
)
