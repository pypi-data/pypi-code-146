"""Basketix free agencies table"""

from .dynamodb_table import DynamoDBTable

class BasketixFreeAgenciesTable(DynamoDBTable):
    def __init__(self, environment):
        DynamoDBTable.__init__(self, 'basketix-free-agencies', environment, 'seasonId', 'freeAgentId')
