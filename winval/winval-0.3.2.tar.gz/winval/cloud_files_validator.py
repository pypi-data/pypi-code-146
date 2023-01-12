import argparse
import json
import re
import google
import subprocess
from google.cloud import storage

from winval.workflow_var import WorkflowVarType
from winval.wdl_parser import WdlParser
from winval import logger


def get_args():
    parser = argparse.ArgumentParser('cloud_files_validator', description='Validate GCS inputs actually exist')
    parser.add_argument('--json', required=True)
    parser.add_argument('--wdl', required=True)
    return parser.parse_args()


def split_uri(uri: str):
    matches = re.match(r"gs://(.*?)/(.*)", uri)
    if matches:
        return matches.groups()
    else:
        return None, None


def blob_exists(bucket_name, filepath):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filepath)
    return blob.exists()


class CloudFilesValidator:

    def __init__(self, wdl_file: str, json_file: str):
        logger.debug('-----------------------------')
        logger.debug('---- CloudFilesValidator ----')
        logger.debug('-----------------------------')
        self.json_file = json_file
        self.workflow_vars = None
        wdl_inputs = WdlParser(wdl_file).parse_workflow_variables()
        self.workflow_vars = wdl_inputs.workflow_vars
        with open(json_file) as jf:
            wdl_inputs.fill_values_from_json(json.load(jf))
        self.validated_files = []
        self.non_validated_files = []

    def validate(self) -> bool:
        for workflow_var in self.workflow_vars.values():
            if workflow_var.type == WorkflowVarType.FILE and workflow_var.value is not None:
                self.validate_file(workflow_var.value)
            elif workflow_var.type == WorkflowVarType.FILE_ARRAY and workflow_var.value is not None:
                for file_uri in workflow_var.value:
                    self.validate_file(file_uri)

        logger.debug('-------------------------------------------')
        summary_str = f"Existing URI's: {len(self.validated_files)}, Non-existing URI's: {len(self.non_validated_files)}"
        logger.info(summary_str)
        for fn in self.non_validated_files:
            logger.error(f'Missing URI: {fn}')

        return len(self.non_validated_files) == 0

    def validate_file(self, file_uri: str):
        file_uri = file_uri.replace('"', '')
        if 'gs://' not in file_uri:
            return
        bucket_name, file_name = split_uri(file_uri)
        if bucket_name is None:
            self.non_validated_files.append(file_uri)
        try:
            if blob_exists(bucket_name, file_name):
                self.validated_files.append(file_uri)
            else:
                self.non_validated_files.append(file_uri)
        # blob_exists requires storage.bucket.get access which might be forbidden, 
        # yet objects in this bucket can still be accessed by gsutil
        # Could not fine a python api to access the object in this case
        except google.api_core.exceptions.Forbidden:
            process = subprocess.run(f'gsutil ls {file_uri}'.split(), capture_output=True)
            if process.returncode == 0:
                self.validated_files.append(file_uri)
            else:
                self.non_validated_files.append(file_uri)

    def validate_files_in_object(self, o):
        if type(o) == dict:
            for key, value in o.items():
                self.validate_files_in_object(value)
        elif type(o) == list:
            for value in o:
                self.validate_files_in_object(value)
        elif type(o) == str:
            self.validate_file(o)


def main():
    """
    validate all GCP URLs in json inputs point to existing objects
    """
    args = get_args()
    validated = CloudFilesValidator(args.wdl, args.json).validate()
    if not validated:
        raise RuntimeError('Found non existing files!')


if __name__ == '__main__':
    main()
