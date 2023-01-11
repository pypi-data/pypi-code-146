import os

import requests
from os.path import getsize
from pathlib import Path
from typing import Tuple
from datomizer import Datomizer
from datomizer.utils.constants import (MANAGEMENT_POST_ADD_ORIGIN_PRIVATE_DATASOURCE, MANAGEMENT_GET_PUT_PRESIGNED_URL,
                                       MANAGEMENT_POST_ADD_TARGET_PRIVATE_DATASOURCE)
from datomizer.utils.general import ID, URL
from datomizer.utils.thresholds import MIN_ROW_COUNT, MAX_COLUMN_COUNT, MAX_FILE_SIZE_MB, MB


def post_create_origin_private_datasource(datomizer: Datomizer) -> Tuple[int, str]:
    datasource_response = datomizer.get_response_json(requests.post, url=MANAGEMENT_POST_ADD_ORIGIN_PRIVATE_DATASOURCE)

    return datasource_response[ID]


def get_put_presigned_url(datomizer: Datomizer, datasource_id, path: str):
    put_presigned_response = datomizer.get_response_json(requests.get,
                                                         url=MANAGEMENT_GET_PUT_PRESIGNED_URL,
                                                         url_params=[datasource_id, path])
    return put_presigned_response[URL]


def create_origin_private_datasource_from_path(datomizer: Datomizer, path: Path):
    datasource_id = post_create_origin_private_datasource(datomizer)
    upload_path(datomizer, datasource_id, path)
    return datasource_id


def create_target_private_datasource(datomizer: Datomizer) -> int:
    datasource = datomizer.get_response_json(requests.post, url=MANAGEMENT_POST_ADD_TARGET_PRIVATE_DATASOURCE)
    return datasource[ID]


def upload_path(datomizer: Datomizer, datasource_id, path: Path):
    for file in os.listdir(path):
        put_presigned_url = get_put_presigned_url(datomizer, datasource_id, file)

        with open(f"{path}/{file}", 'rb') as temp_file:
            response = requests.put(url=put_presigned_url, data=temp_file)
            Datomizer.validate_response(response, "Upload to put presigned url")


def save_df_to_csv(df_map: dict, temp_dir):
    for df_name in df_map:
        path = f"{temp_dir}/{df_name}.csv"
        df = df_map[df_name]
        df_type = f"{type(df).__module__}.{type(df).__name__}"

        if df_type == "pandas.core.frame.DataFrame":
            df.to_csv(path, index=False)
        elif df_type == "pyspark.sql.dataframe.DataFrame":
            df.write.csv(path=path, mode='overwrite', header='true')


def validate_data_size_limits(path, delimiter):
    total_size = 0
    row_count = 0
    column_count = 0
    for file in os.listdir(path):
        with open(f"{path}/{file}") as csv_file:
            first_line = csv_file.readline()
            your_data = csv_file.readlines()

            total_size += round(getsize(path) / MB, 3)
            row_count += len(your_data)
            column_count += first_line.count(delimiter) + 1

    assert total_size <= MAX_FILE_SIZE_MB, \
        f"File size: {total_size}MB - exceeds the limit of: {MAX_FILE_SIZE_MB}MB"
    assert row_count >= MIN_ROW_COUNT, \
        f"Row count is {row_count} - is below the minimum limit of: {MIN_ROW_COUNT} rows"
    assert column_count <= MAX_COLUMN_COUNT, \
        f"Column count is {column_count} - exceeds the limit of: {MAX_COLUMN_COUNT} columns"
