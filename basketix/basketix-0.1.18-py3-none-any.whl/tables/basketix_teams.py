"""Basketix teams table"""

from .dynamodb_table import DynamoDBTable

class BasketixTeamsTable(DynamoDBTable):
    def __init__(self, environment: str):
        DynamoDBTable.__init__(self, 'basketix-teams', environment,  'weekId', 'teamId')
