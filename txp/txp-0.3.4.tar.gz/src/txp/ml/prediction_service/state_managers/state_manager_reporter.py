from google.cloud import pubsub_v1
import json
from google.oauth2 import service_account
from google.cloud import bigquery
import ray
import logging
from txp.common.utils import firestore_utils
import google.cloud.firestore as firestore
from txp.common.config import settings
from datetime import datetime, timedelta
import pytz


class StateManagerReporter:

    def __init__(self, reports_topic, credentials_str, log_level=logging.INFO):
        logging.basicConfig(level=log_level)

        self.reports_topic = reports_topic
        json_dict_service_account = json.loads(credentials_str, strict=False)
        self.credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        self.bigquery_client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
        self.firestore_db = firestore.Client(credentials=self.credentials, project=self.credentials.project_id)

    def generate_report(self, tenant_id):
        tenant_doc = firestore_utils.pull_tenant_doc(self.firestore_db, tenant_id).to_dict()
        if "sections" in tenant_doc:
            for section_id in tenant_doc["sections"]:
                section = tenant_doc["sections"][section_id]
                next_date_str = section["next"]
                default_next_date_str = ""
                for report_id in tenant_doc["reports"]:
                    if section_id in tenant_doc["reports"][report_id]["sections"]:
                        default_next_date_str = tenant_doc["reports"][report_id]["last_generation"]
                        break
                if not next_date_str:
                    logging.info(f"Not next date found for {section_id} taking last generation "
                                 f"from report {default_next_date_str}")
                    next_date_str = default_next_date_str
                if not next_date_str:
                    logging.info(f"Not next date or last generation found for {section_id} skipping section creation")
                    continue
                end_date = datetime.strptime(next_date_str, settings.time.datetime_zoned_format)
                if end_date <= datetime.now(tz=pytz.UTC):
                    time_delta = timedelta(minutes=section["frequency"])
                    start_date = end_date - time_delta
                    publisher = pubsub_v1.PublisherClient(credentials=self.credentials)
                    topic_path = publisher.topic_path(self.credentials.project_id, self.reports_topic)

                    section_request = {
                        "tenant_id": tenant_id,
                        "type": section["type"],
                        "start_datetime": start_date.strftime(settings.time.datetime_zoned_format),
                        "end_datetime": end_date.strftime(settings.time.datetime_zoned_format),
                        "parameters": section["parameters"],
                        "section_id": section_id
                    }
                    future = publisher.publish(topic_path, data=json.dumps(section_request).encode('utf-8'))
                    future.result()
                    logging.info(f"New section request sent for {tenant_id} section id: {section_id} "
                                 f"section: {section_request}")
                    next_date = (end_date + time_delta).strftime(settings.time.datetime_zoned_format)
                    firestore_utils.update_last_section_datetime(self.firestore_db, tenant_id, section_id,
                                                                 section["next"])
                    firestore_utils.update_next_section_datetime(self.firestore_db, tenant_id, section_id,
                                                                 next_date)


@ray.remote
class RayStateManagerReporter(StateManagerReporter):
    def __init__(self, reports_topic, credentials_str):
        super().__init__(reports_topic, credentials_str)
