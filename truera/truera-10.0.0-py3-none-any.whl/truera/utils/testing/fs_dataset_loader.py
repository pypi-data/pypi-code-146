import pickle

import pandas as pd

from truera import constants

NA_VALUES = [
    '-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A', '#NA', 'NULL', 'NaN',
    '-NaN', 'nan', '-nan'
]

_DATASET_MAP = {
    constants.DATASET_ID_FICO:
        dict(
            data_path="fico",
            data_file_prefix="fico",
            models=["xgboost", "logistic"]
        ),
    constants.DATASET_ID_FICO_PYSPARK:
        dict(
            data_path="fico_pyspark",
            data_file_prefix="fico_pyspark",
            models=["gbt_classifier", "dt_classifier", "rf_classifier"]
        ),
    constants.DATASET_ID_FICOV2:
        dict(
            data_path="ficov2",
            data_file_prefix="fico",
            models=["xgboost", "logistic"]
        ),
    constants.DATASET_ID_LENDINGCLUB:
        dict(
            data_path="lendingclub",
            data_file_prefix="lc",
            models=["xgboost", "logistic"]
        ),
    constants.DATASET_ID_LENDINGCLUB_TRANSFORM:
        dict(
            data_path="lendingclub_transform",
            data_file_prefix="lc_transform",
            models=["xgboost"]
        )
}


def load_data(dataset_id, relative_path='truera/utils/test_data/'):
    assert dataset_id in _DATASET_MAP, "Invalid dataset_id: " + dataset_id
    _dataset_info = _DATASET_MAP[dataset_id]
    data_path = _dataset_info["data_path"]
    data_file_prefix = _dataset_info["data_file_prefix"]

    y_path = '{}{}/data/{}_labels_sample_5k.csv'.format(
        relative_path, data_path, data_file_prefix
    )

    x_num_path = '{}{}/data/{}_num_sample_5k.csv'.format(
        relative_path, data_path, data_file_prefix
    )

    x_raw_path = '{}{}/data/{}_raw_sample_5k.csv'.format(
        relative_path, data_path, data_file_prefix
    )

    y = pd.read_csv(y_path, header=None)
    X_num = pd.read_csv(x_num_path, keep_default_na=False, na_values=NA_VALUES)

    X_raw = pd.read_csv(x_raw_path, keep_default_na=False, na_values=NA_VALUES)

    models = {}
    for model_id in _dataset_info["models"]:
        models[model_id] = pickle.load(
            open(f"{relative_path}{data_path}/models/{model_id}.pkl", "rb"),
            encoding='iso-8859-1'
        )
    return {
        'y_path': y_path,
        'x_raw_path': x_raw_path,
        'x_num_path': x_num_path,
        "y": y,
        "X_raw": X_raw,
        "X_num": X_num,
        "models": models
    }


def load_pyspark_test_data(dataset_id, relative_path='truera/utils/test_data/'):
    assert dataset_id in _DATASET_MAP, "Invalid dataset_id: " + dataset_id
    _dataset_info = _DATASET_MAP[dataset_id]
    data_path = _dataset_info["data_path"]
    data_file_prefix = _dataset_info["data_file_prefix"]

    x_num_path = '{}{}/data/{}.csv'.format(
        relative_path, data_path, data_file_prefix
    )

    X_num = pd.read_csv(x_num_path, keep_default_na=False, na_values=NA_VALUES)

    return {'x_num_path': x_num_path, "X_num": X_num}
