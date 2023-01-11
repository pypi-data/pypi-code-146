# =========================== Imports ===============================
import os
import base64
from txp.common.protos.user_notification_pb2 import Notification
import google.cloud.firestore as firestore
from txp.common.utils import firestore_utils
from twilio.rest import Client

# =========================== Constant Data & helper functions ===============================
project_id = os.environ.get('GCP_PROJECT')
ACCOUNT_SID = os.environ.get("ACCOUNT_SID", "")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "")
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "")
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

# =========================== Cloud function def ===============================


def ml_notifications(event, context):
    """This function is the function deployed to run in the cloud
    functions runtime.
    A detailed page with all the context can be found here:
        https://cloud.google.com/functions/docs/calling/pubsub
    In order to know what exactly this function does take a look at readme.md file
    """
    if not ACCOUNT_SID or not AUTH_TOKEN or not WHATSAPP_NUMBER:
        print('Cloud Function was not correctly deployed, re deploy and try again')
        return
    print('Starting to process new notification event')
    if 'data' in event:
        if 'attributes' not in event:
            print('Wrong telemetry event received stopping function execution')
            return
        telemetry_data = base64.b64decode(event['data']).decode()
        proto_string = base64.b64decode(telemetry_data)
        proto = Notification()
        proto.ParseFromString(proto_string)

        firestore_db = firestore.Client()

        tenant = firestore_utils.pull_tenant_doc(firestore_db, proto.content.tenant_id).to_dict()

        for user in tenant["notification_users"]:
            if not user["is_active"]:
                continue
            message = f"El activo {proto.content.asset_id} " \
                      f"está actualmente en condición {proto.content.predicted_condition}."

            whatsapp_msg = CLIENT.messages.create(
                body=message,
                from_=WHATSAPP_NUMBER,
                to="whatsapp:+{}".format(user["phone_number"]),
            )
            print(f"Message: [{whatsapp_msg.body}] sent to {whatsapp_msg.to}")

        firestore_db.close()
