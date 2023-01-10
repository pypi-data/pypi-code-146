from .get_handler import get_handler

def create_handler(db_type, username, password, port, host, database):
    return get_handler(db_type, username, password, port, host, database)