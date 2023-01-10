#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import requests
from app.application import Application
from app.logz import create_logger
from app.tenable import q_vuln


class Test_Tenable:
    """Test Tenable Integrations"""

    logger = create_logger()

    def test_init(self):
        """Init"""
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_tenable(self):
        """Make sure tenable values are present"""
        app = Application()
        config = app.config
        assert "tenable_access_key" in config
        assert "tenable_secret_key" in config

    def test_vulns(self):
        """
        Get Tenable scans
        """
        try:
            r = requests.get("https://sc.tenalab.online", verify=False, timeout=5)
            if r.status_code != 200:
                pytest.skip(f"Tenable is down..{r.status_code}")
        except Exception:
            pytest.skip("Tenable is down..")
        q_vuln(query_id=37009, ssp_id=2, create_issue=True)
        assert 1 == 1


# 51: [{'id': '685', 'name': 'addasset20200720_0322', 'description': 'desc', 'uuid': '099D5F6F-97C8-4551-8...F6ABF85821'}]

# Yesterday updated cli to lock certain functionality based on license level
# Tenable CLI dev site back up, so working on this
# Craig is testing appliance code, hopefully that will be done today.


# Working on matching tenable assets with what is in regscale and create a vulnerability report
