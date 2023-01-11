import time

import txp.common.utils.bigquery_utils
import txp.common.utils.firestore_utils
import txp.common.utils.signals_utils
from google.cloud import pubsub_v1
from google.api_core import retry
from google.oauth2 import service_account
import google.cloud.firestore as firestore
import json
from google.cloud import bigquery
from txp.common.config import settings
import logging


class PubSubSubscriber:
    """Subscriber at GCP PubSub, it reads messages from PubSub service, this class reads messages by  batches of
    max_messages length.

    Args:
        credentials: GCS credentials.
        subscription_id: PubSub subscription id where signal messages are going to come from.
    """

    max_messages = 20
    max_retries = 10

    def __init__(self, credentials, subscription_id):
        self.project_id = credentials.project_id
        self.subscription_id = subscription_id
        self.subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

    def get_messages(self):
        subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)
        with self.subscriber:
            response = self.subscriber.pull(
                request={"subscription": subscription_path, "max_messages": self.max_messages},
                retry=retry.Retry(deadline=300),
            )

            if len(response.received_messages) == 0:
                return

            ack_ids = []
            for received_message in response.received_messages:
                ack_ids.append(received_message.ack_id)

            self.subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})

        return response.received_messages


class SignalsSegregator:
    """This class is in charge of waiting for all necessary PubSub messages for doing a prediction, due to
    telemetry pipelines PubSub messages do not come in order, prediction service has to wait for all messages
    generated at the pipeline in order to make a prediction for the signal.

    Args:
        credentials_str: GCS credentials string.
        dataset: BQ dataset name.
        subscription_id: PubSub subscription id where signal messages are going to come from.
        backup_collection_name: Firestore collection name where all backup is going to be stored.
    """

    def __init__(self, credentials_str, dataset, subscription_id, backup_collection_name, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        json_dict_service_account = json.loads(credentials_str, strict=False)
        self.credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        self.subscription_id = subscription_id
        self.firestore_db = firestore.Client(credentials=self.credentials, project=self.credentials.project_id)
        self.backup_collection_name = backup_collection_name
        self.messages_db = self.load_backup()
        self.dataset = dataset
        self.bigquery_segregator = BigquerySignalsSegregator(credentials_str, dataset)

    def load_backup(self):
        logging.info("Loading signals segregator backup")
        backup_ref = self.firestore_db.collection(self.backup_collection_name).document(
            settings.firestore.ray_signals_segregator_doc_name
        )
        backup = backup_ref.get().to_dict()
        backup_ref.set({})

        if backup:
            logging.info("There were signals at firestore db")
        else:
            logging.info("There were no signals at firestore db")

        logging.info("Loaded signals segregator")

        return backup

    def backup(self):
        logging.info("Backing up signals segregator")
        self.firestore_db.collection(self.backup_collection_name).document(
            settings.firestore.ray_signals_segregator_doc_name
        ).set(self.messages_db)
        logging.info("Signals segregator backed up")

    def __store_message(self, message, schema, task_id):
        table_id = message["table_id"].split(".")[2]
        observation_timestamp = str(message["observation_timestamp"])
        try:
            x = schema[message["edge_logical_id"]][message["perception_name"]][table_id]
        except KeyError:
            return False

        task = self.messages_db.get(task_id, None)
        if task is None:
            self.messages_db[task_id] = {}

        window = self.messages_db[task_id].get(observation_timestamp, None)
        if window is None:
            empty_doc = {}
            for edge_logical_id in schema:
                empty_doc[edge_logical_id] = {}
                for perception in schema[edge_logical_id]:
                    empty_doc[edge_logical_id][perception] = {}
                    for table in schema[edge_logical_id][perception]:
                        if schema[edge_logical_id][perception][table]:
                            empty_doc[edge_logical_id][perception][table] = []
            window = empty_doc
            self.messages_db[task_id][observation_timestamp] = window

        self.messages_db[task_id][observation_timestamp][message["edge_logical_id"]][
            message["perception_name"]][table_id].append(message)
        return True

    def __check_metrics_table_completeness(self, rows):
        if not len(rows):
            return False
        configuration_id = rows[0]["configuration_id"]
        edge_logical_id = rows[0]["edge_logical_id"]
        perception_name = rows[0]["perception_name"]
        tenant_id = rows[0]["tenant_id"]
        return len(rows) == txp.common.utils.firestore_utils.get_signal_dimensions_from_firestore(configuration_id, tenant_id, edge_logical_id,
                                                                                                  perception_name, self.firestore_db)[0]

    @staticmethod
    def __check_time_table_completeness(rows):
        rows = sorted(rows, key=lambda d: d['part_index'])
        return len(rows) and rows[0]["previous_part_index"] >= rows[0]["part_index"] and len(rows) == (
                rows[0]["previous_part_index"] - rows[0]["part_index"] + 1)

    def __check_sampling_window_completeness(self, sampling_window):
        complete = True
        for edge_logical_id in sampling_window:
            for perception_name in sampling_window[edge_logical_id]:
                for table in sampling_window[edge_logical_id][perception_name]:
                    elements = sampling_window[edge_logical_id][perception_name][table]
                    if table == "time":
                        complete = complete and self.__check_time_table_completeness(elements)
                    elif table == "time_metrics" or table == "fft_metrics" or table == "psd_metrics":
                        complete = complete and self.__check_metrics_table_completeness(elements)
                    else:
                        complete = complete and len(elements)
        return complete

    def get_messages(self):

        messages = None
        for i in range(0, PubSubSubscriber.max_retries):
            try:
                subscriber = PubSubSubscriber(self.credentials, self.subscription_id)
                messages = subscriber.get_messages()
                break
            except Exception as e:
                logging.info(f"Unexpected error when reading pubsub Messages, retrying Exception: {e}")
                if i + 1 == PubSubSubscriber.max_retries:
                    raise e
                time.sleep(10)
        return messages

    def process_message(self, message, schema, task_id):
        is_valid_message = self.__store_message(message, schema, task_id)
        if not is_valid_message:
            return False

        sampling_window_data = self.messages_db[task_id][str(message["observation_timestamp"])]
        completed = self.__check_sampling_window_completeness(sampling_window_data)

        return completed

    def get_sampling_window(self, observation_timestamp, task_id):
        return self.messages_db[task_id][str(observation_timestamp)]

    def delete_sampling_window(self, observation_timestamp, task_id):
        self.messages_db[task_id].pop(str(observation_timestamp))
        if not self.messages_db[task_id]:
            self.messages_db.pop(task_id)


class BigquerySignalsSegregator:

    def __init__(self, credentials_str, dataset):
        self.credentials_str = credentials_str
        self.dataset = dataset

    @staticmethod
    def __build_time_signal(rows):
        signal = txp.common.utils.signals_utils.merge_signal_chunks(rows)
        signal["data"] = [dimension["values"] for dimension in signal["data"]]
        return signal

    def get_sampling_window_rows_from_bigquery(self, sampling_window, observation_timestamp, tenant_id):
        json_dict_service_account = json.loads(self.credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        sampling_window_rows = {}
        for edge_logical_id in sampling_window:
            sampling_window_rows[edge_logical_id] = {}
            for perception_name in sampling_window[edge_logical_id]:
                sampling_window_rows[edge_logical_id][perception_name] = {}
                for table_id in sampling_window[edge_logical_id][perception_name]:
                    sampling_window_rows[edge_logical_id][perception_name][
                        table_id] = txp.common.utils.bigquery_utils.get_sampling_window_from_bigquery(
                        f'{self.dataset}.{table_id}', edge_logical_id, perception_name, observation_timestamp,
                        tenant_id, bigquery_client)
                    if table_id == "time":
                        sampling_window_rows[edge_logical_id][perception_name][table_id] = [
                            self.__build_time_signal(sampling_window_rows[edge_logical_id][perception_name][table_id])]
        bigquery_client.close()
        return sampling_window_rows
