import copy
import dataclasses
import os
from abc import ABC
from dataclasses import field
from typing import ClassVar

import pandas
import requests
from bs4 import BeautifulSoup

from dry_scraper.data_sources.data_source import DataSource
from dry_scraper.data_sources.nhl.nhl_helpers.nhl_ros_htm_helpers import \
    (strip_and_zip_player_list, strip_and_zip_official_list, create_ros_entries,
     create_official_entries)
from dry_scraper.shared import (ROSTER_TEMPLATE, TEAM_MAP, SHIFTS_TEMPLATE,
                                ROSTER_CSV_COLUMNS, SHIFTS_CSV_COLUMNS)
from dry_scraper.teams import TEAMS

dataclass = dataclasses.dataclass(init=True, repr=True, eq=False, order=False,
                                  unsafe_hash=False, frozen=False)


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameHtmSource(DataSource, ABC):
    """
    Abstract subclass of DataSource that represents an NHL Game Report

    ...

    Attributes
    ----------
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
        fully qualified nhl.com URL, completed on instantiation
    url_stub : str
        inherited from DataSource
        partial nhl.com URL. static for each subclass
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

    Methods
    -------
    @abstractmethod
    validate_content():
        validate self.content fetched and record result in self.integrity
    fetch_content():
        inherited from DataSource
        fetch content from self.url with self.season_query and store response in self.content
    load_content():
        inherited from DataSource
        load source file designated by self.local_path, if it exists, and store
        contents in self.content
    write_raw_content():
        inherited from DataSource
        write self.content to local directory specified by self.local_path
    """
    url_stub: ClassVar[str] = 'http://www.nhl.com/scores/htmlreports/'
    extension: ClassVar[str] = 'htm'
    season: str = field(init=False, default_factory=str)
    gamePk: str = field(init=False, default_factory=str)

    def fetch_content(self):
        """
        Use requests.get to retrieve HTM file and store in self.content

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


# noinspection PyUnresolvedReferences
@dataclass
class NhlGamePbpHtmSource(NhlGameHtmSource):
    """
    Subclass of NhlGameHtmSource that represents an NHL Play By Play Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI


    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """

    desc: ClassVar[str] = 'NHL Official Game Reports - Play-by-play Report'
    name: ClassVar[str] = 'NHL_HTM_PBP'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'PL'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_PL')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameRosterHtmSource(NhlGameHtmSource):
    """
    Subclass of NhlGameHtmSource that represents an NHL Roster Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI


    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL Official Game Reports - Roster Report'
    name: ClassVar[str] = 'NHL_HTM_ROSTER'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'RO'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_RO')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        """
        Return a dictionary representation of the data available from the roster
        file.
                {
                'season': ...,
                'gamePk': ...,
                'home': {
                    'team':         {...},
                    'dressed':      {...},
                    'scratched':    {...},
                    'head_coaches': {...}
                    },
                'away': {
                    'team':         {...},
                    'dressed':      {...},
                    'scratched':    {...},
                    'head_coaches': {...}
                    },
                'officials': {
                    'referees':     {...},
                    'linesmen':     {...}
                    }}

        Returns:
            self
        """

        roster_dict = copy.deepcopy(ROSTER_TEMPLATE)
        ros_soup = BeautifulSoup(self.content, 'html.parser')
        try:
            away_dressed_tags = ros_soup.select('.border')[2].find_all('td')[3:]
        except:
            away_dressed_tags = []
            print('Failed to parse away roster')
        try:
            home_dressed_tags = ros_soup.select('.border')[3].find_all('td')[3:]
        except:
            home_dressed_tags = []
            print('Failed to parse home roster')
        try:
            away_scratch_tags = ros_soup.select('tr#Scratches > td')[0].find_all('td')[3:]
        except:
            away_scratch_tags = []
            print('Failed to parse away scratches')
        try:
            home_scratch_tags = ros_soup.select('tr#Scratches > td')[1].find_all('td')[3:]
        except:
            home_scratch_tags = []
            print('Failed to parse home scratches')
        try:
            away_coach_tag = ros_soup.select('tr#HeadCoaches > td')[0].find_all('td')[0]
        except:
            away_coach_tag = []
            print('Failed to parse away coach')
        try:
            home_coach_tag = ros_soup.select('tr#HeadCoaches > td')[1].find_all('td')[0]
        except:
            home_coach_tag = []
            print('Failed to parse home coach')
        # Doesn't work before 2009-2010 season but I don't care too much rn
        try:
            official_tags = (ros_soup.select('.border')[-1]
                             .select('table > tr')[1]
                             .select('tr'))
        except:
            official_tags = []
            print('Failed to parse officials')
        try:
            teams = ros_soup.select('td.teamHeading.border')
        except:
            teams = []
            print('Failed to parse team names')
        away_dressed = strip_and_zip_player_list(away_dressed_tags)
        home_dressed = strip_and_zip_player_list(home_dressed_tags)
        away_scratch = strip_and_zip_player_list(away_scratch_tags)
        home_scratch = strip_and_zip_player_list(home_scratch_tags)
        refs, linesmen = strip_and_zip_official_list(official_tags)

        roster_dict['away']['team'] = TEAMS[TEAM_MAP[teams[0].string]]
        roster_dict['home']['team'] = TEAMS[TEAM_MAP[teams[1].string]]
        roster_dict['away']['dressed'] = create_ros_entries(away_dressed)
        roster_dict['home']['dressed'] = create_ros_entries(home_dressed)
        roster_dict['away']['scratched'] = create_ros_entries(away_scratch)
        roster_dict['home']['scratched'] = create_ros_entries(home_scratch)
        roster_dict['away']['headCoach'] = away_coach_tag.string
        roster_dict['home']['headCoach'] = home_coach_tag.string
        roster_dict['officials']['referees'] = create_official_entries(refs)
        roster_dict['officials']['linesmen'] = create_official_entries(linesmen)
        roster_dict['season'] = self.season
        roster_dict['gamePk'] = self.gamePk

        self.content_json = roster_dict
        return self

    def parse_to_csv(self):
        """
        Parse the roster into a pandas dataframe containing each player, head coach, and
        official mentioned in the game sheets and store the result in content_csv.
        Use content_json to accomplish this.

        Returns:
            self

        """
        roster = []
        if not self.content_json:
            self.parse_to_json()
        officials = self.content_json['officials']
        for team in ['home', 'away']:
            team_dict = self.content_json[team]
            home = team == 'home'
            team_tricode = team_dict['team']['abbreviation']

            for player in team_dict['dressed']:
                position = player['position']
                jersey_number = player['jerseyNumber']
                captain = 'C' if player['captain'] else 'A' if player['alternate'] else ''
                name = player['name']
                roster.append((position, jersey_number, captain, name, team_tricode, home,
                               '', '', ''))
            for player in team_dict['scratched']:
                position = player['position']
                jersey_number = player['jerseyNumber']
                captain = 'C' if player['captain'] else 'A' if player['alternate'] else ''
                name = player['name']
                roster.append((position, jersey_number, captain, name, team_tricode, home,
                               True, '', ''))
            roster.append(('', '', '', team_dict['headCoach'], team_tricode, home,
                           '', True, ''))
        for ref in officials['referees'] + officials['linesmen']:
            role = ref['role']
            jersey_number = ref['jerseyNumber']
            name = ref['name']
            roster.append(('', jersey_number, '', name, 'NHL', '', '', '', role))
        self.content_csv = pandas.DataFrame(roster, columns=ROSTER_CSV_COLUMNS)
        self.content_csv.insert(0, 'gamePk', self.gamePk, False)
        self.content_csv.insert(0, 'season', self.season, False)
        return self


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameShiftsHtmSource(NhlGameHtmSource, ABC):
    """
    Abstract subclass of NhlGameHtmSource that represents an NHL TOI Shift Report

    ...

    Attributes
    ----------
    home : bool
        boolean identifying the home or away team

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    home: bool

    def __post_init__(self):
        team = "TH" if self.home else "TV"
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'{team}'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_{team}')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        # This pass is here just so the subclasses think this method has been implemented
        pass
        raise NotImplementedError

    def parse_to_json(self):
        """
        Return a dictionary representation of the shift chart
                {
                'season': ...,
                'gamePk': ...,
                'home': ...,
                'shifts': [{
                    'player': ...,
                    'shift_start': ...,
                    'shift_end': ...
                    }, ...]
                }
       Use content_csv to create this

        Returns:
            self
        """
        if not self.content is None:
            self.parse_to_csv()
        shifts_json = copy.deepcopy(SHIFTS_TEMPLATE)
        shifts_json['shifts'] = self.content_csv[['player', 'shift_start', 'shift_end']] \
            .to_dict('records')
        shifts_json['season'] = self.season
        shifts_json['gamePk'] = self.gamePk
        shifts_json['home'] = self.home
        self.content_json = shifts_json
        return self

    def parse_to_csv(self):
        """
        Parse the shift chart into a pandas dataframe containing each shift.
        The columns of the dataframe are (season, gamePk, player, shift_start, shift_end)

        Returns:
            self

        """
        toi_soup = BeautifulSoup(self.content, 'html.parser')
        row_list = toi_soup.find_all('tr')

        outRows = []
        for i in range(len(row_list) - 1):
            row = row_list[i]
            if row.find('td'):
                row_class = row.find('td').get('class', [])
                if 'playerHeading' in row_class:
                    player_name = row.find('td').string

                    i += 2
                    row = row_list[i]
                    row_class = row.get('class', [])
                    while 'evenColor' in row_class or 'oddColor' in row_class:
                        try:
                            tds = row.find_all('td')
                            per = int(tds[1].string) if tds[1].string != 'OT' else 4
                            shift_start = tds[2].string.split(' / ')[0].split(':')
                            shift_end = tds[3].string.split(' / ')[0].split(':')
                            shift_start = (1200 * (per - 1) +
                                           60 * int(shift_start[0]) +
                                           int(shift_start[1]))
                            shift_end = (1200 * (per - 1) +
                                         60 * int(shift_end[0]) +
                                         int(shift_end[1]))
                            shiftTup = [(player_name, shift_start, shift_end)]
                            outRows += shiftTup
                        except Exception:
                            pass
                        i += 1
                        row = row_list[i]
                        row_class = row.get('class', [])
        self.content_csv = pandas.DataFrame(outRows, columns=SHIFTS_CSV_COLUMNS)
        self.content_csv.insert(0, 'gamePk', self.gamePk, False)
        self.content_csv.insert(0, 'season', self.season, False)
        return self


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameVisitorShiftsHtmSource(NhlGameShiftsHtmSource):
    """
    Subclass of NhlGameShiftsHtmSource that represents an NHL away team TOI Shift Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    home : bool
        boolean identifying the home or away team

    Methods
    -------
    None
    """
    home: ClassVar[bool] = False
    desc: ClassVar[str] = 'NHL Official Game Reports - Away Time on Ice Report'
    name: ClassVar[str] = 'NHL_HTM_ATOI'
    season: str
    gamePk: str


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameHomeShiftsHTMSource(NhlGameShiftsHtmSource):
    """
    Subclass of NhlGameShiftsHtmSource that represents an NHL home team TOI Shift Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    home : bool
        boolean identifying the home or away team

    Methods
    -------
    None
    """
    home: ClassVar[bool] = True
    desc: ClassVar[str] = 'NHL Official Game Reports - Home Time on Ice Report'
    name: ClassVar[str] = 'NHL_HTM_HTOI'
    season: str
    gamePk: str


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameSummaryHtmSource(NhlGameHtmSource):
    """
    Subclass of NhlGameHtmSource that represents an NHL Game Summary Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL Official Game Reports - Game Summary Report'
    name: ClassVar[str] = 'NHL_HTM_GS'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'GS'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_GS')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameEventSummaryHtmSource(NhlGameHtmSource):
    """
    Subclass of NhlGameHtmSource that represents an NHL Event Summary Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL Official Game Reports - Event Summary Report'
    name: ClassVar[str] = 'NHL_HTM_ES'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'ES'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_ES')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameFaceoffSummaryHtmSource(NhlGameHtmSource):
    """
    Subclass of NhlGameHtmSource that represents an NHL Face-off Summary Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL Official Game Reports - Face-off Summary Report'
    name: ClassVar[str] = 'NHL_HTM_FOS'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'FS'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_FS')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameFaceoffComparisonHtmSource(NhlGameHtmSource):
    """
    Subclass of NhlGameHtmSource that represents an NHL Face-off Comparison Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL Official Game Reports - Face-off Comparison Report'
    name: ClassVar[str] = 'NHL_HTM_FOC'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'FC'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_FC')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameShotReportHtmSource(NhlGameHtmSource):
    """
    Subclass of NhlGameHtmSource that represents an NHL Shot Report

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """

    desc: ClassVar[str] = 'NHL Official Game Reports - Shot Report'
    name: ClassVar[str] = 'NHL_HTM_SHOT'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    f'{self.season}/'
                    f'SS'
                    f'0{self.gamePk}.HTM')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_SS')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_json(self):
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError
