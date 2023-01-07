from canner.client import Client
import pytest
import canner
from uuid import uuid4
from .config import TestConfig
from faker import Faker
from logging import getLogger


logger = getLogger("conftest")


# case one, jupyter secret-based client, the user is jupyter user, so the role is data consumer.
secret_client = canner.client.bootstrap(
    endpoint=TestConfig.ENDPOINT,
    workspace_id=TestConfig.WORKSPACE_ID,
    headers={
        "X-CANNERFLOW-SECRET": TestConfig.JUPYTER_SECRET,
        "X-CANNERFLOW-WORKSPACE-ID": TestConfig.WORKSPACE_ID,
    },
)

# case two, token-based client, the user and role will follow by your token information
token_client = canner.client.bootstrap(
    endpoint=TestConfig.ENDPOINT,
    workspace_id=TestConfig.WORKSPACE_ID,
    token=TestConfig.PERSONAL_ACCESS_TOKEN,
)


@pytest.fixture(scope="session", params=[secret_client, token_client])
def canner_client(request):
    return request.param

@pytest.fixture(scope="session")
def jupyter_secret_client():
    return secret_client

@pytest.fixture(scope="session")
def user_token_client():
    return token_client


# This is a general function which used by fixture below clean temporary files
def file_cleaner(canner_client: Client, filename: str):
    ### delete file
    canner_client.delete_file(filename)
    logger.info(f"tested temp file '{filename}' delete ...OK!!")


@pytest.fixture(scope="function")
def csv_filename(canner_client: Client):
    fake = Faker()
    filename = fake.file_name(extension="csv")
    filename = f"{str(uuid4())[:8]}-{filename}"
    logger.info(f"csv filename = {filename}")
    yield filename
    ### delete file
    file_cleaner(canner_client, filename)


@pytest.fixture(scope="function")
def json_filename(canner_client: Client):
    fake = Faker()
    filename = fake.file_name(extension="json")
    filename = f"{str(uuid4())[:8]}-{filename}"
    logger.info(f"json filename = {filename}")
    yield filename
    ### delete file
    file_cleaner(canner_client, filename)


@pytest.fixture(scope="function")
def binary_filename(canner_client: Client):
    fake = Faker()
    filename = fake.file_name(extension="bin")
    filename = f"{str(uuid4())[:8]}-{filename}"
    logger.info(f"bin filename = {filename}")
    yield filename
    ### delete file
    file_cleaner(canner_client, filename)


@pytest.fixture(scope="function")
def binary_filepaths(canner_client: Client):
    fake = Faker()
    filepaths = []
    for _ in range(0, fake.random_int(1, 5)):
        filepath = fake.file_path(depth=fake.random_int(0, 2), extension="bin")
        filepath = filepath.replace("/", f"/{str(uuid4())[:4]}-")
        logger.info(f"bin filepath = {filepath}")
        filepaths.append(filepath)
    yield filepaths
    ### delete file
    for filepath in filepaths:
        file_cleaner(canner_client, filepath)


@pytest.fixture(scope="function")
def png_filename(canner_client: Client):
    fake = Faker()
    filename = fake.file_name(extension="png")
    filename = f"{str(uuid4())[:8]}-{filename}"
    logger.info(f"image png filename = {filename}")
    yield filename
    ### delete file
    file_cleaner(canner_client, filename)
