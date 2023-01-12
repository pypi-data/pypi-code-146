import requests
from lxml import etree, html
from urllib.request import urlopen
from bs4 import BeautifulSoup 
from omletApi.errors import *
from omletApi.timeout import Timeout

class omlet_arcade_api_public:

    def __init__(self, username=None):

        self.username = username
        self.r = requests.get("https://omlet.gg/profile/{0}".format(self.username))

        if (self.r.status_code != 200):
            raise UsernameError("{0} not found".format(self.username))
        else:
            self.soup = BeautifulSoup(self.r.text, "lxml")

            self.htmlparser = html.fromstring(self.r.content) 

    def get_description(self):

        desc = self.soup.find("meta", property="og:description")
        self.description = desc.get("content")

    def get_profile_image(self):

        url = self.soup.find("meta", property="og:image")
        self.url = url.get("content")    

    def get_omlet_icon(self):

        self.icon32 = "https://omlet.gg/arcade-favicon-32x32.png"
        self.icon64 = "https://omlet.gg/arcade-favicon-64x64.png"

    def get_stream_image(self):

        self.stream_url = "https://omlet.gg/stream/{0}/picture.jpg".format(self.username)

    def get_followers_count(self):
        
        response = requests.get(f"https://omapi.ru/api/user/getFollowersCount?username={self.username}&token=default")
        json_load = response.json()

        self.followers = json_load["result"]

    def get_follows_count(self):
        
        response = requests.get(f"https://omapi.ru/api/user/getFollowsCount?username={self.username}&token=default")
        json_load = response.json()

        self.followers = json_load["result"]

    def get_avatar(self):
        
        response = requests.get(f"https://omapi.ru/api/user/getAvatar?username={self.username}&token=default")
        json_load = response.json()

        self.avatar = json_load["result"]

    def get_level(self):
        
        response = requests.get(f"https://omapi.ru/api/user/getLevel?username={self.username}&token=default")
        json_load = response.json()

        self.level = json_load["result"]

    def is_verified(self):
        
        response = requests.get(f"https://omapi.ru/api/user/isVerified?username={self.username}&token=default")
        json_load = response.json()

        self.verified = json_load["result"]

    def is_live(self):
        
        response = requests.get(f"https://omapi.ru/api/user/isLive?username={self.username}&token=default")
        json_load = response.json()

        self.live = json_load["result"]

    def get_stream_hotness(self):
        
        response = requests.get(f"https://omapi.ru/api/user/getStreamHotness?username={self.username}&token=default")
        json_load = response.json()

        self.hotness = json_load["result"]

class omlet_arcade_api_private:

    def __init__(self, username, token=None):

        if (token is None):
            raise TokenNotFound("type token")
        else:
            self.username = username
            self.token = token

        self.r = requests.get("https://omlet.gg/profile/{0}".format(self.username))

        if (self.r.status_code != 200):
            raise UsernameError("{0} not found".format(self.username))
        else:
            pass

    def get_follows_list(self):

        response = requests.get(f"https://omapi.ru/api/user/getFollowsList?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.follows_list = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

    def get_followers_list(self):

        response = requests.get(f"https://omapi.ru/api/user/getFollowersList?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.followers_list = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

    def is_has_omlet_creator(self):

        response = requests.get(f"https://omapi.ru/api/user/isHasOmletCreator?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.omlet_creator = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

    def is_has_omlet_plus(self):

        response = requests.get(f"https://omapi.ru/api/user/isHasOmletPlus?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.omlet_plus = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

    def get_gtream_viewers(self):

        response = requests.get(f"https://omapi.ru/api/user/getStreamViewers?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.stream_viewers = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

    def get_stream_viewers_list(self):

        response = requests.get(f"https://omapi.ru/api/user/getStreamViewersList?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.stream_viewers_list = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

    def get_gtream_viewers(self):

        response = requests.get(f"https://omapi.ru/api/user/getStreamViewers?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.stream_viewers = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

    def get_gtream_viewers(self):

        response = requests.get(f"https://omapi.ru/api/user/getStreamViewers?username={self.username}&token={self.token}")
        json_load = response.json()

        try:
            self.stream_viewers = json_load["result"]
        except:
            raise TokenNotFound("invalid token")

   