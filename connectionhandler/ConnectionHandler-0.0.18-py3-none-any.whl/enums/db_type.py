from enum import Enum

class Db_Type(Enum):
    POSTGRESQL = 1
    MYSQL = 2
    DYNAMODB = 3
    MSSQL = 4
    MONGO = 5
    
    