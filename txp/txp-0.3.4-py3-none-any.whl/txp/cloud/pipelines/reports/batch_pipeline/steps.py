import logging
from txp.common.config import settings
import datetime
import pytz
import os
from txp.common.utils import firestore_utils
from google.cloud import storage, firestore
import apache_beam as beam
import io


class BuildPdf(beam.DoFn):
    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def build_report_pdf(self, tenant_doc, report_id, sections):
        import txp.common.reports.pdf_builders as builders
        builder_type = tenant_doc.get("builder", "MockPDFBuilder")
        logging.info(f"Build report pdf function called over {builder_type} for tenant: {tenant_doc['tenant_id']} "
                     f"report: {report_id}")
        builder = builders.BUILDERS_REGISTRY.get(builder_type, builders.MockPDFBuilder)(tenant_doc, report_id, sections)
        return builder.build_report_pdf()

    def get_pdf_name(self, tenant_doc, report_id):
        datetime_format = settings.time.datetime_zoned_format.replace(" ", "_")
        return f'{tenant_doc["tenant_id"]}_{report_id}_' \
               f'{datetime.datetime.now(tz=pytz.UTC).strftime(datetime_format)}.pdf'

    def process(self, element, timestamp=beam.DoFn.TimestampParam,
                window=beam.DoFn.WindowParam):
        tenant_id, report_id, sections = element
        firestore_db = firestore.Client()
        tenant_doc = firestore_utils.pull_tenant_doc(firestore_db, tenant_id).to_dict()
        logging.info(f'Building pdf for report: {report_id} of tenant: {tenant_doc["tenant_id"]} which contains '
                     f'{len(sections)} sections')
        pdf_path = f"{tenant_doc['tenant_id']}/{report_id}/{self.get_pdf_name(tenant_doc, report_id)}"

        pdf = self.build_report_pdf(tenant_doc, report_id, sections)

        logging.info(f'Built pdf for report: {report_id} of tenant: {tenant_doc["tenant_id"]} which contains '
                     f'{len(sections)} sections')

        yield pdf_path, pdf
        firestore_db.close()


class StorePdf(beam.DoFn):
    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, reports_bucket, timestamp=beam.DoFn.TimestampParam,
                window=beam.DoFn.WindowParam):
        pdf_path, pdf = element
        logging.info(f"Storing {pdf_path} at gcs")
        storage_client = storage.Client()
        bucket = storage_client.bucket(reports_bucket, user_project=os.environ.get("GCP_PROJECT_ID", "tranxpert-mvp"))
        blob = bucket.blob(pdf_path)
        pdf_byte = io.BytesIO(bytes(pdf.output(dest='S'), encoding='latin1'))
        blob.upload_from_file(pdf_byte)
        storage_client.close()
        logging.info(f"{pdf_path} Stored at gcs")
        yield pdf_path


class NotifyPdfCreation(beam.DoFn):
    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def get_pdf_url(self, pdf_path, reports_bucket):
        return f'https://storage.googleapis.com/{reports_bucket}/{pdf_path}'

    def process(self, pdf_path, reports_bucket, notifications_url, username, password, timestamp=beam.DoFn.TimestampParam,
                window=beam.DoFn.WindowParam):
        import requests
        if not username:
            logging.info(f'No username provided for notifications {pdf_path} will not be stored')
            return
        pdf_url = self.get_pdf_url(pdf_path, reports_bucket)
        logging.info(f"Notifying pdf creation on url: {pdf_url} at gcs")

        obj = {
            "tenant_id": pdf_path.split("/")[0],
            "report_url": pdf_url
        }
        x = requests.post(notifications_url, json=obj, auth=(username, password))
        logging.info(f'Request sent response: {x.text}')
