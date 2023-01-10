from .connectiontypes.database_handler import Database_Handler

def get_handler(db_type):
    return Database_Handler(db_type)