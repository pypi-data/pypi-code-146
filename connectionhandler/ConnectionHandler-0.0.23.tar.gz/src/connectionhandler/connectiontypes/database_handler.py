from .postgres_handler import Postgres_Handler as pg_handler

class Database_Handler:
    def __init__(self, db_type, user_name, password, host, port,database):
        self.db_type = db_type
        self.__build_connection(user_name, password, host, port,database)

    def __build_connection(self, user_name, password, host, port, database):
        self.handler = pg_handler(user_name, password, host, port, database)
    
    def add_sql_props(self, columns, keywords, base_query):
        self.handler.define_columns(columns)
        self.handler.set_base_query(base_query)
        self.handler.set_keywords(keywords)
    
    def search_records(self):
        return self.handler.search_for_records()