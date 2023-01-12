import logging
import sys

import sqlalchemy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Connection:

    def __init__(self, user, pwd, host, db):
        assert isinstance(user, str)
        assert isinstance(pwd, str)
        assert isinstance(host, str)
        assert isinstance(db, str)
        self.user = user
        self.pwd = pwd
        self.host = host
        self.db = db

    def create_sql_engine(self, sql_logging=False):
        try:
            logging.info(f'Connecting to {self.db} on host {self.host}')
            conn_str = f'mysql+mysqlconnector://{self.user}:{self.pwd}@{self.host}/{self.db}'
            sql_engine = sqlalchemy.create_engine(conn_str, echo=sql_logging)
            return sql_engine
        except Exception as ex:
            logging.error(str(ex))
            sys.exit(1)
