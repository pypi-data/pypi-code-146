import requests
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from pathlib import Path
import sys
import time
import click
import statistics
requests.packages.urllib3.disable_warnings()
config = ConfigParser()
config.read(str(Path.home() / ".dockyard.ini"))
cookie = config.get("default","cookie", fallback=None)
if cookie == None:
    print("please login using `dcli login` first")
    sys.exit(-1)

def get_url(url):
    start = time.time()
    r = requests.get(url + "/api/ds/me", cookies={"_oauth2_proxy": cookie}, verify=False)
    return time.time() - start

@click.command()
@click.argument("times", type=int)
@click.argument("workers", type=int)
def check_latency(times, workers):
    url = config.get("default","url") 
    list_of_urls = [url]* times
    with ThreadPoolExecutor(max_workers=workers) as pool:
        response_list = list(pool.map(get_url,list_of_urls))

    print(min(response_list))
    print(max(response_list))
    print(statistics.mean(response_list))
    print(statistics.median(response_list))


if __name__ == "__main__":
    check_latency()