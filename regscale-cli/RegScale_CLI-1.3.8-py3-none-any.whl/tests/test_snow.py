#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from app.application import Application
from app.logz import create_logger
from app.servicenow import sync_notes_to_regscale


class Test_Snow:
    """Test ServiceNow Integrations"""

    logger = create_logger()

    def test_init(self):
        """Init"""
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_snow(self):
        """Make sure values are present"""
        app = Application()
        config = app.config
        assert "snowPassword" in config
        assert "snowUserName" in config

    def test_sync(self):
        """
        Sync ServiceNow
        """
        sync_notes_to_regscale("74ad1ff3c611227d01d25feac2af603f")
        assert 1 == 1
