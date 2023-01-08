import json
from requests import get
from bs4 import BeautifulSoup


URL = 'https://filechan.org/'
API_INFO_URL = 'https://api.filechan.org/v2/file'


def fetch_url(url: str) -> str:
    """
    fetch_url : This Function returns the direct file's url from filechan's vaild url

    Args:
        url (str): FileChan Url

        usage : fetch_url("https://filechan.org/89odGaQdy1")

    Returns :

        (str)
    """
    html_file = get(url=url).content
    download_url = BeautifulSoup(html_file, "html.parser").find_all(
        class_="btn btn-primary btn-block")[0].parent.find("a")["href"]
    return download_url


class url_info():
    """
    url_info : A class that gives all information about the url passed on.

    usage :

    obj = url_info("https://filechan.org/89odGaQdy1")

    obj.file_name - (str) returns name of the file uploaded

    obj.file_size - (str) returns size of the file uploaded

    obj.file_bytes - (int) returns size of the file in bytes

    obj.file_id - (str) returns  file id of the file

    obj.full_url - (str) returns full url of the file

    obj.short_url- (str) returns short url of the file
    """

    def __init__(self, url: str):
        self.available_info = ("file_name", "file_size",
                               "file_bytes", "file_id", "full_url", "short_url")
        self.fetch_info(url)

    def fetch_info(self, url: str):
        req_url = API_INFO_URL+"/" + url.replace(URL, "") + "/info"
        data = get(url=req_url).json()
        if data["status"] == True:
            self.file_size = data["data"]["file"]["metadata"]["size"]["readable"]
            self.file_name = data["data"]["file"]["metadata"]["name"]
            self.file_bytes = data["data"]["file"]["metadata"]["size"]["bytes"]
            self.file_id = data["data"]["file"]["metadata"]["id"]
            self.short_url = data["data"]["file"]["url"]["short"]
            self.full_url = data["data"]["file"]["url"]["full"]
            self.direct_url = fetch_url(url=url)
