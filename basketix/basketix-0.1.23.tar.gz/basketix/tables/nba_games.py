"""NBA games table"""

from .dynamodb_table import DynamoDBTable
from ..models import NbaGameModel

class NbaGamesTable(DynamoDBTable[NbaGameModel]):
    def __init__(self, environment: str):
        DynamoDBTable.__init__(self, 'nba-games', environment, 'gameId')
