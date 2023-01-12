import pprint

import requests
from PIL import Image
from io import BytesIO
from munch import DefaultMunch


class DDragonSummonerSpell:
    def __init__(self, data, version):
        try:
            self.version = version
            self.id = data["id"]
            self.name = data["name"]
            self.description = data["description"]
            self.tooltip = data["tooltip"]
            self.maxrank = data["maxrank"]
            self.cooldown = data["cooldown"]
            self.cooldownBurn = data["cooldownBurn"]
            self.cost = data["cost"]
            self.costBurn = data["costBurn"]
            try:
                self.datavalues = data["datavalues"]
            except:
                self.datavalues = None
            self.effect = data["effect"]
            self.effectBurn = data["effectBurn"]
            self.vars = data["vars"]
            self.key = data["key"]
            try:
                self.summonerLevel = data["summonerLevel"]
            except:
                self.summonerLevel = 0
            try:
                self.modes = data["modes"]
            except:
                self.modes = []
            self.costType = data["costType"]
            try:
                self.maxammo = data["maxammo"]
            except:
                self.maxammo = 1
            self.range = data["range"]
            self.rangeBurn = data["rangeBurn"]
            self.image = DefaultMunch.fromDict(data["image"])
            try:
                self.resource = data["resource"]
            except:
                self.resource = None
        except Exception as e:
            pprint.pp(data)
            raise e

        self._icon = None

    def icon(self):
        if self._icon is not None:
            return self._icon
        r = requests.get("https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}".format(self.version, self.image.full))
        print(r.url)
        self._icon = Image.open(BytesIO(r.content))
        return self._icon
