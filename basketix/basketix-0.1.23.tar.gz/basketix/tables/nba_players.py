"""NBA players table"""

from .dynamodb_table import DynamoDBTable
from ..models import NbaPlayerModel

class NbaPlayersTable(DynamoDBTable[NbaPlayerModel]):
    def __init__(self, environment: str):
        DynamoDBTable.__init__(self, 'nba-players', environment, 'playerId')
