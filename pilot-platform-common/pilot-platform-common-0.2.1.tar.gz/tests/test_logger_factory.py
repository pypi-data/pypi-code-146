from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import pytest

from common.logger.logger_factory import LoggerFactory


@pytest.fixture
def logger_factory(faker, tmpdir):
    yield LoggerFactory(faker.slug(), logs_path=tmpdir)

def create_logs_at_all_levels(logger):
    logger.debug('Log entry with level error')
    logger.info('Log entry with level info')
    logger.warning('Log entry with level warning')
    logger.error('Log entry with level error')
    logger.critical('Log entry with level critical')

log_level_labels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class TestLoggerFactory:
    def test_logger_factory_creates_logs_folder_in_working_directory(self, monkeypatch, faker, tmpdir):
        folder = tmpdir.mkdtemp()
        monkeypatch.chdir(folder)
        expected_folder = folder / 'logs'

        LoggerFactory(faker.slug())

        assert Path(expected_folder).is_dir() is True

    def test_get_logger_returns_logger_with_expected_list_of_handlers(self, logger_factory):
        logger = logger_factory.get_logger()

        expected_handlers = [
            TimedRotatingFileHandler,
            StreamHandler,
            StreamHandler,
        ]

        for idx, expected_handler in enumerate(expected_handlers):
            assert isinstance(logger.handlers[idx], expected_handler) is True
    
    def test_get_logger_with_no_custom_log_levels(self, faker, caplog):
        logger = LoggerFactory(name=faker.slug()).get_logger()
        create_logs_at_all_levels(logger)
        assert len(caplog.records) == 5

    def test_get_logger_with_default_log_level_20(self, faker, caplog):
        logger = LoggerFactory(name=faker.slug(), level_default=20).get_logger()
        create_logs_at_all_levels(logger)
        for record in caplog.records:
            assert record.levelname not in log_level_labels[:1]
        assert len(caplog.records) == 4

    def test_get_logger_with_default_log_level_30(self, faker, caplog):
        logger = LoggerFactory(name=faker.slug(), level_default=30).get_logger()
        create_logs_at_all_levels(logger)
        for record in caplog.records:
            assert record.levelname not in log_level_labels[:2]
        assert len(caplog.records) == 3

    def test_get_logger_with_default_log_level_40(self, faker, caplog):
        logger = LoggerFactory(name=faker.slug(), level_default=40).get_logger()
        create_logs_at_all_levels(logger)
        for record in caplog.records:
            assert record.levelname not in log_level_labels[:3]
        assert len(caplog.records) == 2

    def test_get_logger_with_default_log_level_50(self, faker, caplog):
        logger = LoggerFactory(name=faker.slug(), level_default=50).get_logger()
        create_logs_at_all_levels(logger)
        for record in caplog.records:
            assert record.levelname not in log_level_labels[:4]
        assert len(caplog.records) == 1
