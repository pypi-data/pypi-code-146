import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TestConfig(object):
    # Prevent pytest from trying to collect TestConfig as tests:
    __test__ = False

    ENDPOINT = os.getenv("ENDPOINT", "http://localhost:3000")
    WORKSPACE_ID = os.getenv("WORKSPACE_ID", "")
    PERSONAL_ACCESS_TOKEN = os.getenv("CANNER_PERSONAL_ACCESS_TOKEN", "")
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "test_sources")
    SAMPLE_JSON = os.path.join(TEST_SOURCE_PATH, "test_json_sample.json")
    SAMPLE_IMAGE = os.path.join(TEST_SOURCE_PATH, "test_image_sample.png")

    SAMPLE_01_MBCS_CP950_CSV = os.path.join(
        TEST_SOURCE_PATH, "test_csv_sample_01_mbcs_cp950.csv"
    )
    SAMPLE_02_UTF8_BOM_CSV = os.path.join(
        TEST_SOURCE_PATH, "test_csv_sample_02_utf8_bom.csv"
    )
    SAMPLE_03_CP950_CSV = os.path.join(TEST_SOURCE_PATH, "test_csv_sample_03_cp950.csv")
    SAMPLE_04_UTF8_CSV = os.path.join(TEST_SOURCE_PATH, "test_csv_sample_04_utf8.csv")

    SAMPLE_01_MULTIPLE_TYPE_FIELDS_FORMAT_PARQUET = os.path.join(
        TEST_SOURCE_PATH, "test_multi_types_fields_format.parquet"
    )
    SAMPLE_02_ONLY_TIMESTAMP_FIELDS_FORMAT_PARQUET = os.path.join(
        TEST_SOURCE_PATH, "test_only_timestamp_fields_format.parquet"
    )
    SAMPLE_03_ONLY_TIMESTAMP_ZONE_FIELDS_FORMAT_PARQUET = os.path.join(
        TEST_SOURCE_PATH, "test_only_timestamp_zone_fields_format.parquet"
    )
    SAMPLE_04_TIMESTAMP_WITH_TIMESTAMP_ZONE_FIELDS_FORMAT_PARQUET = os.path.join(
        TEST_SOURCE_PATH, "test_timestamp_with_timestamp_zone_fields_format.parquet"
    )

    JUPYTER_SECRET = os.getenv("CANNER_JUPYTER_SECRET", "jupyter-secret")

    def __post_init__(self):
        if not self.WORKSPACE_ID:
            raise EnvironmentError("Need canner workspace ID.")
        if not self.PERSONAL_ACCESS_TOKEN:
            raise EnvironmentError("Need canner web personal access token.")


#
