import pprint

import requests
from munch import DefaultMunch
from PIL import Image
from io import BytesIO


class DDragonChampion:
    def __init__(self, data, extend_method):
        self._extend_method = extend_method
        try:
            self.version = data["version"]
        except:
            self.version = ""
        try:
            champ_key = list(data["data"].keys())[0]
            data = data["data"][champ_key]
        except KeyError as e:
            pass

        self.id = data["id"]
        self.key = data["key"]
        self.name = data["name"]
        self.title = data["title"]
        self.blurb = data["blurb"]
        self.info = DefaultMunch.fromDict(data["info"])
        self.image = DefaultMunch.fromDict(data["image"])
        self.tags = data["tags"]
        try:
            self.partype = data["partype"]
        except:
            self.partype = ""
        self.stats = DefaultMunch.fromDict(data["stats"])
        self._extended = False

        if "skins" in data:
            self._extended = True
            self.skins = DefaultMunch.fromDict(data["skins"])
            self.lore = data["lore"]
            self.blurb = data["blurb"]
            self.allytips = data["allytips"]
            self.enemytips = data["enemytips"]
            self.spells = [Spell(sp, self.version) for sp in data["spells"]]

        self._icon = None
        self._loadingAsset = None
        self._splash = None

    def __getattr__(self, item):
        match item:
            case "skins":
                return self._extend().skins
            case "lore":
                return self._extend().lore
            case "blurb":
                return self._extend().blurb
            case "allytips":
                return self._extend().allytips
            case "enemytips":
                return self._extend().enemytips
            case "spells":
                return self._extend().spells
        return super().__getattribute__(item)

    def _extend(self):
        if self._extended:
            return self
        else:
            self._extended = True
            data = self._extend_method(self.id, self.version, language='en_US', returnFormat='JSON')
            champ_key = list(data["data"].keys())[0]
            data = data["data"][champ_key]
            self.skins = DefaultMunch.fromDict(data["skins"])
            self.lore = data["lore"]
            self.blurb = data["blurb"]
            self.allytips = data["allytips"]
            self.enemytips = data["enemytips"]
            self.spells = [Spell(sp, self.version) for sp in data["spells"]]
            return self

    def icon(self):
        if self._icon is not None:
            return self._icon
        r = requests.get("https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(self.version, self.id))
        print(r.url)
        self._icon = Image.open(BytesIO(r.content))
        return self._icon

    def splash(self):
        if self._splash is not None:
            return self._splash
        r = requests.get(
            "https://ddragon.leagueoflegends.com/cdn/{}/img/champion/splash/{}_0.png".format(self.version, self.id)
        )
        print(r.url)
        self._splash = Image.open(BytesIO(r.content))
        return self._splash

    def loadingAsset(self):
        if self._loadingAsset is not None:
            return self._loadingAsset
        r = requests.get(
            "https://ddragon.leagueoflegends.com/cdn/{}/img/loading/{}_0.png".format(self.version, self.id)
        )
        print(r.url)
        self._loadingAsset = Image.open(BytesIO(r.content))
        return self._loadingAsset


class Spell:
    def __init__(self, data, version):
        self.version = version
        self.name = data["name"]
        self.description = data["description"]
        self.tooltip = data["tooltip"]
        try:
            self.leveltip = DefaultMunch.fromDict(data["leveltip"])
        except KeyError as e:
            self.leveltip = DefaultMunch.fromDict({"label": []})
        self.maxrank = data["maxrank"]
        self.cooldown = data["cooldown"]
        self.cooldownBurn = data["cooldownBurn"]
        self.cost = data["cost"]
        self.costBurn = data["costBurn"]
        self.datavalues = data["datavalues"]
        self.effect = data["effect"]
        self.effectBurn = data["effectBurn"]
        self.vars = data["vars"]
        self.costType = data["costType"]
        self.maxammo = data["maxammo"]
        self.range = data["range"]
        self.rangeBurn = data["rangeBurn"]
        self.resource = data["resource"]
        self.image = DefaultMunch.fromDict(data["image"])

        self._icon = None

    def icon(self):
        if self._icon is not None:
            return self._icon

        r = requests.get(
            "https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}".format(self.version, self.image.full), stream=True
        )
        print(r.url)
        self._icon = Image.open(BytesIO(r.content))
        return self._icon
