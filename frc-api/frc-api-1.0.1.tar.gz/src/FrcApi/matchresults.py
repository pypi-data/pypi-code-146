import requests

from .config import BASEURL, Config
from .fun import season_check


class MatchResults:
    def __init__(self, season: int = 2023) -> None:
        self.SEASON = season
        self.headers = {'Authorization': f'Basic {Config.api_key}'}
        self.payload = {}

    def score_details(self, event_code: str, match_level: str,
                      match_number: int = None, team_number: int = None,
                      start: int = None, end: int = None,
                      season: int = None) -> dict:
        """
        This function returns the score details for a given match.

        MatchLevel: If u want either a qual match or playoff.

        match_number: If u want the results for a specific match.

        TeamNumber: If u want the results for a specific team.

        Start: The start of the matches u want.

        End: The end of the matches u want.
        """
        season = season_check(season, self.SEASON)

        url_args = f"&match_number={match_number}&teamNumber={team_number}&start={start}&end={end}"  # noqa: E501
        url = f"{BASEURL}{season}/scores/{event_code}/{match_level}?{url_args}"
        if match_number and team_number:
            raise ValueError("You can't specify both match_number and team_number")  # noqa: E501

        if match_number and any([start, end]):
            raise ValueError("You can't specify both match_number and start or end")  # noqa: E501

        response = requests.request(
            "GET", url, headers=self.headers, data=self.payload)
        print(url)

        if match_number:
            response_json = response.json()
            data = response_json["MatchScores"][match_number - 1]
            return data

        return response.json()

    def event_match_results(self, event_code: str, match_level: str = None,
                            team_number: int = None, match_number: int = None,
                            start: int = None, end: int = None,
                            season: int = None) -> dict:
        """
        Returns the general details about a single or multiple matches.

        MatchLevel: If you want either a qual match or a playoff match.

        TeamNumber: If you want the results for a specific team.

        match_number: If you want the results for a specific match.

        Start: The start of the matches you want.

        End: The end of the matches you want.
        """

        if any([match_number, start, end]) and not match_level:
            raise ValueError("MatchLevel is required if match_number, start, or end is specified")  # noqa: E501

        elif match_number and any([team_number, start, end]):
            raise ValueError("You can't specify both match_number and team_number or start or end")  # noqa: E501

        url_args = f"teamNumber={team_number}&matchNumber={match_number}&start={start}&end={end}"  # noqa: E501
        if match_level:
            url_args += f"&tournamentLevel={match_level}"

        season = season_check(season, self.SEASON)

        url = f"{BASEURL}{season}/matches/{event_code}?{url_args}"

        response = requests.request("GET", url, headers=self.headers,
                                    data=self.payload)
        if match_number:
            response_json = response.json()
            data = response_json["Matches"][match_number - 1]
            return data

        return response.json()
