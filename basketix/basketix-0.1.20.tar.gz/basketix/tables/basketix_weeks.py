"""Basketix weeks table"""

from .dynamodb_table import DynamoDBTable

class BasketixWeeksTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-weeks', environment, 'weekId')
