"""Basketix leagues table"""

from .dynamodb_table import DynamoDBTable

class BasketixLeaguesTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-leagues', environment, 'leagueId')
