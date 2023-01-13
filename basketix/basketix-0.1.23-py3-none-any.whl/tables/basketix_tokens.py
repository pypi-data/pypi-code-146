"""Tokens table"""

from .dynamodb_table import DynamoDBTable

class TokensTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-tokens', environment, 'token')

class BasketixTokensTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-tokens', environment, 'token')
