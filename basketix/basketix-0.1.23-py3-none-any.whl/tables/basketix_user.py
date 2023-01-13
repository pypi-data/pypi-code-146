"""Basketix user table"""

from .dynamodb_table import DynamoDBTable

class BasketixUsersTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-users', environment, 'basketixId', 'email')
