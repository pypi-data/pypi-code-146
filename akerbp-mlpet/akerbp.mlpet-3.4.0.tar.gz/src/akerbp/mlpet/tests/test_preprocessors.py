import os

from pandas.api.types import is_float_dtype, is_integer_dtype

from akerbp.mlpet import Dataset, preprocessors
from akerbp.mlpet.tests.data.data import TEST_DF

DS = Dataset({"id_column": "foobar"}, os.path.abspath(r"."))
DS.save_df_to_cls(TEST_DF)


def test_encode_columns():
    df_encoded = preprocessors.encode_columns(
        DS.df_original.copy(),
        columns_to_encode=[
            "GROUP",
        ],
        formations_map=DS.formations_map,
        groups_map=DS.groups_map,
    )
    assert is_float_dtype(df_encoded["GROUP"])


def test_onehot_encode_columns():
    categories_to_keep = ["GROUP_ROGALAND"]
    df_encoded, encoded_columns = preprocessors.onehot_encode_columns(
        DS.df_original.copy(),
        columns_to_onehot_encode=[
            "GROUP",
        ],
        categories_to_keep=categories_to_keep,
    )
    encoded_columns = encoded_columns["onehot_columns"]
    for column in encoded_columns:
        assert is_integer_dtype(df_encoded[column])
    assert len(encoded_columns) == len(categories_to_keep)


def test_remove_outliers():
    preprocessors.remove_outliers(TEST_DF, outlier_curves=["GR", "NEU", "RMED", "RDEP"])
