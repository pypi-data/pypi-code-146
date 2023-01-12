from appdirs import user_config_dir
import boto3
import csv
from datetime import datetime
from hashlib import sha256
from humanize import naturalsize
import io
import machineid
from os import stat
from os.path import exists
from pathlib import Path
import pkg_resources
import requests
import yaml

from tagbackup.constants import API_URL, HASH_PREFIX, HASH_SUFFIX


def api_post(url, device_id, data, add_headers):
    timestamp = get_timestamp()
    headers = {}

    if add_headers:
        headers = {
            "tagbackup-device": device_id,
            "tagbackup-timestamp": timestamp,
            "tagbackup-hash": generate_hash(timestamp, device_id),
        }

    try:
        r = requests.post(f"{API_URL}{url}", json=data, headers=headers)
        response = r.json()
        if response and "isValid" in response:
            return response
    except:
        pass

    raise Exception("Error: there was a problem communicating with TagBackup")


def download_file(resource, local_filename, bucket, cloud_filename):
    try:
        resource.Object(bucket, cloud_filename).download_file(local_filename)
        return True
    except:
        return False


def file_exists(filename):
    return exists(filename)


def generate_hash(timestamp, device_id):
    prehash = "::".join(
        [HASH_PREFIX, timestamp, get_machine_id(), device_id, HASH_SUFFIX]
    )
    return sha256(prehash.encode("utf-8")).hexdigest()


def get_config_path():
    return Path(user_config_dir()) / "tagbackup.yaml"


def get_device_id():
    try:
        with open(get_config_path(), "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        device_id = config.get("device", "")
        if len(device_id) == 36:
            return device_id
    except:
        pass

    return None


def get_filesize(file, human_readable):
    filesize = stat(file).st_size
    if human_readable:
        return naturalsize(filesize, binary=True)

    return filesize


def get_machine_id():
    return machineid.hashed_id("tagbackup")


def get_s3_resource(key, secret):
    try:
        return boto3.resource(
            "s3",
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )
    except:
        return None


def get_timestamp():
    return str(round(datetime.utcnow().timestamp()))


def get_version():
    return pkg_resources.get_distribution("tagbackup").version


def set_device_id(device_id):
    try:
        with open(get_config_path(), "w") as file:
            yaml.dump({"device": str(device_id)}, file)

        return True
    except:
        pass

    return False


def tags_to_csv(tags):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(tags)
    return output.getvalue()


def upload_file(resource, local_filename, bucket, cloud_filename):
    try:
        resource.meta.client.upload_file(local_filename, bucket, cloud_filename)
        return True
    except:
        return False
