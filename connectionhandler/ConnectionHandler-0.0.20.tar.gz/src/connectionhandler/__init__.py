from .get_handler import get_handler

def create_handler(db_type):
    return get_handler(db_type)