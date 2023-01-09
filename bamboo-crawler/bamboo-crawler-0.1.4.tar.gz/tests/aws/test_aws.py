import json
import os
import subprocess
import time
from threading import Thread

import boto3
import pytest
import yaml


@pytest.fixture
def moto_environment() -> None:  # type: ignore
    overwrite_envs = {
        "AWS_ACCESS_KEY_ID": "1234",
        "AWS_SECRET_ACCESS_KEY": "5678",
    }
    recovery_values = {
        name: os.environ.get(name) for name in overwrite_envs.keys()
    }
    os.environ.update(overwrite_envs)
    yield
    for k, v in recovery_values.items():
        if v is None:
            del os.environ[k]
        else:
            os.environ[k] = v


def read_and_discard_in_background(file) -> None:  # type: ignore
    Thread(target=lambda f: f.read(), args=(file,), daemon=True).start()


@pytest.fixture
def moto_server_s3(moto_environment) -> None:  # type: ignore
    with subprocess.Popen(
        ["moto_server", "s3", "-p", "5000"], stderr=subprocess.PIPE
    ) as s3:
        read_and_discard_in_background(s3.stderr)
        time.sleep(0.5)
        with open("tests/aws/env.yml") as f:
            y = yaml.safe_load(f.read())
        boto_s3 = boto3.resource("s3", **y["s3_config"])
        boto_s3.create_bucket(
            Bucket="sample-bucket",
            CreateBucketConfiguration={
                "LocationConstraint": y["s3_config"]["region_name"]
            },
        )
        yield
        s3.terminate()


@pytest.fixture
def moto_server_sqs(moto_environment) -> None:  # type: ignore
    with subprocess.Popen(
        ["moto_server", "sqs", "-p", "5001"], stderr=subprocess.PIPE
    ) as sqs:
        read_and_discard_in_background(sqs.stderr)
        time.sleep(0.5)
        with open("tests/aws/env.yml") as f:
            y = yaml.safe_load(f.read())
        boto_sqs = boto3.resource("sqs", **y["sqs_config"])
        boto_sqs.create_queue(QueueName="sample-queue")
        yield
        sqs.terminate()


def run_recipe(taskname: str) -> subprocess.CompletedProcess:
    c = subprocess.run(
        [
            "python3",
            "-m",
            "bamboo_crawler",
            "-r",
            "tests/aws/recipe.yml",
            "-e",
            "tests/aws/env.yml",
            "-t",
            taskname,
        ],
        stdout=subprocess.PIPE,
    )
    return c


def test_aws_inputter_and_outputter(moto_server_s3, moto_server_sqs) -> None:  # type: ignore
    outputter = run_recipe("aws_outputter")
    assert outputter.returncode == 0, "Outputter success"
    inputter = run_recipe("aws_inputter")
    assert inputter.returncode == 0, "Inputter success"
    j = json.loads(inputter.stdout)
    assert j["sampledata"] == "ABCDEFGHIJKLMN"
