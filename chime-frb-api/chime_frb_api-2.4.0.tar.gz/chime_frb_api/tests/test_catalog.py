#!/usr/bin/env python

import requests

from chime_frb_api.backends import frb_master

master = frb_master.FRBMaster(debug=True, base_url="http://localhost:8001")

TEST_CATALOG = {
    "version": "1",
    "locked": False,
    "events": [{"event_number": 9386707, "ra": 0.0, "dec": 0.0}],
}


def test_get_catalog():
    response = requests.post("http://localhost:8001/make-catalog", json=TEST_CATALOG)
    assert response.status_code == 200
    catalog = master.catalog.get_catalog(version=1)
    assert (
        catalog["events"][0]["event_number"]
        == TEST_CATALOG["events"][0]["event_number"]
    )
