import os
import warnings
from typing import List
from urllib.parse import urljoin

import requests


def init_upload_and_run(
    base_url: str, model_name: str, input_files: List[str]
) -> tuple:

    # init model
    timestamp = init(base_url, model_name)

    # upload unput files
    upload_input_files(base_url, model_name, timestamp, input_files)

    # run model
    return run(base_url, model_name, timestamp)


def init(base_url: str, model_name: str) -> str:
    url_init = urljoin(base_url, f"model/{model_name}")
    response_init = requests.post(url_init)
    if response_init.status_code != 200:
        raise RuntimeError(response_init.json()["detail"]["output"])

    return response_init.json()["timestamp"]


def upload_input_files(base_url, model_name, timestamp, input_files) -> None:
    url_upload = urljoin(base_url, "model")
    files = [("files", open(input_file)) for input_file in input_files]
    data = {"model_name": model_name, "timestamp": timestamp}

    response = requests.post(url_upload, files=files, data=data)

    if response.status_code != 200:
        raise RuntimeError(response.json()["detail"]["output"])


def run(base_url, model_name, timestamp) -> tuple:
    url = urljoin(base_url, f"model/{model_name}/{timestamp}/run")
    response = requests.post(url)

    if response.status_code != 200:
        raise RuntimeError(response.json()["detail"]["output"])

    output_lines = response.json()["output"].split("\n")
    model_name = response.json()["model_name"]
    timestamp = response.json()["timestamp"]
    artefacts = response.json()["artefacts"]
    return model_name, timestamp, output_lines, artefacts


def get_artefact_names(base_url, model_name, timestamp):
    url = urljoin(base_url, f"artefacts/{model_name}/{timestamp}")
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(response.json()["detail"]["output"])

    return response.json()["artefacts"]


def download_artefact(base_url, model_name, timestamp, input_dir, artefact):
    url = urljoin(base_url, f"artefact/{model_name}/{timestamp}/{artefact}")
    response = requests.get(url)
    if response.status_code != 200:
        warnings.warn("The requested artefact %s is not available!" % artefact)
    else:
        with open(os.path.join(input_dir, artefact), "wb") as file:
            file.write(response.content)
