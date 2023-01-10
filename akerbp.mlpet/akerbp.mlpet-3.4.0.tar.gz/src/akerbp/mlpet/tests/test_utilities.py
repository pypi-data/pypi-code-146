import os

import pandas as pd
import yaml
from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import APIKey

from akerbp.mlpet import utilities as utils
from akerbp.mlpet.tests.data.data import (
    FORMATION_TOPS_MAPPER,
    TEST_DF,
    VERTICAL_DEPTHS_MAPPER,
)

ID_COLUMNS = "well_name"
VSH_KWARGS = {
    "nan_numerical_value": -9999,
    "nan_textual_value": "MISSING",
    "VSH_curves": ["GR"],
}

# Assuming COGNITE_API_KEY is set in the environment
credentials = APIKey(os.environ["COGNITE_API_KEY"])
client_config = ClientConfig(
    client_name="test", project="akbp-subsurface", credentials=credentials
)
CLIENT = CogniteClient(client_config)
WELL_NAMES = ["25/10-10"]


def test_get_formation_tops():
    formation_tops_mapper = utils.get_formation_tops(WELL_NAMES, CLIENT)
    assert formation_tops_mapper == FORMATION_TOPS_MAPPER


def test_get_vertical_depths():
    retrieved_vertical_depths = utils.get_vertical_depths(WELL_NAMES, CLIENT)
    # empty_queries should be an empty list for the provided WELL_NAMES
    assert retrieved_vertical_depths == VERTICAL_DEPTHS_MAPPER


def test_remove_wo_label():
    df = utils.drop_rows_wo_label(TEST_DF[["AC", "BS"]], label_column="BS")
    assert df.shape[0] == 8


def test_standardize_names():
    mapper = yaml.load(
        open("src/akerbp/mlpet/tests/data/test_mappings.yaml", "r"),
        Loader=yaml.SafeLoader,
    )
    utils.standardize_names(TEST_DF.columns.tolist(), mapper=mapper)


def test_standardize_group_formation_name():
    assert utils.standardize_group_formation_name("ØRN") == "ORN"


def test_map_formation_group_system():
    tests = pd.Series(["UNDIFFERENTIATED", "FOO BAR", "NO FORMAL NAME 1", "HeGrE"])
    tests = tests.apply(utils.standardize_group_formation_name)
    assert utils.map_formation_group_system(tests, MissingValue=-9999) == (
        ("UNKNOWN FM", -9999, "UNKNOWN FM", -9999),
        ("UNKNOWN GP", -9999, "UNKNOWN GP", "HEGRE GP"),
        (-9999, -9999, -9999, "TRIASSIC SY"),
    )


def test_get_well_metadata():
    metadata = utils.get_well_metadata(client=CLIENT, well_names=WELL_NAMES)
    assert metadata[WELL_NAMES[0]]["CDF_wellName"] == WELL_NAMES[0]


def test_get_cognite_client_no_args_returns_logged_in_client():
    client = utils.get_cognite_client()
    logged_in = client.login.status().logged_in
    assert logged_in


def test_get_cognite_client_pass_api_key_returns_logged_in_client():
    api_key = os.environ["COGNITE_API_KEY"]
    client = utils.get_cognite_client(
        cognite_api_key=api_key,
    )
    logged_in = client.login.status().logged_in
    assert logged_in


def test_get_cognite_client_wrong_api_key_return_client_not_logged_in():
    api_key = "wrong_key_go_home"
    client = utils.get_cognite_client(cognite_api_key=api_key)
    logged_in = client.login.status().logged_in
    assert not logged_in
