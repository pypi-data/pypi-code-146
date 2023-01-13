"""Basketix user temp table"""

from .dynamodb_table import DynamoDBTable

class BasketixUsersTempTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-users-temp', environment, 'confirmationCode', 'email')
