from dataclasses import dataclass
from abc import ABC, abstractmethod


class BasicTrainingServiceException(ABC):

    @abstractmethod
    def get_message(self, **key_args):
        pass


@dataclass
class NoParquetFileFound(FileNotFoundError, BasicTrainingServiceException):
    file_name: str

    def get_message(self, **key_args):
        return f" Could not find parquet file {self.file_name} at {key_args['gcs_file_path']}"


@dataclass
class ErrorWhileTrainingModel(Exception):  # TODO: this is a too broad exception specific errors should be captured

    def get_message(self, **key_args):
        return f"There was an error during model training, please refer to service logs for more info"


@dataclass
class WrongLabelValue(Exception):
    label_value: str

    def get_message(self, **key_args):
        return f"Wrong label value processing data: {self.label_value}"

