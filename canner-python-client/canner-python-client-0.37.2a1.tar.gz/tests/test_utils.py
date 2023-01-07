from canner.utils import *
import pandas as pd
import numpy as np

data = [
    [
        "FINISHED",
        "2019-11-20 07:32:21.363",
        209,
        None,
        None,
        "select * from canner.1.sq",
        "f648ac0e-7a87-409f-bed0-27a1fb9e9927",
        None,
        None,
        "20191120_070156_00003_q7byd",
        "default/query/data/20191120_070156_00003_q7byd/data",
        "BASIC_USER",
        0,
        0,
        4,
        True,
    ],
    [
        "FINISHED",
        "2019-11-20 07:30:53.979",
        1301,
        None,
        None,
        "select * from canner.1.sq",
        "f648ac0e-7a87-409f-bed0-27a1fb9e9927",
        None,
        None,
        "20191115_023945_00063_8553e",
        "default/query/data/20191115_023945_00063_8553e/data",
        "BASIC_USER",
        0,
        866,
        0,
        True,
    ],
]
columns = [
    {
        "name": "status",
        "type": "varchar",
        "typeSignature": {
            "rawType": "varchar",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [{"kind": "LONG_LITERAL", "value": 2147483647}],
        },
    },
    {
        "name": "started_at",
        "type": "timestamp",
        "typeSignature": {
            "rawType": "timestamp",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "duration",
        "type": "double",
        "typeSignature": {
            "rawType": "double",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "columns",
        "type": "json",
        "typeSignature": {
            "rawType": "json",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "data",
        "type": "json",
        "typeSignature": {
            "rawType": "json",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "sql",
        "type": "varchar",
        "typeSignature": {
            "rawType": "varchar",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [{"kind": "LONG_LITERAL", "value": 2147483647}],
        },
    },
    {
        "name": "workspace_id",
        "type": "varchar",
        "typeSignature": {
            "rawType": "varchar",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [{"kind": "LONG_LITERAL", "value": 2147483647}],
        },
    },
    {
        "name": "error",
        "type": "json",
        "typeSignature": {
            "rawType": "json",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "data_link",
        "type": "varchar",
        "typeSignature": {
            "rawType": "varchar",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [{"kind": "LONG_LITERAL", "value": 2147483647}],
        },
    },
    {
        "name": "statement_id",
        "type": "varchar",
        "typeSignature": {
            "rawType": "varchar",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [{"kind": "LONG_LITERAL", "value": 2147483647}],
        },
    },
    {
        "name": "location",
        "type": "varchar",
        "typeSignature": {
            "rawType": "varchar",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [{"kind": "LONG_LITERAL", "value": 2147483647}],
        },
    },
    {
        "name": "user_type",
        "type": "varchar",
        "typeSignature": {
            "rawType": "varchar",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [{"kind": "LONG_LITERAL", "value": 2147483647}],
        },
    },
    {
        "name": "in_bound",
        "type": "integer",
        "typeSignature": {
            "rawType": "integer",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "out_bound",
        "type": "integer",
        "typeSignature": {
            "rawType": "integer",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "row_count",
        "type": "integer",
        "typeSignature": {
            "rawType": "integer",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
    {
        "name": "from_cache",
        "type": "boolean",
        "typeSignature": {
            "rawType": "boolean",
            "typeArguments": [],
            "literalArguments": [],
            "arguments": [],
        },
    },
]


class TestDataFactory(object):
    def test_should_be_list_when_data_format_is_list(self):
        data_list = data_factory(data_format="list", columns=columns, data=data)
        assert isinstance(data_list, list), "Should be a list"

    def test_should_be_column_list_in_first_row_when_data_format_is_list(self):
        data_list = data_factory(data_format="list", columns=columns, data=data)
        assert list(data_list)[0] == list(
            map(lambda column: column["name"], columns)
        ), "First row should be column list"

    def test_should_be_data_list_in_last_row_when_data_format_is_list(self):
        data_list = data_factory(data_format="list", columns=columns, data=data)
        assert data_list[1:] == data, "Last row should be data list"

    def test_expect_dataframe_when_data_format_is_df(self):
        data_list = data_factory(data_format="df", columns=columns, data=data)
        assert isinstance(data_list, pd.DataFrame), "Should be a data frame"

    def test_should_be_np_array_when_data_format_is_np(self):
        data_list = data_factory(data_format="np", columns=columns, data=data)
        assert isinstance(data_list, np.ndarray), "Should be a np array"
