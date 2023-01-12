import json
import re
from abc import ABC
from datetime import datetime
from typing import ClassVar, TypeVar

from pandas import DataFrame
import pydantic
import requests

from dry_scraper.data_sources.nhl.pydantic_models import (
    nhl_game_live_feed_api_source,
    nhl_game_content_api_source,
    nhl_people_api_source,
    nhl_schedule_api_source,
    nhl_teams_api_source,
    nhl_divisions_api_source,
    nhl_conferences_api_source,
)
from dry_scraper.data_sources.data_source import DataSource


DataModel = TypeVar("DataModel", bound=pydantic.BaseModel)


class NhlApiSource(DataSource, ABC):
    """
    Abstract subclass of DataSource that represents a request and result from NHL API.
    API fully documented here: https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md

    ...

    Attributes
    ----------
    _url_stub : ClassVar[str]
        partial URL location of data source
    _extension : ClassVar[str]
        file extension to be used when writing the raw data source to disk e.g. json, HTM
    _pyd_model : DataModel
        pydantic model class describing the response
    _url : str
        fully qualified URL location of data source, completed on instantiation
    _query : dict
        dict representation of API query
    _content : str
        string representation of raw data retrieved by fetch_content()
    _content_pyd : DataModel
        pydantic model representation of the requested data created on call to parse_to_pyd()

    Methods
    -------
    fetch_content(): -> Self:
        fetch content from self.url and store response in self.content
    parse_to_pyd(): -> Self:
        Parse content into pydantic model and store result in self.content_pyd
    """

    _url_stub: ClassVar[str] = "https://statsapi.web.nhl.com/api/v1"
    _extension: ClassVar[str] = "json"
    _pyd_model: ClassVar[DataModel]
    _url: str
    _query: dict
    _content: str
    _content_pyd: DataModel

    @property
    def query(self) -> dict | None:
        return getattr(self, "_query", None)

    @query.setter
    def query(self, value: dict) -> None:
        self._query = value

    @property
    def pyd_model(self) -> DataModel:
        return self._pyd_model

    def parse_to_pyd(self):  # -> Self:
        """
        Parse content into a Pydantic model and store result in self.content_pyd

        Returns:
        self
        """
        self._content_pyd = self.pyd_model.parse_raw(self.content)

    def fetch_content(self):
        """
        Query NHL API endpoint at self.url and store response in self.content

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


class NhlGameApiSource(NhlApiSource, ABC):
    """
    Abstract subclass of NhlApiSource that represents a request from an NHL Game API

    ...

    Attributes
    ----------
    _season : str
        8 character representation of an NHL season (e.g. 20202021)
    _gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)

    Methods
    -------
    """

    _season: str
    _gamePk: str

    def __init__(self, season: str | int, gamePk: str | int) -> None:
        self.season = season
        self.gamePk = gamePk

    @property
    def season(self) -> str:
        return self._season

    @season.setter
    def season(self, value: int | str) -> None:
        self._season = str(value)

    @property
    def gamePk(self) -> str:
        return self._gamePk

    @gamePk.setter
    def gamePk(self, value: int | str) -> None:
        self._gamePk = str(value)


class NhlGameBoxScoreApiSource(NhlGameApiSource):
    """
    Subclass of NhlGameApiSource that represents a request from the NHL box score API

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response


    Methods
    -------
    """

    _pyd_model: ClassVar[DataModel] = nhl_game_live_feed_api_source.BoxScore

    def __init__(self, season: str | int, gamePk: str | int) -> None:
        super().__init__(season, gamePk)
        self.url = (
            f"{self.url_stub}"
            "/game/"
            f"{self.season[:4]}"
            "0"
            f"{self.gamePk}"
            "/boxscore"
        )


class NhlGameLineScoreApiSource(NhlGameApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL line score API

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response


    Methods
    -------
    """

    _pyd_model: ClassVar[DataModel] = nhl_game_live_feed_api_source.LineScore

    def __init__(self, season: str | int, gamePk: str | int) -> None:
        super().__init__(season, gamePk)
        self.url = (
            f"{self.url_stub}"
            "/game/"
            f"{self.season[:4]}"
            "0"
            f"{self.gamePk}"
            "/linescore"
        )


