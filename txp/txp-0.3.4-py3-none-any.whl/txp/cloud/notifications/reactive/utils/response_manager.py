from decouple import config
from google.cloud import bigquery
from twilio.rest import Client
from txp.common.utils.bigquery_utils import get_last_task_prediction_for_asset

from .chat_responses import (
    TwilioTemplates,
    WhatsAppResponses,
    ASSET_NAMES,
    CONDITION_NAMES,
)
from .database_utils import get_tenants_from_phone_number, read_tenants_json
from .models import DialogFlowRequest
from .twilio_manager import TwilioManager, simple_report_pdf


account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)
twilio_manager = TwilioManager(client)


async def get_last_task_prediction(*arg, **kwargs):
    """Wrap a synchronous function to run as asynchronous."""
    return get_last_task_prediction_for_asset(*arg, **kwargs)


def asset_status_short_template(asset_id: str, condition: str) -> str:
    """Returns a string with a filled template. The template is ASSET_SHORT_STATUS.

    Args:
        asset_id: Asset ID.
        condition: Asset's current condition.
    """
    return TwilioTemplates.ASSET_STATUS_SHORT.value.format(asset_id, condition.upper())


def asset_name(asset_id: str, asset_mapping: dict) -> str:
    """Maps the asset_id to a more readable equivalent name for the receiver of the message.

    Args:
        asset_id: Asset ID.
        asset_mapping: A dictionary with more human-readable asset names.
    """
    return asset_mapping[asset_id]


def condition_name(asset_condition: str, condition_mapping: dict) -> str:
    """Maps the asset's condition to a more readable equivalent name for the receiver of the message.

    Args:
        asset_condition: Asset's condition.
        condition_mapping: A dictionary with more human-readable asset's condition names.
    """
    return condition_mapping[asset_condition]


def fulfillment_asset_condition(query: dict) -> str:
    """Returns the text template of the asset condition with its fields filled.

    Args:
        query: Database query (dict) about asset condition.
    """
    if query is None:
        return WhatsAppResponses.ASSET_DATA_12_HR_NOT_FOUND.value
    else:
        return asset_status_short_template(
            asset_name(query["asset_id"], ASSET_NAMES),
            condition_name(query["condition"], CONDITION_NAMES),
        )


async def response_builder(
    dialogflow_request: DialogFlowRequest,
    hardcoded_table: str,
    bigquery_client: bigquery.Client,
) -> str:
    """Selects a response according to the action selected by DialogFlow.

    Args:
        dialogflow_request: JSON request from DialogFlow.
        hardcoded_table: Name of BigQuery table with data about assets.
        bigquery_client: A bigquery.Client, authenticated with the provided credentials.
    """
    dialogflow_query = dialogflow_request.queryResult

    match dialogflow_query.action:

        case "asset_current_state":
            from_whatsapp = dialogflow_request.originalDetectIntentRequest.payload.From
            if from_whatsapp is not None:
                tenants_json = read_tenants_json(
                    "utils/tenants_data.json"
                )  # Data from tenants in json format.
                tenant = get_tenants_from_phone_number(tenants_json, from_whatsapp)[0]
                if tenant is not None:
                    entity = dialogflow_query.parameters["asset1"]
                    query = await get_last_task_prediction(
                        tenant_id=tenant,
                        table_name=hardcoded_table,
                        asset_id=entity,
                        days=0.5,
                        client=bigquery_client,
                    )
                    fulfillment_text = fulfillment_asset_condition(query)
                else:
                    fulfillment_text = (
                        TwilioTemplates.SERVICE_NOT_AVAILABLE_CONTACT_US.value
                    )
            else:
                fulfillment_text = WhatsAppResponses.ONLY_WORKS_ON_WHATSAPP.value

        case "asset_report":
            # fulfillment_text = WhatsAppResponses.REPORT_SENT.value
            # to_whatsapp = dialogflow_request.originalDetectIntentRequest.payload.From
            # from_whatsapp = dialogflow_request.originalDetectIntentRequest.payload.To
            # twilio_manager.send_media(
            #     "Reporte",
            #     from_phone=from_whatsapp,
            #     to_phone=to_whatsapp,
            #     media_url=simple_report_pdf,
            # )

            # TEMPORAL SOLUTION:
            fulfillment_text = "Puedes consultar tu reporte actualizado aquí: https://storage.cloud.google.com/txp-reports/labshowroom-001/report_1/labshowroom-001_report_1_2022-09-30-22-00-00.pdf"

        case _:
            fulfillment_text = WhatsAppResponses.NOT_SUPPORTED_AT_THIS_TIME.value

    return fulfillment_text
