"""Basketix seasons table"""

from .dynamodb_table import DynamoDBTable

class BasketixSeasonsTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-seasons', environment, 'seasonId')
