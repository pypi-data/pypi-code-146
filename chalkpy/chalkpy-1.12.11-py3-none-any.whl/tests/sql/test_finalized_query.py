from sqlalchemy import text

from chalk.features import features, unwrap_feature
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.sql.finalized_query import FinalizedChalkQuery, Finalizer


@features
class ColNameMappingFeatures:
    id: str
    foo: str
    bar: str


def test_get_col_name_mapping():
    finalized_query = FinalizedChalkQuery(
        query=text("select 1"),
        params={},
        finalizer=Finalizer.ALL,
        incremental_settings=None,
        source=BaseSQLSource(name=""),
        fields={
            "id": unwrap_feature(ColNameMappingFeatures.id),
            "foo": unwrap_feature(ColNameMappingFeatures.foo),
            "bar": unwrap_feature(ColNameMappingFeatures.bar),
        },
    )
    col_name_mapping = finalized_query.get_col_name_mapping(result_columns=["ID", "foo", "bAr"], expected_features=None)
    assert col_name_mapping == {
        "ID": "col_name_mapping_features.id",
        "foo": "col_name_mapping_features.foo",
        "bAr": "col_name_mapping_features.bar",
    }


def test_get_col_name_mapping_with_expected():
    finalized_query = FinalizedChalkQuery(
        query=text("select 1"),
        params={},
        finalizer=Finalizer.ALL,
        incremental_settings=None,
        source=BaseSQLSource(name=""),
        fields={},
    )
    col_name_mapping = finalized_query.get_col_name_mapping(
        result_columns=["ID", "foo", "bAr"],
        expected_features=[
            unwrap_feature(ColNameMappingFeatures.id),
            unwrap_feature(ColNameMappingFeatures.foo),
            unwrap_feature(ColNameMappingFeatures.bar),
        ],
    )
    assert col_name_mapping == {
        "ID": "col_name_mapping_features.id",
        "foo": "col_name_mapping_features.foo",
        "bAr": "col_name_mapping_features.bar",
    }
