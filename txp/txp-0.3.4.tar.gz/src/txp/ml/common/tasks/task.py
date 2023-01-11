from abc import ABC, abstractmethod
from joblib import load
from dataclasses import dataclass
import tempfile
import os
import json
from google.cloud import storage
from google.oauth2 import service_account

from txp.ml.common.tasks.encoder import Encoder, EncoderStorage
from txp.ml.common.tasks.policy import Policy, PolicyStorage
from txp.common.ml.tasks import AssetTask


@dataclass
class TaskStorage:
    task_id: str
    encoder_storage: EncoderStorage
    policy_storage: PolicyStorage


class Task(ABC):
    task_bucket: str = "txp-model-storage"
    task_id: str

    def __init__(self, encoder: Encoder, policy: Policy, task_definition: AssetTask, credentials_str) -> None:
        self.encoder = encoder
        self.policy = policy
        self.ready = False
        self.credentials = credentials_str
        self.task_definition = task_definition
        self.task_id = self.task_definition.task_id

    def load_from_bucket(self, task_file: str):
        if task_file is not None:
            print(f"Restoring task from {task_file} in {self.task_bucket} bucket")
            tmp_file = download_task_file_from_bucket(self.credentials, self.task_bucket, task_file)
            task_data = load(tmp_file)
            self.load(task_data)
            os.remove(tmp_file)
            self.ready = True

    def save(self) -> TaskStorage:
        return TaskStorage(self.task_id, self.encoder.save(), self.policy.save())

    def load(self, task_storage: TaskStorage):
        self.task_id = task_storage.task_id
        self.encoder.load(task_storage.encoder_storage)
        self.policy.load(task_storage.policy_storage)

    def get_task_id(self):
        return self.task_id

    def get_encoder(self):
        return self.encoder

    def get_schema(self):
        return self.encoder.schema

    def is_ready(self):
        return self.ready

    def set_policy(self, new_policy: Policy):
        self.policy = new_policy

    def transform_dataset(self, dataset) -> None:
        pass

    @abstractmethod
    def predict(self, sampling_window_rows) -> tuple:
        """Returns the prediction results for the given sampling windows
        generated input vectors.

        Args:
            sampling_window_rows: filled Firestore dictionary, this dict
                contains all the rows present in bigquery tables.

        Returns:
            Enumerated value for Classification Tasks.
        """
        pass


def download_task_file_from_bucket(credentials_str, bucket_name, file_name) -> str:
    json_dict_service_account = json.loads(credentials_str, strict=False)
    credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
    storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    blob.download_to_filename(tmp_file.name)

    return tmp_file.name


