import pprint

from .runes import DDragonRune, DDragonRuneTree
import requests
import json
from .champions import DDragonChampion
from .items import DDragonItem
from .summonerSpells import DDragonSummonerSpell
from munch import DefaultMunch

class DDragonFactory:
    def __init__(self):
        self._regionStatus = {}
        self._versions = None
        self._champions = {}
        self._summoners = {}
        self._indivChampion = {}
        self._items = {}
        self._runes = {}
        self._id_to_key = {}

    def regionStatus(self, region: str):
        if region not in self._regionStatus:
            r = requests.get("https://ddragon.leagueoflegends.com/realms/{}.json".format(region))
            self._regionStatus[region] = json.loads(r.content)
        return self._regionStatus[region]

    def versions(self):
        if self._versions is None:
            self._versions = json.loads(requests.get("https://ddragon.leagueoflegends.com/api/versions.json").content)
            self._versions = list(filter(lambda v:"lolpatch_" not in v,self._versions))
        return self._versions

    def champions(self, version, language='en_US') -> {str:DDragonChampion}:
        if version + language not in self._champions:
            # print(self._champions.keys())
            # print("https://ddragon.leagueoflegends.com/cdn/{}/data/{}/champion.json".format(version, language))
            r = json.loads(
                requests.get(
                    "https://ddragon.leagueoflegends.com/cdn/{}/data/{}/champion.json".format(version, language)
                ).content
            )
            self._champions[version + language] = {r["data"][c]["key"]: DDragonChampion(r["data"][c], self.champion) for
                                                   c in r["data"]}
            # print(self._champions[version + language].keys())
            self._id_to_key[version + language] = {r["data"][c]["id"]: r["data"][c]["key"] for c in r["data"]}
        return self._champions[version + language]

    def summoners(self, version, language='en_US'):
        if version + language not in self._summoners:
            r = json.loads(
                requests.get(
                    "https://ddragon.leagueoflegends.com/cdn/{}/data/{}/summoner.json".format(version, language)
                ).content
            )
            
            self._summoners[version + language] = {r["data"][c]["key"]: DDragonSummonerSpell(r["data"][c], version) for
                                               c in r["data"]}
            
        return self._summoners[version + language]

    def summonerFromId(self, summonerSpellId, version, language='en_US'):
        if summonerSpellId == '0' or summonerSpellId == 0:
            return DefaultMunch({"name":""})
        return self.summoners(version, language)[str(summonerSpellId)]

    def champion(self, champion, version, language='en_US', returnFormat='ddragonFactory'):
        if champion + version + language not in self._champions:
            url = "https://ddragon.leagueoflegends.com/cdn/{}/data/{}/champion/{}.json".format(
                version, language,
                champion
            )
            # print(url)
            data = json.loads(
                requests.get(
                    url
                ).content
            )
            self._indivChampion[champion + version + language] = DDragonChampion(
                data,
                self.champion
            )
            if returnFormat == 'JSON':
                return data

        return self._indivChampion[champion + version + language]

    def championFromId(self, championId, version, language='en_US'):
        return self.champions(version, language)[str(championId)]

    def championFromName(self, championName, version, language='en_US'):
        return self.champions(version, language)[self._id_to_key[version + language][championName]]

    def championFromFullName(self, championName, version, language='en_US'):
        for champ in self.champions(version, language).values():
            if champ.name == championName:
                return champ

    def items(self, version, language='en_US'):
        if version + language not in self._items:
            r = json.loads(
                requests.get(
                    "https://ddragon.leagueoflegends.com/cdn/{}/data/{}/item.json".format(version, language)
                ).content
            )["data"]

            # print("https://ddragon.leagueoflegends.com/cdn/{}/data/{}/item.json".format(version, language))
            self._items[version + language] = {it_id: DDragonItem(r[it_id], version) for it_id in r}
        return self._items[version + language]

    def itemFromId(self, itemdId, version, language='en_US'):
        exclude_list = [1501]
        if itemdId == 0 or int(itemdId) in exclude_list:
            return DefaultMunch({"name":""})
        try:
            return self.items(version, language)[str(itemdId)]
        except Exception as e:
            # Handle Ornn Items
            if int(itemdId) >= 7000:
                return self.items("12.21.1", language)[str(itemdId)]
            else:
                raise e

    def runes(self, version, language='en_US'):
        version_split = version.split(".")
        cdragon_patch = version_split[0] + "." + version_split[1]
        if version + language not in self._runes:
            if self.versions().index(version) < self.versions().index("7.23.1"):
                r = requests.get(
                    "https://ddragon.leagueoflegends.com/cdn/{}/data/{}/runesReforged.json".format(version, language)
                )
                # print("https://ddragon.leagueoflegends.com/cdn/{}/data/{}/runesReforged.json".format(version, language))
                runesFile = json.loads(r.content)
                self._runes[version + language] = {tree["id"]: DDragonRuneTree(tree, cdragon_patch) for tree in
                                                   runesFile}
                for tree in runesFile:
                    for slot in tree["slots"]:
                        for rune in slot["runes"]:
                            self._runes[version + language][rune["id"]] = DDragonRune(rune, cdragon_patch)
            else:
                r = requests.get(
                    "https://ddragon.leagueoflegends.com/cdn/{}/data/{}/mastery.json".format(version, language)
                )
                # print("https://ddragon.leagueoflegends.com/cdn/{}/data/{}/mastery.json".format(version, language))
                runesFile = json.loads(r.content)["data"]
                #pprint.pp(runesFile)
                self._runes[version + language] = {runesFile[rune]["id"]: DDragonRune(runesFile[rune], cdragon_patch) for rune in
                                                   runesFile}





            if 5003 not in self._runes[version + language]:
                for rune in statRunes:
                    self._runes[version + language][rune["id"]] = DDragonRune(rune, cdragon_patch)

        return self._runes[version + language]

    def runeFromId(self, runeId, version, language='en_US'):
        if runeId == 0:
            return None
        #pprint.pp(self.runes(version, language))
        return self.runes(version, language)[runeId]


