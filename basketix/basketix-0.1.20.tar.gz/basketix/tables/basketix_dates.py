"""Basketix dates table"""

from .dynamodb_table import DynamoDBTable

class BasketixDatesTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-dates', environment, 'date')
