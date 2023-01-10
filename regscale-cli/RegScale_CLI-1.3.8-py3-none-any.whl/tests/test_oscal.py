#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile

import requests

from app.api import Api
from app.application import Application
from app.login import login
from app.logz import create_logger
from app.oscal import process_component, upload_catalog, upload_profile
import pytest

sys.path.append("..")  # Adds higher directory to python modules path.


class Test_Oscal:
    """Oscal Test Class"""

    logger = create_logger()

    def test_init(self):
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    @pytest.mark.skip(reason="This test is way too slow atm.")
    def test_catalog(self):
        """Test Catalog Code"""
        app = Application()
        api = Api(app)
        self.logger.debug(os.getenv("REGSCALE_USER"))
        self.logger.debug(os.getenv("REGSCALE_PASSWORD"))
        if not os.path.exists("processing"):
            os.mkdir("processing")
        # Need a runner to allow click to work with pytest
        # Get fresh token
        login(os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=app)
        file_url = "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog-min.json"
        tmp_file = tempfile.NamedTemporaryFile()
        f = open(tmp_file.name, "w", encoding="utf-8")
        r = api.get(url=file_url, headers={})
        f.write(r.text)
        f.close()
        cat_name = r.json()["catalog"]["metadata"]["title"]
        # Pass default argument to click function
        self.logger.debug(f.name)

        Test_Oscal.upload_catalog(self, f.name)
        # delete extra data after we are finished
        Test_Oscal.delete_inserted_catalog(self, cat_name)
        self.logger.debug(cat_name)
        tmp_file.close()
        # shutil.rmtree('processing')
        # Test_Oscal.delete_inserted_catalog(cat_name)

    def test_profile(self):
        """Test Profile Code"""
        app = Application()
        api = Api(app)
        self.logger.debug(os.getenv("REGSCALE_USER"))
        self.logger.debug(os.getenv("REGSCALE_PASSWORD"))
        if not os.path.exists("processing"):
            os.mkdir("processing")
        # Need a runner to allow click to work with pytest
        # Get fresh token
        login(os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=app)
        file_url = "https://raw.githubusercontent.com/GSA/fedramp-automation/2229f10cc0b143410522026b793f4947eebb0872/dist/content/baselines/rev4/json/FedRAMP_rev4_HIGH-baseline_profile.json"
        tmp_file = tempfile.NamedTemporaryFile()
        f = open(tmp_file.name, "w", encoding="utf-8")
        r = api.get(url=file_url, headers={})
        f.write(r.text)
        f.close()
        prof_name = r.json()["profile"]["metadata"]["title"]
        # Pass default argument to click function
        self.logger.debug(f.name)

        Test_Oscal.upload_profile(self, file_name=f.name, title=prof_name)
        # delete extra data after we are finished
        Test_Oscal.delete_inserted_profile(self, prof_name)
        self.logger.debug(prof_name)
        tmp_file.close()
        # shutil.rmtree('processing')
        # Test_Oscal.delete_inserted_catalog(cat_name)

    def test_component(self):
        app = Application()
        api = Api(app)
        if not os.path.exists("processing"):
            os.mkdir("processing")
        login(os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=app)
        r = api.get(
            url="https://repo1.dso.mil/platform-one/big-bang/apps/sandbox/loki/-/raw/main/oscal-component.yaml",
            headers={},
        )
        assert r.text
        tmp_file = tempfile.NamedTemporaryFile()
        with open(tmp_file.name, "w", encoding="utf-8") as f:
            f.write(r.text)
        os.rename(tmp_file.name, tmp_file.name + ".yaml")
        filename = tmp_file.name + ".yaml"
        process_component(filename)

    def upload_profile(self, file_name, title):
        """Upload the catalog"""
        upload_profile(
            file_name=file_name, title=title, catalog="84", categorization="Moderate"
        )

    def upload_catalog(self, file_name):
        """Upload the catalog"""
        upload_catalog(file_name=file_name)

    def delete_inserted_catalog(self, cat_name):
        """delete catalog"""
        app = Application()
        api = Api(app)
        config = app.config
        headers = {
            "accept": "*/*",
            "Authorization": config["token"],
        }
        cats = api.get(
            url=config["domain"] + "/api/catalogues/getList", headers=headers
        ).json()
        delete_this_cat = sorted(
            [x for x in cats if x["title"] == cat_name],
            key=lambda d: d["id"],
            reverse=True,
        )[0]
        self.logger.info(delete_this_cat)
        response = api.delete(
            url=f"https://dev.regscale.com/api/catalogues/{delete_this_cat['id']}",
            headers=headers,
        )
        self.logger.info(headers)
        self.logger.info(response)

    def delete_inserted_profile(self, prof_name):
        """delete profile"""
        app = Application()
        api = Api(app)
        config = app.config
        headers = {
            "accept": "*/*",
            "Authorization": config["token"],
        }
        profs = api.get(
            url=config["domain"] + "/api/profiles/getList", headers=headers
        ).json()
        delete_this_prof = sorted(
            [x for x in profs if x["name"] == prof_name],
            key=lambda d: d["id"],
            reverse=True,
        )[0]
        self.logger.info(delete_this_prof)
        response = api.delete(
            url=f"https://dev.regscale.com/api/profiles/{delete_this_prof['id']}",
            headers=headers,
        )
        self.logger.info(headers)
        self.logger.info(response)