statRunes = [
    {
        "id": 5003,
        "name": "MagicRes",
        "key": "MagicRes",
        "majorChangePatchVersion": "",
        "tooltip": "+8 Magic Resist",
        "shortDesc": "+8 Magic Resist",
        "longDesc": "+8 Magic Resist",
        "recommendationDescriptor": "",
        "icon": "/statmods/StatModsMagicResIcon.png",
        "endOfGameStatDescs": [],
        "recommendationDescriptorAttributes": {}
    },
    {
        "id": 5002,
        "name": "Armor",
        "key": "Armor",
        "majorChangePatchVersion": "",
        "tooltip": "+6 Armor",
        "shortDesc": "+6 Armor",
        "longDesc": "+6 Armor",
        "recommendationDescriptor": "",
        "icon": "/statmods/StatModsArmorIcon.png",
        "endOfGameStatDescs": [],
        "recommendationDescriptorAttributes": {}
    },
    {
        "id": 5008,
        "name": "Adaptive",
        "key": "Adaptive",
        "majorChangePatchVersion": "",
        "tooltip": "<scaleAD>+@f2@ Attack Damage</scaleAD>",
        "shortDesc": "+9 <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>Adaptive Force</font></lol-uikit-tooltipped-keyword>",
        "longDesc": "+9 <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>Adaptive Force</font></lol-uikit-tooltipped-keyword>",
        "recommendationDescriptor": "",
        "icon": "/statmods/StatModsAdaptiveForceIcon.png",
        "endOfGameStatDescs": [],
        "recommendationDescriptorAttributes": {}
    },
    {
        "id": 5001,
        "name": "HealthScaling",
        "key": "HealthScaling",
        "majorChangePatchVersion": "",
        "tooltip": "+@f1@ Health (based on level)",
        "shortDesc": "+15-140 Health (based on level)",
        "longDesc": "+15-140 Health (based on level)",
        "recommendationDescriptor": "",
        "icon": "/statmods/StatModsHealthScalingIcon.png",
        "endOfGameStatDescs": [],
        "recommendationDescriptorAttributes": {}
    },
    {
        "id": 5007,
        "name": "CDRScaling",
        "key": "CDRScaling",
        "majorChangePatchVersion": "",
        "tooltip": "+@f1@ Ability Haste",
        "shortDesc": "+8 <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_CDR'>Ability Haste</lol-uikit-tooltipped-keyword> ",
        "longDesc": "+8 <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_CDR'>Ability Haste</lol-uikit-tooltipped-keyword> ",
        "recommendationDescriptor": "",
        "icon": "/statmods/StatModsCDRScalingIcon.png",
        "endOfGameStatDescs": [],
        "recommendationDescriptorAttributes": {}
    },
    {
        "id": 5005,
        "name": "AttackSpeed",
        "key": "AttackSpeed",
        "majorChangePatchVersion": "",
        "tooltip": "+10% Attack Speed",
        "shortDesc": "+10% Attack Speed",
        "longDesc": "+10% Attack Speed",
        "recommendationDescriptor": "",
        "icon": "/statmods/statmodsattackspeedicon.png",
        "endOfGameStatDescs": [],
        "recommendationDescriptorAttributes": {}
    },
]

ddragon_factory = DDragonFactory()