class NhlGameContentApiSource(NhlGameApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL content API

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response


    Methods
    -------
    """

    _pyd_model: ClassVar[DataModel] = nhl_game_content_api_source.GameContent

    def __init__(self, season: str | int, gamePk: str | int) -> None:
        super().__init__(season, gamePk)
        self.url = (
            f"{self.url_stub}"
            "/game/"
            f"{self.season[:4]}"
            "0"
            f"{self.gamePk}"
            "/content"
        )


class NhlGameLiveFeedApiSource(NhlGameApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL live feed API

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response

    Methods
    -------
    yield_teams_and_date() -> (str, str, str):
        return home and away tricodes and date string of game from self.content
        used by NhlEspnPbpXmlSource to determine ESPN game code
    """

    _pyd_model: ClassVar[DataModel] = nhl_game_live_feed_api_source.LiveFeed

    def __init__(self, season: str | int, gamePk: str | int) -> None:
        super().__init__(season, gamePk)
        self.url = (
            f"{self.url_stub}"
            "/game/"
            f"{self.season[:4]}"
            "0"
            f"{self.gamePk}"
            "/feed/live"
        )

    def yield_teams_and_date(self) -> (str, str, str):
        """
            Return home and away tricodes and date string of game from self.content

        Returns:
            home (str): home team tricode
            away (str): away team tricode
            date (str): date string
        """
        game_data = json.loads(self.content)["gameData"]
        try:
            home = game_data["teams"]["home"]["triCode"]
            away = game_data["teams"]["away"]["triCode"]
            date = game_data["datetime"]["dateTime"]
        except KeyError:
            home, away, date = None, None, None
        return home, away, date


class NhlScheduleApiSource(NhlApiSource):
    """
    Subclass of NhlGameApiSource that represents a request from the NHL schedule API
    If no attributes are specified, the API will return today's games

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response
    _date : str
        single date for the season_query (e.g. 2021-03-17)
    _start_date : str
        start date for a date range season_query
    _end_date : str
        end date for  date range season_query
    _season : str
        8 character representation of an NHL season (e.g. 20202021)
    _team_id : str
        one or more 2 character ID numbers representing NHL teams separated by commas
        or one or more tricodes representing NHL teams separated by commas
        e.g. '1,2,3' or 'NJD,NYI,NYR'
    _game_type : str
        one or more character codes for different game types separated by commas
        (e.g. PR for preseason, R for regular, A for all-star, P for playoffs)
        all options listed here: https://statsapi.web.nhl.com/api/v1/gameTypes
    _expand : str
        descriptor that provides additional information with the response
        'broadcasts' shows broadcast information, 'linescore' shows the line score,
        'tickets' shows ticketing information
        all options listed here: https://statsapi.web.nhl.com/api/v1/expands

    Methods
    -------
    """

    _pyd_model: ClassVar[DataModel] = nhl_schedule_api_source.Schedule
    _date: str
    _start_date: str
    _end_date: str
    _season: str
    _team_id: str
    _game_type: str
    _expand: str

    def __init__(
        self,
        date=None,
        start_date=None,
        end_date=None,
        season=None,
        team_id=None,
        game_type=None,
        expand=None,
    ):
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.season = season
        self.team_id = team_id
        self.game_type = game_type
        self.expand = expand
        self.url = f"{self.url_stub}/schedule"
        query = {}
        if date:
            query["date"] = date
        if start_date:
            query["startDate"] = start_date
        if end_date:
            query["endDate"] = end_date
        if season:
            query["season"] = season
        if team_id:
            query["teamID"] = team_id
        if game_type:
            query["gameType"] = game_type
        if expand:
            query["expand"] = expand
        self.query = query

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str | datetime) -> None:
        if isinstance(value, datetime):
            self._date = value.strftime("%Y-%m-%d")
        else:
            self._date = value

    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, value: str | datetime) -> None:
        if isinstance(value, datetime):
            self._start_date = value.strftime("%Y-%m-%d")
        else:
            self._start_date = value

    @property
    def end_date(self) -> str:
        return self._end_date

    @end_date.setter
    def end_date(self, value: str | datetime) -> None:
        if isinstance(value, datetime):
            self._end_date = value.strftime("%Y-%m-%d")
        else:
            self._end_date = value

    @property
    def season(self) -> str:
        return self._season

    @season.setter
    def season(self, value: int | str) -> None:
        self._season = str(value)

    @property
    def team_id(self) -> str:
        return self._team_id

    @team_id.setter
    def team_id(self, value: int | str) -> None:
        """
        Set value of team_id by coercing the user input into the acceptable form of one or more team ID numbers
        Parameters
        ----------
        value : int | str
            an int representing one team ID, or a str representing multiple.
            str can be a comma delimited list of team ID numbers or tricodes.
        """
        num_pattern = re.compile(r"^(\d|\d\d)$|^(\d,|\d\d,)+(\d|\d\d)$")
        tri_pattern = re.compile(r"^[a-zA-Z]{3}$|^([a-zA-Z]{3},)+[a-zA-Z]{3}$")

        if isinstance(value, int) or num_pattern.match(str(value)):
            self._team_id = str(value)
        elif isinstance(value, str) and tri_pattern.match(value):
            tricode_list: list[str] = value.split(",")
            team_dict: dict[str, int] = NhlTeamsApiSource().create_team_dict()
            id_list: list[str] = []
            for team in tricode_list:
                team_id: int = team_dict.get(team, default=-1)
                if team_id != -1:
                    id_list.append(str(team_id))
            self._team_id = ",".join(id_list)
        else:
            self._team_id = ""

    @property
    def game_type(self) -> str:
        return self._game_type

    @game_type.setter
    def game_type(self, value: str) -> None:
        self._game_type = value

    @property
    def expand(self) -> str:
        return self._expand

    @expand.setter
    def expand(self, value: str) -> None:
        self._expand = value


class NhlTeamsApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL teams API

    ...

    Attributes
    ----------
    _team_id : int
        team id number for the NHL API query

    Methods
    -------
    create_team_dict -> dict[str, int]:
        Request the full list of NHL teams and return a dictionary associating tricodes
        to team ID numbers
    """

    _pyd_model: ClassVar[DataModel] = nhl_teams_api_source.Teams
    _team_id: str

    def __init__(self, team_id="") -> None:
        self.team_id = team_id
        self.url = f"{self.url_stub}" "/teams/" f"{self.team_id}"

    @property
    def team_id(self) -> str:
        return self._team_id

    @team_id.setter
    def team_id(self, value: str | int) -> None:
        self._team_id = str(value)

    @staticmethod
    def create_team_dict() -> dict[str, int]:
        """
        Request the full list of NHL teams and return a dictionary associating tricodes
        to team ID numbers.

        For now, use hardcoded version

        Returns:
        team_dict : dict[str:int]
            dictionary associating tricodes to team ID numbers
        """
        from dry_scraper.teams import TEAMS

        team_dict = {}

        for team in TEAMS:
            tricode = team["abbreviation"]
            id_number = team["id"]
            team_dict[tricode] = id_number

        return team_dict


class NhlPeopleApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL people API

    ...

    Attributes
    ----------
    _person_id : int
        person id number for the NHL API query

    Methods
    -------
    """

    _pyd_model: ClassVar[DataModel] = nhl_people_api_source.People
    _person_id: str

    def __init__(self, person_id) -> None:
        self.person_id = person_id
        self.url = f"{self.url_stub}" "/people/" f"{self.person_id}"

    @property
    def person_id(self) -> str:
        return self._person_id

    @person_id.setter
    def person_id(self, value: str | int) -> None:
        self._person_id = str(value)


class NhlDivisionApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL divisions API

    ...

    Attributes
    ----------
    _division_id : int
        division id number for the NHL API query

    Methods
    -------
    """

    _pyd_model: ClassVar[DataModel] = nhl_divisions_api_source.Divisions
    _division_id: str

    def __init__(self, division_id="") -> None:
        self.division_id = division_id
        self.url = f"{self.url_stub}" "/divisions/" f"{self.division_id}"

    @property
    def division_id(self) -> str:
        return self._division_id

    @division_id.setter
    def division_id(self, value: str | int) -> None:
        self._division_id = str(value)


class NhlConferenceApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL conferences API

    ...

    Attributes
    ----------
    _conference_id : int
        conference id number for the NHL API query

    Methods
    -------
    """

    _pyd_model: ClassVar[DataModel] = nhl_conferences_api_source.Conferences
    _conference_id: str

    def __init__(self, conference_id=""):  # -> Self:
        self.conference_id = conference_id
        self.url = f"{self.url_stub}" "/conferences/" f"{self.conference_id}"

    @property
    def conference_id(self) -> str:
        return self._conference_id

    @conference_id.setter
    def conference_id(self, value: str | int) -> None:
        self._conference_id = str(value)
