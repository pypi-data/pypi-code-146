import dataclasses
import os
from dataclasses import field
from datetime import datetime
from typing import ClassVar

import pandas
import requests

from dry_scraper.data_sources.data_source import DataSource
from dry_scraper.data_sources.nhl.nhl_helpers.espn_xml_helpers import (
    determine_espn_play_type, build_shootout_end_event,
    parse_xml_plays, build_goal_event, build_shot_event, build_faceoff_event,
    build_missed_shot_event, build_hit_event, build_takeaway_event, build_giveaway_event,
    build_blocked_shot_event, build_penalty_event, build_stop_event,
    build_period_start_event, build_period_end_event, build_game_end_event,
    determine_espn_id)
from dry_scraper.shared import (
    EVENTTYPEID_EVENT, ESPN_CSV_COLUMNS
)

dataclass = dataclasses.dataclass(init=True, repr=True, eq=False, order=False,
                                  unsafe_hash=False, frozen=False)


# noinspection PyUnresolvedReferences,PyArgumentList
@dataclass
class NhlEspnPbpXmlSource(DataSource):
    """
    Abstract subclass of DataSource that represents an ESPN XML play by play

        XML play schema
            play_list[0]:   x-coord of event
            play_list[1]:   y-coord of event
            play_list[2]:   id number indicating event type
            play_list[3]:   time elapsed in period
            play_list[4]:   period
            play_list[5]:   player1
            play_list[6]:   player2
            play_list[7]:   player3
            play_list[8]:   text description of event
            play_list[9]:   id indicating secondary detail about event
                            shot type, penalty type, zone, etc.
            play_list[10]:  home team goals
            play_list[11]:  away team goals
            play_list[12]:  id indicating player
                            only example found so far is player serving a bench minor
            play_list[13]:  strength state
                            701 EV, 702 PP, 703 SH, etc.
            play_list[14]:  id number indicating team of event player1
            play_list[15]:  shows up only on goals scored
                            801/803/805 no apparent pattern
            play_list[16]:  shows up on SOG, missed shots, goals
                            901 on all except 903 on ENG
            play_list[17]:  goal scorer's season total
            play_list[18]:  primary assister's season total
            play_list[19]:  secondary assister's season total

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    content : str
        inherited from DataSource.
        string representation of data retrieved by fetch_content() or load_content()
    local_path : str
        inherited from DataSource
        full path to storage location for file representation of data
    local_path_stub : str
        inherited from DataSource
        partial path to storage location. set in config. static for all subclasses
    url : str
        inherited from DataSource
        fully qualified espn.com URL, completed on instantiation
    url_stub : str
        inherited from DataSource
        partial espn.com URL. static for each subclass
    extension : str
        inherited from DataSource
        file extension to be used when writing the raw data source to disk e.g. json, HTM
    integrity : dict
        inherited from DataSource
        information about the integrity of content as determined by validate_content()
    season : str
        8 character representation of an NHL season (e.g. 20202021)
    gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)
    espn_game_id : str
        9 character representation of NHL game on espn.com (e.g. 401272554)

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    fetch_content():
        inherited from DataSource
        fetch content from self.url with self.season_query and store response in self.content
    load_content():
        inherited from DataSource
        load source file designated by self.local_path, if it exists, and store
        contents in self.content
    parse_to_json():
        Parse content into dict/json form and store result in self.content_json
    parse_to_csv():
        Parse content into pandas dataframe and store result in self.content_csv
    write_raw_content():
        inherited from DataSource
        write self.content to local directory specified by self.local_path
    determine_espn_id():
        determine the game ID number assigned by ESPN to the season and game_id provided
    """

    url_stub: ClassVar[str] = 'https://www.espn.com/nhl/gamecast/data/masterFeed?gameId='
    extension: ClassVar[str] = 'xml'
    desc: ClassVar[str] = 'ESPN NHL - Play-by-play XML'
    name: ClassVar[str] = 'ESPN_XML_PBP'
    season: str
    gamePk: str
    espn_game_id: str = field(init=False, default_factory=str)

    def __post_init__(self):
        self.espn_game_id = determine_espn_id(self.season, self.gamePk)
        self.url = f'{self.url_stub}{self.espn_game_id}'
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_ES')

    def fetch_content(self):
        """
        Use requests.get to retrieve XML file
        
        Returns:
            self
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.content = response.text
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        return self

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        """
        Parse the XML into a list of dictionaries representing each play of the game as
        described in ESPM XML play-by-play record and store in content_json

        Returns:
            self
        """
        plays = parse_xml_plays(self.content)

        build_event = {
            'GOAL': build_goal_event,
            'SHOT': build_shot_event,
            'FACEOFF': build_faceoff_event,
            'MISSED_SHOT': build_missed_shot_event,
            'HIT': build_hit_event,
            'TAKEAWAY': build_takeaway_event,
            'GIVEAWAY': build_giveaway_event,
            'BLOCKED_SHOT': build_blocked_shot_event,
            'PENALTY': build_penalty_event,
            'STOP': build_stop_event,
            'PERIOD_START': build_period_start_event,
            'PERIOD_END': build_period_end_event,
            'GAME_END': build_game_end_event,
            'SHOOTOUT_END': build_shootout_end_event
        }

        all_plays = []
        for i, espn_play in enumerate(plays):
            play_list = espn_play.split('~')

            if play_list[2] == '504':
                play_type = 'TAKEAWAY' if 'TAKEAWAY' in play_list[8] else 'GIVEAWAY'
            else:
                play_type = determine_espn_play_type(play_list[2])

            nhl_play = build_event[play_type](espn_play)

            if play_type in ['PERIOD_START', 'PERIOD_END', 'GAME_END', 'SHOOTOUT_END']:
                all_plays.append(nhl_play)
                continue

            nhl_play['result']['description'] = play_list[8]
            nhl_play['result']['event'] = EVENTTYPEID_EVENT[play_type]
            nhl_play['result']['eventTypeId'] = play_type

            nhl_play['coordinates']['x'] = play_list[0]
            nhl_play['coordinates']['y'] = play_list[1]

            nhl_play['about']['eventIdx'] = i
            nhl_play['about']['period'] = play_list[4]
            try:
                period_time = (datetime.strptime('20:00', '%M:%S') -
                               datetime.strptime(play_list[3], '%M:%S'))
                nhl_play['about']['periodTimeRemaining'] = (
                        '%02d:%02d' % (int(play_list[3].split(':')[0]),
                                       int(play_list[3].split(':')[1])))
            except ValueError:
                period_time = (datetime.strptime('20:00', '%M:%S') -
                               datetime.strptime('00:00', '%M:%S'))
                nhl_play['about']['periodTimeRemaining'] = '20:00'
            nhl_play['about']['periodTime'] = ('%02d:%02d'
                                               % (period_time.seconds // 60,
                                                  period_time.seconds % 60))
            nhl_play['about']['goals']['home'] = play_list[10]
            nhl_play['about']['goals']['away'] = play_list[11]
            all_plays.append(nhl_play)
        self.content_json = {'season': self.season, 'espn_game_id': self.espn_game_id,
                             'gamePk': self.gamePk, 'allPlays': all_plays}
        return self

    def parse_to_csv(self):
        """
        Parse the XML into a pandas dataframe containing each play of the game as
        described in ESPM XML play-by-play record and store in content_csv

        Returns:
            self

        """
        plays = parse_xml_plays(self.content)
        plays = [play.split('~') for play in plays]

        self.content_csv = pandas.DataFrame(plays, columns=ESPN_CSV_COLUMNS)
        self.content_csv.insert(0, 'gamePk', self.gamePk, False)
        self.content_csv.insert(0, 'espn_game_id', self.espn_game_id, False)
        self.content_csv.insert(0, 'season', self.season, False)
        return self
