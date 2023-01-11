import argparse
import logging
import os
import apache_beam as beam
import txp.common.utils.signals_utils
from apache_beam.options.pipeline_options import PipelineOptions
import google.cloud.firestore as firestore
from typing import List
import json

from txp.cloud.pipelines.telemetry import steps as ts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


BIGQUERY_TABLE = "PROJECT_ID:DATASET_NAME.TABLE_NAME"
MODEL_SERVING_TOPIC_PREFIX = f'projects/{os.environ.get("GCP_PROJECT_ID", "tranxpert-mvp")}/topics/'
MODEL_SERVING_TOPIC_NAME = 'txp-model-serving-signals-test'
SIGNALS_QUEUE_COLLECTION = 'signals_queue_test'
DATA_LAKE = 'tranxpert-mvp-telemetry-data-lake-test'


def get_firestore_collection(signals_queue_collection) -> List[str]:
    signals = []
    db = firestore.Client()
    docs = db.collection(signals_queue_collection).stream()
    for doc in docs:
        doc_as_dictionary = doc.to_dict()

        if bool(doc_as_dictionary):
            signals.append(json.dumps(doc_as_dictionary))

    return signals


class BuildSignalsFromGcs(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, data_lake, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import os
        from google.cloud import storage

        project_data_lake = data_lake
        project_name = os.environ.get("GCP_PROJECT_ID", "tranxpert-mvp")

        all_chunks = []
        storage_client = storage.Client()
        bucket = storage_client.bucket(project_data_lake, user_project=project_name)

        signal_json = json.loads(element)

        for k in signal_json:
            for path in signal_json[k]:
                blob = bucket.blob(path)
                all_chunks.append(json.loads(blob.download_as_string()))

        all_chunks.sort(key=lambda c: c["part_index"])

        yield txp.common.utils.signals_utils.merge_signal_chunks(all_chunks)


class PopFirestoreQueue(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, signals_queue_collection, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import google.cloud.firestore as firestore
        firestore_db = firestore.Client()
        signal_json = json.loads(element)
        path = signal_json["paths"][0]
        doc = path.split("/")[1]
        doc_id = doc.split("|")[:-2]
        doc_id = "|".join(doc_id)
        firestore_db.collection(signals_queue_collection).document(doc_id).delete()


class BatchPublishToPubSub(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, topic_path, **kwargs):
        from google.cloud import pubsub_v1
        publisher = pubsub_v1.PublisherClient()
        future = publisher.publish(topic_path, data=element)
        return future.result()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_table", help="Output Time BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--fft_table", help="Output Fft BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--psd_table", help="Output Psd BigQuery Table", default=BIGQUERY_TABLE)

    parser.add_argument("--time_metrics_table", help="Output Time metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--fft_metrics_table", help="Output Fft metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--psd_metrics_table", help="Output Psd metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--model_signals_topic_name", help="topic for processing signals with ml task",
                        default=MODEL_SERVING_TOPIC_NAME)
    parser.add_argument("--signals_queue_collection",
                        help="queue of signals stored in firestore, "
                             "this is where signals are going to be downloaded from",
                        default=SIGNALS_QUEUE_COLLECTION)
    parser.add_argument("--data_lake", help="data lake bucket name in gcp", default=DATA_LAKE)

    known_args, pipeline_args = parser.parse_known_args()
    model_serving_topic = MODEL_SERVING_TOPIC_PREFIX + known_args.model_signals_topic_name

    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as p:
        pending_signals = (
                p
                | "ReadFromFirestore" >> beam.Create(get_firestore_collection(known_args.signals_queue_collection))
        )

        (
                pending_signals
                | "DeleteFromFirestore" >> beam.ParDo(PopFirestoreQueue(), known_args.signals_queue_collection)
        )

        signal_collection = (
                pending_signals
                | "BuildSignalsFromGcs" >> beam.ParDo(BuildSignalsFromGcs(), known_args.data_lake)
        )

        ########################################################################################################################
        time_signal = (
                signal_collection
                | "TimeProcessing" >> beam.ParDo(ts.TimeProcessing())
        )
        (
                time_signal
                | "WriteTimeToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.time_table)
                | "WriteTimeToPubSub" >> beam.ParDo(BatchPublishToPubSub(), model_serving_topic)
        )
        (
                time_signal
                | "TimeMetrics" >> beam.ParDo(ts.TimeMetrics())
                | "WriteTimeMetricsToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.time_metrics_table)
                | "WriteTimeMetricsToPubSub" >> beam.ParDo(BatchPublishToPubSub(), model_serving_topic)
        )
        ########################################################################################################################
        fft_signal = (
                signal_collection
                | "FftProcessing" >> beam.ParDo(ts.FftProcessing())
        )
        (
                fft_signal
                | "WriteFftToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.fft_table)
                | "WriteFftToPubSub" >> beam.ParDo(BatchPublishToPubSub(), model_serving_topic)
        )
        (
                fft_signal
                | "FftMetrics" >> beam.ParDo(ts.FftMetrics())
                | "WriteFftMetricsToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.fft_metrics_table)
                | "WriteFftMetricsToPubSub" >> beam.ParDo(BatchPublishToPubSub(), model_serving_topic)
        )
        ########################################################################################################################
        psd_signal = (
                signal_collection
                | "PsdProcessing" >> beam.ParDo(ts.PsdProcessing())

        )
        (
                psd_signal
                | "WritePsdToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.psd_table)
                | "WritePsdToPubSub" >> beam.ParDo(BatchPublishToPubSub(), model_serving_topic)
        )
        (
                psd_signal
                | "PsdMetrics" >> beam.ParDo(ts.PsdMetrics())
                | "WritePsdMetricsToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.psd_metrics_table)
                | "WritePsdMetricsToPubSub" >> beam.ParDo(BatchPublishToPubSub(), model_serving_topic)
        )


if __name__ == "__main__":
    run()
