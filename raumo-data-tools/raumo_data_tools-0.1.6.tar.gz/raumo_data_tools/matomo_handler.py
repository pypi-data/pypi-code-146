from sqlalchemy import create_engine
from raumo_data_tools.config_handler import ConfigHandler

class MatomoHandler():
    def __init__(self, config_name):
        """init all dataframes
        """
        config = ConfigHandler(config_name)
        self.host = config.HOST
        self.user = config.USER
        self.pw = config.PW
        self.db_name = config.DB
        self.connect()

    def connect(self):
        connection_string = 'mysql+pymysql://' + self.user + ':' + self.pw + '@' + self.host + '/' + self.db_name
        self.db = create_engine(connection_string)
        return self.db