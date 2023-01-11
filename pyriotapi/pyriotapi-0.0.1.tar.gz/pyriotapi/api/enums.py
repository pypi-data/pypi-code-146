from enum import Enum, IntEnum


class Region(Enum):
    BR = 'br1'
    EUN = 'eun1'
    EUW = 'euw1'
    JP = 'jp1'
    KR = 'kr'
    LAS = 'la1'
    LAN = 'la2'
    NA = 'na1'
    OC = 'oc1'
    TR = 'tr1'
    RU = 'ru'

    def __str__(self) -> str:
        return self.name

class Queue(Enum):
    SOLO = 'RANKED_SOLO_5x5'
    FLEX = 'RANKED_FLEX_SR'

    def __str__(self) -> str:
        return self.name

class Tier(IntEnum):
    IRON = 1
    BRONZE = 2
    SILVER = 3
    GOLD = 4
    PLATINUM = 5
    DIAMOND = 6
    MASTER = 7
    GRANDMASTER = 8
    CHALLENGER = 9

    def __str__(self) -> str:
        return self.name.title()

class Division(IntEnum):
    I = 1
    II = 2
    III = 3
    IV = 4

    def __str__(self) -> str:
        return self.name

class Locale(Enum):
    Czech = 'cs_CZ'
    Greek = 'el_GR'
    Polish = 'pl_PL'
    Romanian = 'ro_RO'
    Hungarian = 'hu_HU'
    English_GB = 'en_GB'
    German = 'de_DE'
    Spanish_ES = 'es_ES'
    Italian = 'it_IT'
    French = 'fr_FR'
    Japanese = 'ja_JP'
    Korean = 'ko_KR'
    Spanish_MX = 'es_MX'
    Spanish_AR = 'es_AR'
    Portuguese = 'pt_BR'
    English_US = 'en_US'
    Russian = 'ru_RU'
    Turkish = 'tr_TR'
    Malay = 'ms_MY'
    English_PH = 'en_PH'
    English_SG = 'en_SG'
    Thai = 'th_TH'
    Vietnamese = 'vn_VN'
    Indonesian = 'id_ID'
    Chinese_MY = 'zh_MY'
    Chinese_CN = 'zh_CN'
    Chinese_TW = 'zh_TW'

    def __str__(self) -> str:
        return self.name