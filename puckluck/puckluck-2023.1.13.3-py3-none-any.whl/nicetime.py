import pandas as pd
import requests


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


# def nhl_parse_gamedata(pbp):
#     # gamedata = pbp['gameData']
#     # gid = pbp.get('gamePk')
#     # startend = pd.json_normalize(gamedata['datetime'])
#     # teams = [team for team in gamedata['teams']
#     pass
