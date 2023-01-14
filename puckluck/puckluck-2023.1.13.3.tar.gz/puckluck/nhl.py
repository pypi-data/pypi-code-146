# imports
import requests
import pandas as pd


def games_range(start="2022-10-01", end="2022-10-27"):
    """Uses the NHL stats api to get the games over the range of dates supplied

    Args:
        start (str, optional): Start date. Defaults to '2022-10-01'.
        end (str, optional): End Date. Defaults to '2022-10-27'.

    Returns:
        pd.DataFrame: DataFrame of the games over the window of start and end.
    """

    URL = "https://statsapi.web.nhl.com/api/v1/schedule"
    params = {"startDate": start, "endDate": end}
    resp = requests.get(URL, params=params)
    dates = resp.json()["dates"]
    game_data = []
    for date in dates:
        for game in date["games"]:
            parsed = pd.json_normalize(game)
            parsed.columns = parsed.columns.str.replace(".", "_", regex=True)
            parsed_dict = parsed.to_dict(orient="records")
            game_data.append(
                parsed_dict[0]
            )  # even though one game, records is a list of a single dict
    games = pd.DataFrame(game_data)
    return games


def get_pbp(gid="2022020111"):
    """Get the PBP JSON for a single Game Id

    Args:
        gid (str, optional): The game id. Defaults to '2022020111'.

    Returns:
        dict: The PBP JSON as a dictionary
    """
    URL = f"http://statsapi.web.nhl.com/api/v1/game/{gid}/feed/live"
    resp = requests.get(URL)
    pbp = resp.json()
    return pbp


def parse_livedata(pbp):
    livedata = pbp["liveData"]
    box = livedata["boxscore"]
    # parse refs
    refs = pd.json_normalize(box["officials"])
    refs.columns = refs.columns.str.replace(".", "_", regex=True)
    # parse the team boxscore data
    teams = box["teams"]
    teams["away"].keys()
