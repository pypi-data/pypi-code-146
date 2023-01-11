import dataclasses
import json
import os
from abc import ABC
from dataclasses import field
from typing import ClassVar

import requests

from dry_scraper.data_sources.data_source import DataSource

dataclass = dataclasses.dataclass(init=True, repr=True, eq=False, order=False,
                                  unsafe_hash=False, frozen=False)


# noinspection PyUnresolvedReferences
@dataclass
class NhlApiSource(DataSource, ABC):
    """
    Abstract subclass of DataSource that represents a request and result from NHL API.
    API fully documented here: https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md

    ...

    Attributes
    ----------
    content : str
        inherited from DataSource.
        string representation of data retrieved by fetch_content() or load_content()
    content_parsed : dict
        inherited from DataSource.
        dict representation of raw content parsed by parse_to_json()
    content_csv : str
        inherited from DataSource.
        string representation of content parsed into csv format
    local_path : str
        inherited from DataSource
        full path to storage location for file representation of data
    local_path_stub : str
        inherited from DataSource
        partial path to storage location. set in config. static for all subclasses
    url : str
        inherited from DataSource
        fully qualified API endpoint, completed on instantiation
    url_stub : str
        inherited from DataSource
        partial API endpoint. static for each subclass
    extension : str
        inherited from DataSource
        file extension to be used when writing the raw data source to disk e.g. json, HTM
    integrity : dict
        inherited from DataSource
        information about the integrity of content as determined by validate_content()


    Methods
    -------
    @abstractmethod
    validate_content():
        validate self.content fetched and record result in self.integrity
    fetch_content():
        inherited from DataSource
        fetch content from self.url store response in self.content
    load_content():
        inherited from DataSource
        load source file designated by self.local_path, if it exists, and store
        contents in self.content
    parse_to_json():
        inherited from DataSource
        Parse content into dict/json form and store result in self.content_json
    write_raw_content():
        inherited from DataSource
        write self.content to local directory specified by self.local_path
    """
    url_stub: ClassVar[str] = 'https://statsapi.web.nhl.com/api/v1'
    extension: ClassVar[str] = 'json'
    query: dict = field(default_factory=dict, init=False)

    def fetch_content(self):
        """
        Query NHL API endpoint at self.url

        Returns:
            self
        """
        try:
            response = requests.get(self.url, self.query, timeout=10)
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

    def parse_to_json(self):
        """
        Use json.loads to create a dictionary object for the data source and store it in
        self.content_json

        Returns:
            self
        """
        self.content_json = json.loads(self.content)
        return self


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameBoxScoreApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL box score API

    ...

    Attributes
    ----------
    season : str
        8 character representation of an NHL season (e.g. 20202021)
    gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """

    desc: ClassVar[str] = 'NHL API - Box Score'
    name: ClassVar[str] = 'NHL_API_BOX'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/game/'
                    f'{self.season[:4]}'
                    '0'
                    f'{self.gamePk}'
                    '/boxscore')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_BS')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameLineScoreApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL line score API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    season : str
        8 character representation of an NHL season (e.g. 20202021)
    gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)
    name : str
        identifying name for the CLI


    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL API - Line Score'
    name: ClassVar[str] = 'NHL_API_LINE'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/game/'
                    f'{self.season[:4]}'
                    '0'
                    f'{self.gamePk}'
                    '/linescore')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_LS')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameContentApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL content API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    season : str
        8 character representation of an NHL season (e.g. 20202021)
    gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)
    name : str
        identifying name for the CLI


    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL API - Game Content'
    name: ClassVar[str] = 'NHL_API_CONTENT'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/game/'
                    f'{self.season[:4]}'
                    '0'
                    f'{self.gamePk}'
                    '/content')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_CN')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameLiveFeedApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL live feed API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    season : str
        8 character representation of an NHL season (e.g. 20202021)
    gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)
    name : str
        identifying name for the CLI


    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    yield_teams_and_date():
        return home and away tricodes and date string of game from self.content
        used by NhlEspnPbpXmlSource to determine ESPN game code
    """
    desc: ClassVar[str] = 'NHL API - Game Live Feed'
    name: ClassVar[str] = 'NHL_API_LIVE'
    season: str
    gamePk: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/game/'
                    f'{self.season[:4]}'
                    '0'
                    f'{self.gamePk}'
                    '/feed/live')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.season[:4]}{self.gamePk}_LV')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def yield_teams_and_date(self):
        """
            Return home and away tricodes and date string of game from self.content

        Returns:
            home (str): home team tricode
            away (str): away team tricode
            date (str): date string
        """
        game_data = json.loads(self.content)['gameData']
        try:
            home = game_data['teams']['home']['triCode']
            away = game_data['teams']['away']['triCode']
            date = game_data['datetime']['dateTime']
        except KeyError:
            home, away, date = None, None, None
        return home, away, date

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlGameDiffPatchApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL diffPatch API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    season : str
        8 character representation of an NHL season (e.g. 20202021)
    gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)
    start_timecode : str
        the API will respond with plays from the designated game that were recorded after
        the given timecode

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    # desc: ClassVar[str] = 'NHL API - Game DiffPatch'
    # name: ClassVar[str] = 'NHL_API_DIFF'
    season: str
    gamePk: str
    start_timecode: str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/game/'
                    f'{self.season[:4]}'
                    '0'
                    f'{self.gamePk}'
                    '/feed/live/diffPatch')
        self.query = {'startTimecode': self.start_timecode}
        # noinspection PyTypeChecker
        self.local_path = os.path.join(self.local_path_stub,
                                       (f'{self.season[:4]}{self.gamePk}-',
                                        f'{self.start_timecode}_DF'))

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlScheduleApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL schedule API
    If no attributes are specified, the API will return today's games

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    date : str
        single date for the season_query (e.g. 2021-03-17)
    start_date : str
        start date for a date range season_query
    end_date : str
        end date for  date range season_query
    season : str
        8 character representation of an NHL season (e.g. 20202021)
    team_id : str
        one or more 2 character ID numbers representing NHL teams
        TODO: implement either API request to go from team name to ID number or
              just hardcode it somewhere
    game_type : str
        character code for different game types (e.g. R for regular, P for playoffs)
        all options listed here: https://statsapi.web.nhl.com/api/v1/gameTypes
    expand : str
        descriptor that provides additional information with the response
        'broadcasts' shows broadcast information, 'linescore' shows the line score,
        'tickets' shows ticketing information
    filename : str
        filename for content to be saved in self.local_path_stub
        default value is 'schedule'

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    # desc: ClassVar[str] = 'NHL API - Schedule'
    # name: ClassVar[str] = 'NHL_API_SCHEDULE'
    date: str = field(default='', init=True)
    start_date: str = field(default='', init=True)
    end_date: str = field(default='', init=True)
    season: str = field(default='', init=True)
    team_id: str = field(default='', init=True)
    game_type: str = field(default='', init=True)
    expand: str = field(default='', init=True)
    filename: str = field(default='schedule', init=True)

    def __post_init__(self):
        self.url = f'{self.url_stub}/schedule/'
        self.query = {'date': self.date,
                      'startDate': self.start_date,
                      'endDate': self.end_date,
                      'season': self.season,
                      'teamID': self.team_id,
                      'gameType': self.game_type,
                      'expand': f'schedule.{self.expand}'}
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.filename}')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyUnresolvedReferences
@dataclass
class NhlExpandsApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL API endpoint for
    expands options

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI


    Methods
    -------
    None
    """
    desc: ClassVar[str] = 'NHL API - Expands Options'

    def __post_init__(self):
        self.url = f'{self.url_stub}/expands/'
        self.query = {}
        self.local_path = ''
        self.fetch_content()

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyAbstractClass
# noinspection PyUnresolvedReferences
@dataclass
class NhlFranchiseApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL franchises API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    franchise_id : int
        franchise id number for the NHL API query

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL API - Franchise'
    name: ClassVar[str] = 'NHL_API_FRANCHISE'
    franchise_id: str = ''

    def __post_init__(self):
       self.url = (f'{self.url_stub}'
                   '/franchises/'
                   f'{self.franchise_id}')
       self.local_path = os.path.join(self.local_path_stub,
                                      f'{self.franchise_id}_FRANCHISE')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError

# noinspection PyAbstractClass
# noinspection PyUnresolvedReferences
@dataclass
class NhlTeamApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL teams API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    team_id : int
        team id number for the NHL API query

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL API - Team'
    name: ClassVar[str] = 'NHL_API_TEAM'
    team_id: str = ''

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/teams/'
                    f'{self.team_id}')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.team_id}_TEAM')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyAbstractClass
# noinspection PyUnresolvedReferences
@dataclass
class NhlPeopleApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL people API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    person_id : int
        person id number for the NHL API query

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL API - People'
    name: ClassVar[str] = 'NHL_API_PEOPLE'
    person_id : str

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/people/'
                    f'{self.person_id}')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.person_id}_PERSON')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyAbstractClass
# noinspection PyUnresolvedReferences
@dataclass
class NhlDivisionApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL divisions API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    division_id : int
        division id number for the NHL API query

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL API - Divisions'
    name: ClassVar[str] = 'NHL_API_DIVISIONS'
    division_id: str = ''

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/divisions/'
                    f'{self.division_id}')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.division_id}_DIVISION')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError


# noinspection PyAbstractClass
# noinspection PyUnresolvedReferences
@dataclass
class NhlConferenceApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL conferences API

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    conference_id : int
        conference id number for the NHL API query

    Methods
    -------
    validate_content():
        validate self.content fetched and record result in self.integrity
    """
    desc: ClassVar[str] = 'NHL API - Conference'
    name: ClassVar[str] = 'NHL_API_CONFERENCE'
    conference_id: str = ''

    def __post_init__(self):
        self.url = (f'{self.url_stub}'
                    '/conferences/'
                    f'{self.conference_id}')
        self.local_path = os.path.join(self.local_path_stub,
                                       f'{self.conference_id}_CONFERENCE')

    def validate_content(self):
        """
        Validate self.content and record result in self.integrity

        Returns:
            self
        """
        raise NotImplementedError

    def parse_to_csv(self):
        raise NotImplementedError
