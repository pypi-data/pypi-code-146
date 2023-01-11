
# =========================== Imports ===============================
import base64
import sys
from txp.cloud import (
    pull_current_configuration_from_firestore,
    pull_docs_from_collection_associated_with_configuration
)
import google.cloud.firestore as firestore
from google.cloud import bigquery
from txp.cloud import settings as cloud_settings
from typing import List, Dict
from datetime import datetime
import json

# =========================== Constant Data & helper functions ===============================
edges_collection_name = cloud_settings.firestore.edges_collection
edges_states_table_name = "statesdataset01.edges_states"


def _is_gateway_state(event_data) -> bool:
    """Returns true if the event was sent by a Gateway"""
    return 'edges' in event_data


def _get_configuration_reference(db: firestore.Client, tenant_id: str) -> firestore.DocumentReference:
    configuration = pull_current_configuration_from_firestore(db, tenant_id)
    if not configuration:
        print("No Configuration document was found", file=sys.stderr)
        return None

    return configuration.reference


def _update_edges_documents(edges_new_states: Dict, documents: List[firestore.DocumentSnapshot]):
    for document in documents:
        doc_ref = document.reference
        doc_ref.update({
            'state': edges_new_states[document.get('logical_id')]
        })
        print(f'Firestore entry updated for edge: {document.get("logical_id")}')


def _clear_resources(db: firestore.Client):
    db.close()


def persist_states(client: bigquery.Client, edges_state_dict):
    table = f"""{client.project}.{edges_states_table_name}"""
    for edge_logical_id in edges_state_dict:
        select_query = f"""
        SELECT * FROM `{table}`
        WHERE edge_logical_id = "{edge_logical_id}"
        ORDER BY timestamp DESC
        LIMIT 1;
        """
        df = (client.query(select_query).result().to_dataframe())
        last_state = None
        for index, row in df.iterrows():
            last_state = row
            break
        rows_to_insert = []
        if last_state is None or edges_state_dict[edge_logical_id]["driver_state"] != last_state["state"]:
            new_state = edges_state_dict[edge_logical_id]["driver_state"]
            timestamp = edges_state_dict[edge_logical_id]["since_datetime"]
            timestamp = int(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timestamp() * 1e9)
            rows_to_insert.append({"edge_logical_id": edge_logical_id, "state": new_state, "timestamp": timestamp})
        if len(rows_to_insert):
            errors = client.insert_rows_json(table, rows_to_insert)
            if not errors:
                print("New rows have been added.")
            else:
                print("Encountered errors while inserting state rows: {}".format(errors))
        else:
            print("There are not new states")


# =========================== Cloud function def ===============================
def process_state_event_to_firestore(event, context):
    """This function is the function deployed to run in the cloud
    functions runtime

    A detailed page with all the context can be found here:
        https://cloud.google.com/functions/docs/calling/pubsub
    """
    print('Starting to process event received...')
    if 'data' in event:
        state_data = base64.b64decode(event['data']).decode()
        attributes = event.get('attributes', None)
        if attributes:
            db = firestore.Client()
            bigquery_client = bigquery.Client()
            event_device_id = attributes['deviceId']
            print(f'Event received from {event_device_id}')

            if _is_gateway_state(state_data):
                edges_state_dict = json.loads(state_data)['edges']
                tenant_id = json.loads(state_data)['tenant_id']
                configuration_ref = _get_configuration_reference(db, tenant_id)
                if not configuration_ref:
                    _clear_resources(db)
                    exit(1)

                try:
                    persist_states(bigquery_client, edges_state_dict)
                except:
                    print("Error while updating state on BigQuery table", file=sys.stderr)

                print(f'State received for devices. '
                      f'This will update Firestore configuration {configuration_ref.get().get("configuration_id")}')

                # Get edges from firestore
                edges_docs: List[firestore.DocumentSnapshot] = pull_docs_from_collection_associated_with_configuration(
                    db, edges_collection_name, configuration_ref
                )
                # Filter the edges to the reported ones
                edges_docs = list(filter(
                    lambda edge_snapshot: edge_snapshot.get('logical_id') in edges_state_dict.keys(),
                    edges_docs
                ))
                # Update the edges in Firestore
                _update_edges_documents(edges_state_dict, edges_docs)

                print("The edges were updated successfully in the Database snapshot")
                _clear_resources(db)

            else:
                print('State event received from a Edge. Ignore.')

    else:
        print('Unexpected error: No data received in function.', file=sys.stderr)
