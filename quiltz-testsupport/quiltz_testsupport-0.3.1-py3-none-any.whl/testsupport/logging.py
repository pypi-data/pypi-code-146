import pytest
from hamcrest import assert_that, has_item
import logging
from logging import Handler, INFO


@pytest.fixture
def log_collector():
    collector = LogCollector.create()
    yield collector
    collector.remove()


class LogCollector(Handler):
    @staticmethod
    def create():
        collector = LogCollector()
        logging.getLogger().addHandler(collector)
        logging.getLogger().setLevel(INFO)
        return collector

    def __init__(self):
        super().__init__()
        self.records = []
    
    def emit(self, record):
        self.records.append((record.levelname, record.getMessage()))

    def assert_warning(self, expected_message):
        assert_that(self.records, has_item(('WARNING', expected_message)))

    def assert_info(self, expected_message):
        assert_that(self.records, has_item(('INFO', expected_message)))

    def remove(self):
        logging.getLogger().removeHandler(self)
