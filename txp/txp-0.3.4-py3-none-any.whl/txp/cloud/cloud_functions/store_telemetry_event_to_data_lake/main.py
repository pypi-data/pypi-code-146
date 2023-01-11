# =========================== Imports ===============================
import os
import json
import base64

import txp.common.utils.dataflow_utils
from google.cloud import storage
from txp.common.protos.gateway_package_pb2 import GatewayPackageProto
import google.cloud.firestore as firestore

# =========================== Constant Data & helper functions ===============================
project_id = os.environ.get('GCP_PROJECT')
data_lake_bucket_name = \
    f"{project_id}-{os.environ.get('DATA_LAKE_BUCKET_NAME', 'tranxpert-mvp-telemetry-data-lake')}"
pending_signal_chunks_collection_name = os.environ.get('PENDING_SIGNAL_CHUNKS_COLLECTION', 'pending_signal_chunks')


# =========================== Cloud function def ===============================

def insert_pending_signal_chunk(chunk_id, gateway_id, db):
    db.collection(pending_signal_chunks_collection_name).document(chunk_id).set({
        "id": chunk_id,
        "path": f"{gateway_id}/{chunk_id}"
    })


def get_chunk_id(chunk):
    return (
        f"""{chunk["edge_logical_id"]}|"""
        f"""{chunk["perception_name"]}|"""
        f"""{chunk["package_timestamp"]}|"""
        f"""{chunk["signal_timestamp"]}|"""
        f"""{chunk["previous_part_index"]}|"""
        f"""{chunk["part_index"]}"""
    )


def store_telemetry_event_to_data_lake(event, context):
    """This function is the function deployed to run in the cloud
    functions runtime.
    A detailed page with all the context can be found here:
        https://cloud.google.com/functions/docs/calling/pubsub
    In order to know what exactly this function does take a look at readme.md file
    """
    print('Starting to process telemetry event received...')
    if 'data' in event:
        if 'attributes' not in event:
            print('Wrong telemetry event received stopping function execution')
            return
        telemetry_data = base64.b64decode(event['data']).decode()
        proto_string = base64.b64decode(telemetry_data)
        proto = GatewayPackageProto()
        proto.ParseFromString(proto_string)
        chunks = txp.common.utils.dataflow_utils.from_proto_to_json(proto)
        gateway_id = event['attributes']['gatewayId']
        storage_client = storage.Client()
        bucket = storage_client.bucket(data_lake_bucket_name, user_project=project_id)
        firestore_db = firestore.Client()
        for chunk in chunks:
            print(f"Processing chunk: {get_chunk_id(chunk)}")
            blob = bucket.blob(f"{gateway_id}/{get_chunk_id(chunk)}")
            blob.upload_from_string(
                data=json.dumps(chunk),
                content_type='application/json'
            )
            insert_pending_signal_chunk(get_chunk_id(chunk), gateway_id, firestore_db)
        firestore_db.close()
