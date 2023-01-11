import argparse
import logging
import os
import apache_beam as beam
import txp.cloud.pipelines.telemetry.vibration_pipeline_steps
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from txp.cloud.pipelines.telemetry import steps as ts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../../../common/credentials/pub_sub_to_bigquery_credentials.json"
INPUT_SUBSCRIPTION = "projects/PROJECT_ID/subscriptions/SUBSCRIPTION_NAME"
BIGQUERY_TABLE = "PROJECT_ID:DATASET_NAME.TABLE_NAME"
MODEL_SERVING_TOPIC_PREFIX = f'projects/{os.environ.get("GCP_PROJECT_ID", "tranxpert-mvp")}/topics/'
MODEL_SERVING_TOPIC_NAME = 'txp-model-serving-signals-test'


class FromProtoToJson(beam.DoFn):
    """This step will parse the Gateway Package yield multiple `element`(s).
    One per perception dimension signal in the package. """
    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element: bytes, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import base64
        from txp.common.protos.gateway_package_pb2 import GatewayPackageProto
        from txp.common.utils import dataflow_utils

        proto_string = base64.b64decode(element)
        proto = GatewayPackageProto()
        proto.ParseFromString(proto_string)

        for e in dataflow_utils.from_proto_to_json(proto):
            logging.info(f'arrived: {e["perception_name"]} - {e["edge_logical_id"]} - {e["tenant_id"]}')
            yield e


class FromProtoToJsonAllPackagePerceptions(beam.DoFn):
    """This step will parse the Gateway Package a yield an `element` with
    all the signals contained on the package. """
    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element: bytes, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import base64
        from txp.common.protos.gateway_package_pb2 import GatewayPackageProto
        from txp.common.utils import dataflow_utils

        proto_string = base64.b64decode(element)
        proto = GatewayPackageProto()
        proto.ParseFromString(proto_string)

        yield dataflow_utils.from_proto_to_json(proto)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_subscription",
        help='Input PubSub subscription of the form "projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."',
        default=INPUT_SUBSCRIPTION
    )
    parser.add_argument("--time_table", help="Output Time BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--fft_table", help="Output Fft BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--psd_table", help="Output Psd BigQuery Table", default=BIGQUERY_TABLE)

    parser.add_argument("--time_metrics_table", help="Output Time metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--fft_metrics_table", help="Output Fft metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--psd_metrics_table", help="Output Psd metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--model_signals_topic_name", help="topic for processing signals with ml task",
                        default=MODEL_SERVING_TOPIC_NAME)

    known_args, pipeline_args = parser.parse_known_args()
    model_serving_topic = MODEL_SERVING_TOPIC_PREFIX + known_args.model_signals_topic_name

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as p:
        read_from_pubsub = (
            p
            | "ReadFromPubSub" >> beam.io.gcp.pubsub.ReadFromPubSub(
                subscription=known_args.input_subscription, timestamp_attribute=None
            )
        )
        signal_collection = (
            read_from_pubsub
            | "FromProtoToJson" >> beam.ParDo(FromProtoToJson())
        )
        signal_package_collection = (
            read_from_pubsub
            | "FromProtoToJsonAllPackagePerceptions" >> beam.ParDo(
                FromProtoToJsonAllPackagePerceptions()
            )
        )

########################################################################################################################
        # This steps will compute the Vibration Specific Analytics table rows
        rms_signal_collection = (
            signal_package_collection
            | "VibrationProcessing" >> beam.ParDo(
            txp.cloud.pipelines.telemetry.vibration_pipeline_steps.VibrationProcessing())
        )
        (
            rms_signal_collection
            | "WriteVibrationToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), 'telemetry:vibration')
        )

########################################################################################################################
        time_signal = (
            signal_collection
            | "TimeProcessing" >> beam.ParDo(ts.TimeProcessing())
        )
        (
            time_signal
            | "WriteTimeToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.time_table)
            | "WriteTimeToPubSub" >> beam.io.WriteToPubSub(topic=model_serving_topic, with_attributes=False)
        )
        (
            time_signal
            | "TimeMetrics" >> beam.ParDo(ts.TimeMetrics())
            | "WriteTimeMetricsToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.time_metrics_table)
            | "WriteTimeMetricsToPubSub" >> beam.io.WriteToPubSub(topic=model_serving_topic, with_attributes=False)
        )
########################################################################################################################
        fft_signal = (
            signal_collection
            | "FftProcessing" >> beam.ParDo(ts.FftProcessing())
        )
        (
            fft_signal
            | "WriteFftToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.fft_table)
            | "WriteFftToPubSub" >> beam.io.WriteToPubSub(topic=model_serving_topic, with_attributes=False)
        )
        (
            fft_signal
            | "FftMetrics" >> beam.ParDo(ts.FftMetrics())
            | "WriteFftMetricsToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.fft_metrics_table)
            | "WriteFftMetricsToPubSub" >> beam.io.WriteToPubSub(topic=model_serving_topic, with_attributes=False)
        )
########################################################################################################################
        psd_signal = (
            signal_collection
            | "PsdProcessing" >> beam.ParDo(ts.PsdProcessing())

        )
        (
            psd_signal
            | "WritePsdToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.psd_table)
            | "WritePsdToPubSub" >> beam.io.WriteToPubSub(topic=model_serving_topic, with_attributes=False)
        )
        (
            psd_signal
            | "PsdMetrics" >> beam.ParDo(ts.PsdMetrics())
            | "WritePsdMetricsToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), known_args.psd_metrics_table)
            | "WritePsdMetricsToPubSub" >> beam.io.WriteToPubSub(topic=model_serving_topic, with_attributes=False)
        )


if __name__ == "__main__":
    run()

