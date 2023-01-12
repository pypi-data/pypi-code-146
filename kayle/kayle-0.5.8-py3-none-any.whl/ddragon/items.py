import pprint

from munch import DefaultMunch
import requests
from PIL import Image
from io import BytesIO


class DDragonItem:
    def __init__(self, data, version):
        self.version = version
        self.name = data["name"]
        self.description = data["description"]
        self.colloq = data["colloq"]
        self.plaintext = data["plaintext"]
        if "into" in data:
            self.into = data["into"]
        else:
            self.into = []
        self.image = DefaultMunch.fromDict(data["image"])
        self.gold = DefaultMunch.fromDict(data["gold"])
        self.tags = data["tags"]
        try:
            self.maps = DefaultMunch.fromDict(data["maps"])
        except:
            self.maps = [11]
        self.stats = DefaultMunch.fromDict(data["stats"])

        self._icon = None

    def icon(self):
        if self._icon is not None:
            return self._icon
        r = requests.get("https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}".format(self.version, self.image.full))
        print(r.url)
        self._icon = Image.open(BytesIO(r.content))
        return self._icon
