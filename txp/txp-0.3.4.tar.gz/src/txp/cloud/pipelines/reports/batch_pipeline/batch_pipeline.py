import argparse
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import firestore, bigquery
from txp.common.utils import firestore_utils, reports_utils
from txp.common.config import settings
from txp.cloud.pipelines.reports.batch_pipeline import steps as ts
import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

BIGQUERY_TABLE = "PROJECT_ID:DATASET_NAME.TABLE_NAME"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../../../common/credentials/pub_sub_to_bigquery_credentials.json"


def get_all_sections(dataset):
    dataset = dataset.replace(":", ".")
    firestore_db = firestore.Client()
    bigquery_db = bigquery.Client()
    all_tenants = firestore_utils.get_all_tenants_from_firestore(firestore_db)
    for tenant_doc in all_tenants:
        if "reports" in tenant_doc:
            for report_id in tenant_doc["reports"]:
                max_section_id = tenant_doc["reports"][report_id]["max_section_id"]
                max_section = tenant_doc["sections"][max_section_id]
                if not max_section["last"]:
                    continue
                end_datetime = datetime.datetime.strptime(max_section["last"], settings.time.datetime_zoned_format)
                start_datetime = datetime.datetime.strptime(tenant_doc["reports"][report_id]["last_generation"],
                                                            settings.time.datetime_zoned_format)
                sections_group = reports_utils.get_report_sections(firestore_db, bigquery_db,
                                                                   f"{dataset}.sections",
                                                                   tenant_doc["tenant_id"], report_id, start_datetime,
                                                                   end_datetime)
                if sections_group is None:
                    continue
                for sections in sections_group:
                    logging.info(f'On start date: {start_datetime} and end date: {end_datetime} '
                                 f'for {tenant_doc["tenant_id"]} on report {report_id} '
                                 f'there are {len(sections)} sections')
                    yield tenant_doc["tenant_id"], report_id, sections
                firestore_utils.update_last_report_datetime(firestore_db, tenant_doc["tenant_id"], report_id,
                                                            max_section["last"])
    firestore_db.close()
    bigquery_db.close()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports_dataset", help="Bigquery sections dataset name")
    parser.add_argument("--reports_bucket_name", help="Google cloud storage final destination for report pdf files")
    parser.add_argument("--notifications_user", help="Username for auth with notification service", default="")
    parser.add_argument("--notifications_password", help="Password for auth with notification service", default="")
    parser.add_argument("--notifications_url", help="Notifications service url", default="")

    known_args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as p:
        (
                p
                | "GetAllSections" >> beam.Create(get_all_sections(known_args.reports_dataset))
                | "BuildPdf" >> beam.ParDo(ts.BuildPdf())
                | "StorePdf" >> beam.ParDo(ts.StorePdf(), known_args.reports_bucket_name)
                | "Notify" >> beam.ParDo(ts.NotifyPdfCreation(), known_args.reports_bucket_name,
                                         known_args.notifications_url,
                                         known_args.notifications_user,
                                         known_args.notifications_password)
        )


if __name__ == "__main__":
    run()
