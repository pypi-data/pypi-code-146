import logging
from os.path import isfile, splitext, basename

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Trigger:

    def __init__(self, trigger_filepath, session_instance):
        assert isfile(trigger_filepath)
        assert hasattr(session_instance, 'execute')

        self.trigger_filepath = trigger_filepath
        self.session_instance = session_instance
        self.trigger_name = splitext(basename(self.trigger_filepath))[0]

    def drop_and_create_trigger(self):
        self.drop_trigger_if_exists()
        self.create_trigger()

    def drop_trigger_if_exists(self):
        drop_sql = f'DROP TRIGGER IF EXISTS {self.trigger_name};'
        logging.info(drop_sql)
        self.session_instance.execute(drop_sql)

    def create_trigger(self):
        with open(self.trigger_filepath, 'r') as reader:
            create_sql = reader.read()
            logging.info(create_sql)
            self.session_instance.execute(create_sql)
