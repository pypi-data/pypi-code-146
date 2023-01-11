# api_main.py - Main FastAPI application.
# Copyright (C) 2022 Tranxpert.
# This program runs an API for the Tranxpert's messaging service using FastAPI.
# It contains one endpoint for sending messages using the Twilio API and WhatsApp API.

# ----- Run the application -----
# $ uvicorn main:app --reload
# ----- Documentation -----
# http://127.0.0.1:8000/docs (local)

# ----- Imports -----

import uvicorn
from fastapi import FastAPI, Depends
from txp.common.utils.bigquery_utils import (
    get_authenticated_client as get_bigquery_authenticated_client,
)

from utils.authentication import get_current_username
from utils.database_utils import get_gcloud_credentials_from_file, CREDENTIALS_PATH
from utils.models import DialogFlowRequest, DialogFlowResponse
from utils.response_manager import response_builder

HARDCODED_TABLE = "ml_events_and_states.states"

credentials = get_gcloud_credentials_from_file(CREDENTIALS_PATH)
bigquery_client = get_bigquery_authenticated_client(credentials)
# bigquery_client = bigquery.Client()


app = FastAPI()


@app.get("/users/me")
async def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.post("/dialogflow-webhook")
async def dialogflow_request(
    request: DialogFlowRequest, username: str = Depends(read_current_user)
):
    response_text = await response_builder(request, HARDCODED_TABLE, bigquery_client)
    response = DialogFlowResponse(fulfillmentText=response_text, source="webhookdata")

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
