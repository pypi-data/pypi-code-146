"""NBA games table"""

from .dynamodb_table import DynamoDBTable
from ..models import NbaPlayerPerformanceModel

class NbaPlayersStatsTable(DynamoDBTable[NbaPlayerPerformanceModel]):
    def __init__(self, environment: str):
        DynamoDBTable.__init__(self, 'nba-players-stats', environment, 'playerId', 'gameDate')

class NbaPlayerPerformancesTable(DynamoDBTable[NbaPlayerPerformanceModel]):
    def __init__(self, environment: str):
        DynamoDBTable.__init__(self, 'nba-players-stats', environment, 'playerId', 'gameDate')
