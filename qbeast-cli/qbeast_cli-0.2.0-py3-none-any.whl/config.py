import json
import os
from pathlib import Path
from qbeast.predefs import qbeast_config_path, profile_filename, curator_config_filename
import yaml

ENDPOINT = os.environ.get("ENDPOINT_QBEAST", 'https://v0.studio.qbeast.io')
_BEARER_TOKEN_ = ''

JSON_PROFILE = {}

AWS_PROFILE = ''


def get_profile_config():
    profile_config = {
        "bearer_token": get_bearer_token(),
        "endpoint": ENDPOINT
    }
    return profile_config


def update_endpoint(new_endpoint):
    global ENDPOINT
    ENDPOINT = new_endpoint


def get_bearer_token():
    global _BEARER_TOKEN_
    if _BEARER_TOKEN_ == '':
        if os.path.exists(qbeast_config_path + '/' + profile_filename):
            with open(qbeast_config_path + '/' + profile_filename, 'r') as f:
                _BEARER_TOKEN_ = json.loads(f.read())['bearer_token']
    return _BEARER_TOKEN_


def update_bearer_token(new_token):
    global _BEARER_TOKEN_
    _BEARER_TOKEN_ = new_token


# Creates the Sharing Profile
def create_profile():
    Path(qbeast_config_path).mkdir(parents=True, exist_ok=True)
    with open(qbeast_config_path + '/' + profile_filename, "w") as profile_file:
        profile_content = json.dumps(get_profile_config())
        profile_file.write(profile_content + '\n')


# Load profile with credentials
def load_profile(profile_file):
    global JSON_PROFILE
    JSON_PROFILE = json.loads(open(profile_file).read())


def create_dbt_profile():
    info = {"ermes_antiphishing": {
        "outputs": {
            "dev": {"host": "localhost", "method": "thrift", "port": 10001, "schema": "dbt_dev", "type": "spark"}
        },
        "target": "dev"}
    }
    with open("/tmp/profiles.yml", "w") as profile_file:
        yaml.dump(info, profile_file)


# Load S3 credentials from profile
def load_aws_credentials():
    global AWS_PROFILE
    AWS_PROFILE = os.environ.get("AWS_PROFILE", "")


# Curator config file
def write_curator_config(config_key, config_value):
    config = dict()
    if not os.path.exists(qbeast_config_path + "/" + curator_config_filename):
        Path(qbeast_config_path).mkdir(parents=True, exist_ok=True)
    if os.path.exists(qbeast_config_path + "/" + curator_config_filename):
        with open(qbeast_config_path + "/" + curator_config_filename, "r") as f:
            config = json.loads(f.read())
    config[config_key] = config_value
    with open(qbeast_config_path + "/" + curator_config_filename, "w") as f:
        f.write(json.dumps(config))

def read_curator_config(config_key):
    if os.path.exists(qbeast_config_path + "/" + curator_config_filename):
        with open(qbeast_config_path + "/" + curator_config_filename, "r") as f:
            try:
                config = json.loads(f.read())
                return config[config_key]
            except:
                return None
    return None