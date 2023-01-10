#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from app.api import Api
from app.application import Application
from app.login import is_licensed, login
from app.logz import create_logger

sys.path.append("..")  # Adds higher directory to python modules path.


class Test_Login:
    logger = create_logger()

    def test_init(self):
        """simple init test"""
        with open("init.yaml", "r") as f:
            data = f.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_login(self):
        """Simple login test"""
        app = Application()
        self.logger.debug(os.getenv("REGSCALE_USER"))
        self.logger.debug(os.getenv("REGSCALE_PASSWORD"))

        jwt = login(os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=app)
        self.logger.info(jwt)
        assert jwt is not None

    def test_application(self):
        """simple test of config"""
        app = Application()
        config = app.config
        assert "domain" in config
        assert "token" in config

    def test_license(self):
        app = Application()
        license = is_licensed(app)
        assert license
