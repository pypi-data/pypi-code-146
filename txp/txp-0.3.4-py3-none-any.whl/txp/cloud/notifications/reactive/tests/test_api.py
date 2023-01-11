import json
import os
import sys

import pytest
from fastapi.testclient import TestClient
from twilio.rest import Client
from decouple import config

from ..api_main import app


if sys.version_info < (3, 10):
    pytest.skip("requires python3.10 or higher", allow_module_level=True)


TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
API_USERNAME = config("API_USERNAME")
API_PASSWORD = config("API_PASSWORD")
TEST_WHATSAPP_NUMBER = config("TEST_WHATSAPP_NUMBER")


client = TestClient(app)
f = open("tests/dialogflow_request_asset_state_whatsapp.json")
asset_current_state_data = json.load(f)
f.close()


@pytest.fixture()
def request_asset_current_state():
    headers = {"Content-Type": "application/json"}
    response = client.post(
        "/dialogflow-webhook",
        auth=(API_USERNAME, API_PASSWORD),
        headers=headers,
        json=asset_current_state_data,
    )
    return response


# @pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
def test_asset_current_state_ok(request_asset_current_state):
    assert request_asset_current_state.status_code == 200


# @pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
def test_asset_current_state_database_response(request_asset_current_state):
    assert (
        not (
            "fulfillmentText",
            "No encuentro ese activo o datos sobre él en las últimas 12 horas. Intenta de nuevo con otro nombre o contacta con nuestro servicio técnico.",
        )
        in request_asset_current_state.json().items()
    )


def test_twilio_api():
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = twilio_client.messages.create(
        body="El activo {} está actualmente en condición {}.".format(
            "nevera", "OPTIMA"
        ),
        from_="whatsapp:+18045342681",
        to=TEST_WHATSAPP_NUMBER,
    )

    assert message.status == "queued"
