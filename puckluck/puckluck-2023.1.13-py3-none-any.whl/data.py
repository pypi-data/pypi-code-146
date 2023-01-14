# imports
import requests
import pandas as pd


def nhl_games(season=202122):
    """Get the list of games from Nice Time on Ice API

    Args:
        season (int, optional): The season identifier. Defaults to 202122.
    """
    # build the url for Nice time on Ice API
    URL = f"http://www.nicetimeonice.com/api/seasons/{season}/games"
    # get the games
    games = requests.get(URL).json()
    # put into a dataframe
    df = pd.DataFrame(games)
    df.columns = df.columns.str.lower()
    # return
    return df


def nhl_games_range(start="2022-10-01", end="2022-10-27"):
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


def nhl_get_pbp(gid="2022020111"):
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


# def nhl_parse_gamedata(pbp):
#     # gamedata = pbp['gameData']
#     # gid = pbp.get('gamePk')
#     # startend = pd.json_normalize(gamedata['datetime'])
#     # teams = [team for team in gamedata['teams']
#     pass


def nhl_parse_livedata(pbp):
    livedata = pbp["liveData"]
    box = livedata["boxscore"]
    # parse refs
    refs = pd.json_normalize(box["officials"])
    refs.columns = refs.columns.str.replace(".", "_", regex=True)
    # parse the team boxscore data
    teams = box["teams"]
    teams["away"].keys()
