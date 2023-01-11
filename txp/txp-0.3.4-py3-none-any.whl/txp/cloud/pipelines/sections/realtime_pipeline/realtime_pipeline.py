import argparse
import logging
import os
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from txp.cloud.pipelines.sections.realtime_pipeline import steps as ts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
BIGQUERY_TABLE = "PROJECT_ID:DATASET_NAME.TABLE_NAME"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../../../common/credentials/pub_sub_to_bigquery_credentials.json"


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_subscription",
        help='Input PubSub subscription of the form "projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."',
        default="SUBSCRIPTION_NAME"
    )

    parser.add_argument("--sections_table", help="Sections Output Bigquery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--time_table", help="Input Time BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--fft_table", help="Input Fft BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--psd_table", help="Input Psd BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--time_metrics_table", help="Input Time metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--fft_metrics_table", help="Input Fft metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--psd_metrics_table", help="Input Psd metrics BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--events_table", help="Input ml events BigQuery Table", default=BIGQUERY_TABLE)
    parser.add_argument("--states_table", help="Input ml states BigQuery Table", default=BIGQUERY_TABLE)

    known_args, pipeline_args = parser.parse_known_args()
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(StandardOptions).streaming = True

    sections_table = known_args.sections_table.replace(":", ".")
    time_table = known_args.time_table.replace(":", ".")
    fft_table = known_args.fft_table.replace(":", ".")
    psd_table = known_args.psd_table.replace(":", ".")
    time_metrics_table = known_args.time_metrics_table.replace(":", ".")
    fft_metrics_table = known_args.fft_metrics_table.replace(":", ".")
    psd_metrics_table = known_args.psd_metrics_table.replace(":", ".")
    events_table = known_args.events_table.replace(":", ".")
    states_table = known_args.states_table.replace(":", ".")

    with beam.Pipeline(options=pipeline_options) as p:
        datasets = (
                p
                | "ReadFromPubSub" >> beam.io.gcp.pubsub.ReadFromPubSub(
                    subscription=known_args.input_subscription,
                    timestamp_attribute=None
                )
                | "ProcessPubsub" >> beam.ParDo(ts.ProcessPubsub(), time_table, fft_table, psd_table,
                                                time_metrics_table, fft_metrics_table, psd_metrics_table,
                                                events_table, states_table)
        )
        ########################################################################################################################

        (
                datasets
                | "Plot2dSection" >> beam.ParDo(ts.Plot2DSectionProcessing())
                | "WritePlot2dNumericSectionToBigQuery" >> beam.ParDo(ts.WriteToBigQuery(), sections_table)
        )


if __name__ == "__main__":
    run()
