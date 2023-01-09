"""Tests for utils.py."""
from unittest.mock import Mock

import pytest

from bitfount.federated.algorithms.column_avg import ColumnAverage
from bitfount.federated.algorithms.sql_query import SqlQuery
from bitfount.federated.protocols.results_only import ResultsOnly
from bitfount.federated.utils import _PROTOCOLS
from bitfount.schemas.exceptions import SchemaClassError
from bitfount.schemas.utils import _dict_to_schema, _obj_to_schema, bf_dump, bf_load
from tests.utils.helper import unit_test


@unit_test
def test_dump_with_empty_object_error() -> None:
    """Tests that empty object dump raises error."""
    with pytest.raises(SchemaClassError):
        bf_dump(None)  # type: ignore[arg-type] # Reason: purpose of test


@unit_test
def test_depth_greater_than5_raises_error_dict_to_schema() -> None:
    """Tests that depth greater than 5 raises error."""
    with pytest.raises(SchemaClassError):
        _dict_to_schema(Mock(), Mock(), depth=6)


@unit_test
def test_depth_greater_than5_raises_error_obj_to_schema() -> None:
    """Tests that depth greater than 5 raises error."""
    with pytest.raises(SchemaClassError):
        _obj_to_schema(Mock(), depth=6)


@unit_test
def test_dump_with_multi_algorithm_protocol() -> None:
    """Tests that dumping multi algorithm protocol works."""
    algo = ColumnAverage(field="a", table_name="b")
    algo2 = SqlQuery(query="SELECT * FROM a")
    # ResultsOnly is not a multi algorithm protocol but we are using it as one just
    # for testing purposes
    protocol = ResultsOnly(
        algorithm=[algo, algo2]  # type: ignore[arg-type] # Reason: see above
    )
    assert bf_dump(protocol) == {
        "algorithm": [
            {"field": "a", "table_name": "b", "class_name": "bitfount.ColumnAverage"},
            {
                "query": "SELECT * FROM a",
                "table": None,
                "class_name": "bitfount.SqlQuery",
            },
        ],
        "class_name": "bitfount.ResultsOnly",
    }


@unit_test
def test_load_with_multi_algorithm_protocol() -> None:
    """Tests that loading multi algorithm protocol works."""
    protocol = bf_load(
        {
            "algorithm": [
                {
                    "field": "a",
                    "table_name": "b",
                    "class_name": "bitfount.ColumnAverage",
                },
                {
                    "query": "SELECT * FROM a",
                    "table": None,
                    "class_name": "bitfount.SqlQuery",
                },
            ],
            "class_name": "bitfount.ResultsOnly",
        },
        _PROTOCOLS,
    )
    assert isinstance(protocol, ResultsOnly)
    # ResultsOnly is not a multi algorithm protocol but we are using it as one just
    # for testing purposes
    algo = protocol.algorithm[0]  # type: ignore[index] # Reason: See above
    algo2 = protocol.algorithm[1]  # type: ignore[index] # Reason: See above
    assert isinstance(algo, ColumnAverage)
    assert isinstance(algo2, SqlQuery)
    assert algo.field == "a"
    assert algo.table_name == "b"
    assert algo2.query == "SELECT * FROM a"
