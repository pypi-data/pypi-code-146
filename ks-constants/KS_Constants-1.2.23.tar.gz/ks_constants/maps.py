from enum import Enum
from ks_constants.devs import Developer
from ks_constants.locale import Language
import os

KS2_MAPS_DIRECTORY = "ks2-maps"

class Map(Enum):
    Classic = (0,
               {
                   Language.Chinese: '经典永存',
                   Language.English: 'Classic',
                   Language.Korean: '기본'
               },
               "CLASSIC",
               Developer.Luminous,
               [os.path.join("Base.SC2Data", "GameData", "Terrain", "Classic.xml")],
               os.path.join(KS2_MAPS_DIRECTORY, "classic.SC2Map"),
               False,
               False,
               None)
    Duck_Map = (1,
                {
                    Language.Chinese: '鸭鸭',
                    Language.English: 'Duck Map',
                    Language.Korean: '오리'
                },
                "DUCK_MAP",
                Developer.Duck,
                [os.path.join("Base.SC2Data", "GameData", "Terrain", "DuckMap.xml")],
                os.path.join(KS2_MAPS_DIRECTORY, "duck_map.SC2Map"),
                True,
                True,
                None)
    Zerus_Volcanoes = (2,
                       {
                           Language.Chinese: '泽鲁斯火山',
                           Language.English: 'Zerus Volcanoes',
                           Language.Korean: '제루스 화산'
                       },
                       "ZERUS_VOLCANOES",
                       Developer.Luminous,
                       [os.path.join("Base.SC2Data", "GameData", "Terrain", "ZerusVolcanoes.xml")],
                       os.path.join(KS2_MAPS_DIRECTORY, "zerus_volcanoes.SC2Map"),
                       True,
                       True,
                       None)
    Ruins_Of_Imladoon = (3,
                         {
                             Language.Chinese: '伊姆拉杜恩遗址',
                             Language.English: 'Ruins of Imladoon',
                             Language.Korean: '임라둔의 잔해'
                         },
                         "RUINS_OF_IMLADOON",
                         Developer.Fatline,
                         [os.path.join("Base.SC2Data", "GameData", "Terrain", "RuinsOfImladoon.xml")],
                         os.path.join(KS2_MAPS_DIRECTORY, "ruins_of_imladoon.SC2Map"),
                         True,
                         True,
                         Developer.Templar)
    Four_Seasons = (4,
                    {
                        Language.Chinese: '四季交叠',
                        Language.English: 'Four Seasons',
                        Language.Korean: '사계절'
                    },
                    "FOUR_SEASONS",
                    Developer.Luminous,
                    [os.path.join("Base.SC2Data", "GameData", "Terrain", "FourSeasons.xml")],
                    os.path.join(KS2_MAPS_DIRECTORY, "four_seasons.SC2Map"),
                    False,
                    False,
                    None)
    Heart_Of_Amethyst = (5,
                         {
                             Language.Chinese: '紫水晶之心',
                             Language.English: 'Heart of Amethyst',
                             Language.Korean: '자수정의 심장'},
                         "HEART_OF_AMETHYST",
                         Developer.Luminous,
                         [os.path.join("Base.SC2Data", "GameData", "Terrain", "HeartOfAmethyst.xml")],
                         os.path.join(KS2_MAPS_DIRECTORY, "heart_of_amethyst.SC2Map"),
                         False,
                         False,
                         None)
    Vintage_Shores = (6,
                      {
                          Language.Chinese: '夏日海滩',
                          Language.English: 'Vintage Shores',
                          Language.Korean: '빈티지 해변'
                      },
                      "VINTAGE_SHORES",
                      Developer.Templar,
                      [os.path.join("Base.SC2Data", "GameData", "Terrain", "VintageShores.xml")],
                      os.path.join(KS2_MAPS_DIRECTORY, "vintage_shores.SC2Map"),
                      False,
                      False,
                      None)
    Aiur_Fountains = (7,
                      {
                          Language.Chinese: '艾尔之泉',
                          Language.English: 'Aiur Fountains',
                          Language.Korean: '아이어 분수'
                      },
                      "AIUR_FOUNTAINS",
                      Developer.Luminous,
                      [os.path.join("Base.SC2Data", "GameData", "Terrain", "AiurFountains.xml")],
                      os.path.join(KS2_MAPS_DIRECTORY, "aiur_fountains.SC2Map"),
                      False,
                      False,
                      None)
    Kaldir_Cliffs = (8,
                     {
                         Language.Chinese: '冰封王座',
                         Language.English: 'Kaldir Cliffs',
                         Language.Korean: '칼디르 절벽'
                     },
                     "KALDIR_CLIFFS",
                     Developer.Understudy,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "KaldirCliffs.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "kaldir_cliffs.SC2Map"),
                     False,
                     False,
                     None)
    Lost_Tides = (9,
                     {
                         Language.Chinese: '失意之汐',
                         Language.English: 'Lost Tides',
                         Language.Korean: '잃어버린 강'
                     },
                     "LOST_TIDES",
                     Developer.Templar,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "LostTides.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "lost_tides.SC2Map"),
                     True,
                     True,
                     None)

    # galaxy representation is the string value of the Preset in KS2 Galaxy
    def __init__(self,
                 index: int,
                 name_dict: dict,
                 galaxy_representation: str,
                 original_author: Developer,
                 custom_file_list: list[str],
                 file_path: str,
                 is_available: bool = False, # whether community has downvoted map
                 is_active: bool = False, # whether the map is in the current pool
                 current_author: Developer = None):
        self._index = index
        self._name_dict = name_dict
        self._galaxy_representation = galaxy_representation
        self._custom_file_list = custom_file_list
        self._file_path = file_path
        self._original_author = original_author
        self._current_author = original_author if current_author is None else current_author
        self._is_available = is_available
        self._is_active = is_active

    @classmethod
    def from_index(cls, index):
        return _maps_list[index]

    def get_index(self):
        return self._index

    def get_name(self, locale: Language):
        return self._name_dict[locale]

    def get_english_name(self):
        return self.get_name(Language.English)

    def get_galaxy_representation(self):
        return self._galaxy_representation

    def original_author(self):
        return self._original_author

    def current_author(self):
        return self._current_author

    def file_path(self):
        return self._file_path

    def is_available(self):
        return self._is_available

    def is_active(self):
        return self._is_active

    def custom_file_list(self):
        return self._custom_file_list


_maps_list = list(Map)
