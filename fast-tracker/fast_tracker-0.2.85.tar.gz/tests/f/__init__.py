import logging
import time
import requests


def do_job_a(**kwargs):
    # logging.info("job AAA")
    # logging.info(kwargs)
    print(kwargs)
    requests.get("https://baidu.com")
    requests.get("https://docs.mingyuanyun.com/")
    requests.get("https://baidu.com")
    return True
