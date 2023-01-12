import requests

from .config import BASEURL, Config
from .fun import season_check


class Rankings:
    def __init__(self, season: int = 2023):
        """Initialize the class."""
        self.season = season
        self.headers = {"Authorization": f"Basic {Config.api_key}"}
        self.payload = {}
    # class DistrictRankingCalculation
    # def qual_performance_points(self, tournament_type: str,
    #                             qualification_rank: int, teams_at_event: int,
    #                             season: int = None) -> int:
    #     """
    #     This function returns the qual performance points for a given team.

    #     TournamentType: The type of tournament the team is in.
    #     Ex: "DistrictEvent" or "Championship" check docs for all of the types.  # noqa: E501

    #     qualificationRank: The rank of the team in the qual.

    #     teamsAtEvent: The number of teams at the event.
    #     """
    #     season = season_check(self.season, season)
    #     url_args = f"&tournamentType={tournament_type}&qualificationRank={qualification_rank}&teamsAtEvent={teams_at_event}"  # noqa: E501
    #     url = f"{BASEURL}{season}/rankings/district/qualPerformanceCalculation?{url_args}"  # noqa: E501

    #     response = requests.request("GET", url, headers=self.headers,
    #                                 data=self.payload)
    #     return int(response.text)

    # def alliance_selection_points(self, tournament_type: str,
    #                               number_of_alliances: int | str,
    #                               alliance_number: int, alliance_role: str,
    #                               season: int = None) -> int:
    #     """
    #     This function returns the alliance selection points for a given team.

    #     TournamentType: The type of tournament the team is in.
    #     Ex: "DistrictEvent" or "Championship" check docs for all of the types.  # noqa: E501

    #     NumberOfAlliances: The number of alliances.
    #     Ex: "Two", "Four",  "Six", "eight", "Sixteen"

    #     allianceNumber: What playoff alliance the team is on

    #     allianceRole: What role the team is in the alliance.
    #     Ex: "Captain", "Round1-3", "Backup" or "None"
    #     """
    #     season = season_check(self.season, season)

    #     url_args = f"&tournamentType={tournament_type}&sizeType={str(number_of_alliances) + 'Alliance'}&allianceNumber={alliance_number}&allianceRole={alliance_role}"  # noqa: E501
    #     url = f"https://frc-api.firstinspires.org/v3.0/{season}/rankings/district/allianceSelectionCalculation?{url_args}"  # noqa: E501

    #     response = requests.request("GET", url, headers=self.headers,
    #                                 data=self.payload)
    #     return int(response.text)

    # def playoff_advancement_points(self, tournament_type: str,
    #                                quarter_final_wins: int,
    #                                semi_final_wins: int, final_wins: int,
    #                                season: int = None) -> int:
    #     """
    #     might be down test later
    #     This function returns the playoff advancement points for a given team.  # noqa: E501

    #     tournamentType: The type of tournament the team is in.
    #     Ex: "DistrictEvent" or "Championship" check docs for all of the types.  # noqa: E501

    #     quarterFinalWins: The number of quarter finals the team has won.

    #     semiFinalWins: The number of semi finals the team has won.

    #     finalWins: The number of finals the team has won.
    #     """

    #     season = season_check(self.season, season)
    #     url_args = f"&tournamentType={tournament_type}&quarterFinalWins={quarter_final_wins}&semiFinalWins={semi_final_wins}&finalWins={final_wins}"  # noqa: E501
    #     url = f"{BASEURL}{season}/rankings/district/playoffAdvancementCalculation?{url_args}"  # noqa: E501

    #     response = requests.request("GET", url, headers=self.headers,
    #                                 data=self.payload)
    #     return response.text

    def event_rankings(self, event_code: str, team_number: int = None,
                       top: int = None, season: int = None) -> dict:
        """
        This function returns the rankings of a event.

        event_code: The event code of the event.

        Team_number: The team number of the team.

        top: The number of teams to return.
        """
        season = season_check(season, self.season)

        if team_number and top:
            raise ValueError("Can't use team_number and top at the same time.")
        url_args = f"&teamNumber={team_number}&top={top}"
        url = f"{BASEURL}{season}/rankings/{event_code}?{url_args}"  # noqa: E501

        response = requests.request("GET", url, headers=self.headers,
                                    data=self.payload)
        print(url)
        return response.json()

    def district_rankings(self, district_code: str = "",
                          team_number: int = None, top: int = None,
                          page: int | list = "", page_min: int = 1,
                          page_max: int = None, season: int = None) -> dict | list:  # noqa: E501
        """
        District: The district you want to get the rankings for.
        Ex: "NE" or "ONT"

        teamNumber: The team number of the team.

        page: The page of the rankings you want to get.
        Can't be used with top.

        top: The number of teams to return.
        Can't be used with page.
        """

        if team_number and any([top, page, district_code]):
            print(team_number, top, page, district_code)
            raise ValueError("Can't use team_number and any other arguments at the same time.")  # noqa: E501

        elif top and page != "":
            raise ValueError("Can't use top and page at the same time.")

        season = season_check(season, self.season)
        url_args = f"&districtCode={district_code}&teamNumber={team_number}&top={top}"  # noqa: E501

        if type(page) == int:
            url_args += f"&page={page}"

        elif type(page) == str:
            data = []
            if page_max is None:
                url = f"{BASEURL}{season}/rankings/district?{url_args}&page=1"
                response = requests.request("GET", url, headers=self.headers,
                                            data=self.payload)
                print(url)
                response_json = response.json()
                page_max = response_json["pageTotal"]
                on_page = response_json["rankingCountPage"]
                if page_max == 1 or on_page == top:
                    return response_json

            for page in range(page_min, page_max + 1):
                url = f"{BASEURL}{season}/rankings/district?{url_args}&page={page}"  # noqa: E501
                response = requests.request("GET", url, headers=self.headers,
                                            data=self.payload)
                data.append(response.json())
            return data

        elif type(page) == list:
            data = []
            for i in page:
                url = f"{BASEURL}{season}/rankings/district?{url_args}&page={i}"  # noqa: E501
                response = requests.request("GET", url, headers=self.headers,
                                            data=self.payload)
                data.append(response.json())
            return data

        else:
            raise TypeError("page must be an int, str, or list")

        url = f"{BASEURL}{season}/rankings/district?{url_args}"
        response = requests.request("GET", url, headers=self.headers,
                                    data=self.payload)
        print(url)
        return response.json()
