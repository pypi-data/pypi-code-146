"""NBA games module"""

from typing import List, Optional, Dict

from boto3.dynamodb.conditions import Key

from ..tables import NbaGamesTable
from ..entities import BasketixWeek, BasketixDate
from ..models import NbaGameModel, NbaGameStatus

class NbaGamesHandler:
    """Handle NBA games."""

    def __init__(self, environment: str):
        """Init NBA games handler."""

        self.nba_games_table = NbaGamesTable(environment=environment)

    def get_game_info(self, game_id: str) -> NbaGameModel:
        """Get game information from database."""

        game = self.nba_games_table.query(game_id)[0]

        return game

    def get_game_date(self, game_id: str) -> str:
        """Returns date of a game"""

        return self.get_game_info(game_id=game_id)['gameDate']

    def get_all_games_of_day(self, date: str) -> List[NbaGameModel]:
        """Get all games for a specific date."""

        week = BasketixWeek.from_date(date)

        return self.nba_games_table.query(Key('weekId').eq(week.id) & Key('gameDate').eq(date), index_name='nba-games-table-secondary-index')

    def get_all_finished_games_of_day(self, date: str) -> List[NbaGameModel]:
        """Get all finished games for a specific date."""

        return [game for game in self.get_all_games_of_day(date) if self.is_finished(game=game)]

    def get_all_game_ids_of_day(self, date: str) -> List[str]:
        """Get all game ids for a specific date."""

        return [game['gameId'] for game in self.get_all_games_of_day(date=date)]

    def is_finished(self, game_id: Optional[str] = None, game: Optional[NbaGameModel] = None) -> bool:
        """Returns if game is finish or not"""

        if not game:

            if not game_id:
                raise Exception('One of game_id or game should be defined')

            game = self.get_game_info(game_id)

        return game['gameStatus'] == NbaGameStatus.FINISHED

    def get_all_games_of_week_for_team(self, team_id: str, week_id: str) -> List[NbaGameModel]:
        """Returns all games for a specific week and team"""

        games = self.get_all_games_of_week(week_id)

        return [game for game in games if team_id in game['teamIds']]

    def get_game_info_for_team(self, game: NbaGameModel, team_id: str) -> dict:
        """Returns game basic info with the scope of team_id"""

        return {
            'gameId': game['gameId'],
            'gameDate': game['gameDate'],
            'gameStatus': game['gameStatus'],
            'startTimeUTC': game['gameId'],
            'isHome': [team['location'] for team in game['teams'] if team['teamId'] == team_id][0] == 'home',
            'isAway': [team['location'] for team in game['teams'] if team['teamId'] == team_id][0] == 'away',
            'opponentId': [_id for _id in game['teamIds'] if _id != team_id][0],
        }

    def get_all_games_of_week(self, week_id: str) -> List[NbaGameModel]:
        """Get all game for a specific week."""

        return self.nba_games_table.query(Key('weekId').eq(week_id), index_name='nba-games-table-secondary-index')

    def get_last_finished_game(self, team_ids: List[str], max_occurrence: int = 7) -> Dict[str, NbaGameModel]:
        """Returns for each team id the last finished game, if any"""

        last_game_by_team = {}
        team_ids_set = set(team_ids)

        occurrence = 0
        cursor_date = BasketixDate.today()
        while occurrence <= max_occurrence and team_ids_set - set(last_game_by_team):
            games = self.get_all_finished_games_of_day(date=cursor_date.date)
            last_game_by_team = {
                **last_game_by_team,
                **{team_id: game for game in games for team_id in game['teamIds'] if team_id not in last_game_by_team}
            }

            cursor_date = cursor_date.day_before
            occurrence += 1

        return last_game_by_team
