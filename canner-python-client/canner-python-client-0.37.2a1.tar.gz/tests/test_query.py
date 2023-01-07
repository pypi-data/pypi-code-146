from pandas.core.frame import DataFrame
import pytest
import numpy as np
import pandas as pd
from canner.client import Client
from canner.dto import SqlQueryStatus
from canner.exceptions import CannerError
from canner.query import Query as CannerQuery

# Use jupyter_secret_client, because jupyter_user is data consumer role and not has permission to list saved query
def test_list_saved_query_failed_when_user_role_not_has_permission(jupyter_secret_client: Client):
    # Arrange
    workspace_id = jupyter_secret_client.workspace.workspace_id
    expected = {
        'error_code': 'GRAPHQL_ADMISSION_CONTROL_FORBIDDEN',
        'message': f'This API need WorkspaceOwner,WorkspaceDataAnalyst of scope {workspace_id}, but not found in user roles'
    }
    try:
        jupyter_secret_client.list_saved_query()
    except CannerError as error:
        # Assert exception message if getting the failed when list saved query
        assert (str(error.error_code) == expected['error_code']), f"should be throw error with error_code {expected['error_code']}"
        assert (str(error.message) == expected['message']), f"should be throw error with message {expected['message']}"


# Use user_token_client, because jupyter_secret_client is data consumer role, not permission to list saved query
def test_list_saved_query_success_when_user_role_has_permission(user_token_client: Client):
    saved_query = user_token_client.list_saved_query()
    assert isinstance(saved_query, list), "should get a list"


# Use jupyter_secret_client, because jupyter_user is data consumer role and not has permission to list saved query
def test_use_saved_query_failed_when_user_role_not_has_permission(jupyter_secret_client: Client):
     # Arrange
    workspace_id = jupyter_secret_client.workspace.workspace_id
    expected = {
        'error_code': 'GRAPHQL_ADMISSION_CONTROL_FORBIDDEN',
        'message': f'This API need WorkspaceOwner,WorkspaceDataAnalyst of scope {workspace_id}, but not found in user roles'
    }
    try:
        saved_query = jupyter_secret_client.list_saved_query()
        if len(saved_query) is 0:
            return
        query = jupyter_secret_client.use_saved_query(saved_query[0])
        query.wait_for_finish(timeout=300)
    except CannerError as error:
        # Assert exception message if getting the failed when list saved query
        assert (str(error.error_code) == expected['error_code']), f"should be throw error with error_code {expected['error_code']}"
        assert (str(error.message) == expected['message']), f"should be throw error with message {expected['message']}"
    


# Use user_token_client, because jupyter_secret_client is data consumer role, not permission to list saved query
def test_use_saved_query_success_when_user_role_has_permission(user_token_client: Client):
    saved_query = user_token_client.list_saved_query()
    if len(saved_query) is 0:
        return
    query = user_token_client.use_saved_query(saved_query[0])
    query.wait_for_finish(timeout=300)
    print(query)
    assert isinstance(query, CannerQuery), "should get a query instance"
    assert type(query.id) == str, "query id should be a string"
    assert isinstance(query.status, SqlQueryStatus), "query status should a string"
    assert type(query.row_count) == int, "query row_count should be a int"
    assert type(query.statement_id) == str, "query statement_id should a string"

    assert isinstance(
        query.columns, list
    ), "columns should be list, but got {columns}".format(columns=query.columns)

    first = query.get_first()
    assert len(first) == 2, "should only get 2 (includes one column row)"

    all_data = query.get_all()
    assert (
        len(all_data) == query.row_count + 1
    ), "should get row_count + 1 (includes the column)"

    any_data = query.get(10, 3)
    assert len(any_data) <= 11, "should get less than 11 rows (includes the column)"

    query.data_format = "df"
    first = query.get_first()
    assert isinstance(first, pd.DataFrame), "should be a dataframe"

    query.data_format = "np"
    first = query.get_first()
    assert isinstance(first, np.ndarray), "should be a np array"


def test_gen_query_with_row_data(canner_client: Client):
    query = canner_client.gen_query(
        "SELECT CAST(ROW(ARRAY[1], 2.0) AS ROW(x ARRAY(BIGINT), y DOUBLE))",
        cache_refresh=True,
    )
    query.wait_for_finish(timeout=300)
    assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
    assert query.row_count == 1, "should have row_count"
    assert len(query.get_first(1)) == 2, "should get two columns"


def test_gen_query_with_empty_data(canner_client: Client):
    query = canner_client.gen_query(
        "select * from tpch.tiny.lineitem limit 0", cache_refresh=True
    )
    query.wait_for_finish(timeout=300)
    assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
    assert query.row_count == 0, "should have row_count"
    assert len(query.get_first(1)) == 1, "should only get column"


def test_gen_query_with_empty_data_in_df(canner_client: Client):
    query = canner_client.gen_query(
        "select * from tpch.tiny.lineitem limit 0", cache_refresh=True, data_format="df"
    )
    query.wait_for_finish(timeout=300)
    assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
    assert query.row_count == 0, "should have row_count"
    df = query.get_all()

    column_results = DataFrame(df).columns.tolist()
    assert len(column_results) != 0, "should get columns in data frame"


def test_gen_query(canner_client: Client):
    query = canner_client.gen_query(
        "select * from tpch.tiny.lineitem limit 1000", cache_refresh=True
    )
    query.wait_for_finish(timeout=300)
    assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
    assert query.row_count > 0, "should have row_count"
    assert len(query.get_first(1)) == 2, "should get 2 rows include column"


def test_get_data_flow(canner_client: Client):
    # NOTE: Because query sql result for "cache_refresh" = false will make data disappear in v1.109.0
    # So we need to set "cache_refresh" is true to close caching result for preventing the issue.
    query = canner_client.gen_query(
        """ SELECT * FROM (
        VALUES (1, 10), (2, 20), (3, 30), (4, 40), (5, 50), (6, 60), (7, 70), (8, 80), (9, 90), (10, 100)
    ) AS testtable(col, col10)
    """, cache_refresh=True)

    query.wait_for_finish(timeout=10, period=3)
    data = list(query.get_all())
    assert data[0] == ["col", "col10"]
    data = data[1:11]  # remove header
    assert len(data) is 10

    first3 = query.get_first(limit=3)
    first3 = first3[1:4]  # remove header
    assert len(first3) is 3
    assert first3 == data[0:3]

    last3 = query.get_last(limit=3)
    last3 = last3[1:4]  # remove header
    assert len(last3) is 3
    assert last3 == data[7:10]

    middle = query.get(limit=3, offset=3)
    middle = middle[1:4]  # remove header
    assert len(middle) is 3
    assert middle == data[3:6]


def test_show_nested_warning(canner_client: Client, caplog):
    nestedsql = """SELECT * FROM (
        VALUES (
            ARRAY[CAST(ROW(1, 2.0) AS ROW(x BIGINT, y DOUBLE)), CAST(ROW(2, 4.0) AS ROW(x BIGINT, y DOUBLE))],
            MAP(ARRAY['1', '2'], ARRAY[CAST(ROW(1, 2.0) AS ROW(x BIGINT, y DOUBLE)), CAST(ROW(2, 4.0) AS ROW(x BIGINT, y DOUBLE))]),
            CAST(ROW(1, CAST(ROW(1, 2.0) AS ROW(x BIGINT, y DOUBLE))) AS ROW(x BIGINT, y ROW(x BIGINT, y DOUBLE)))
        )
    ) AS nestedtable (array_of_row, map_of_row, row_of_row)"""

    query = canner_client.gen_query(nestedsql, data_format="df", fetch_by="storage")
    query.wait_for_finish(timeout=300)
    df = query.get_all()
    assert (
        len(caplog.messages) is 3
    ), f"Expect that got 3 warnings but {len(caplog.messages)}."
    assert caplog.messages[0].find(
        "array_of_row"
    ), "Didn't get the warning for array_of_row column."
    assert caplog.messages[1].find(
        "map_of_row"
    ), "Didn't get the warning for map_of_row column."
    assert caplog.messages[2].find(
        "row_of_row"
    ), "Didn't get the warning for row_of_row column."


@pytest.mark.parametrize(
    "input_sql_query,expected",
    [
        (
            "test",
            "line 1:1: mismatched input 'test'. Expecting:"
        ),
        (
            "slect * from tpch.tiny.lineitem limit 1",
            "line 1:1: mismatched input 'slect'. Expecting:"
        ),
        (
            "select from tpch.tiny.lineitem limit 1",
            "line 1:8: mismatched input 'from'. Expecting:",
        ),
        ("select * from tpch.tiny limit 1", "line 2:15: Schema 'tpch' does not exist"),
        ("select 0 from tpch.tiny limit 1", "line 2:15: Schema 'tpch' does not exist"),
        ("select *", "line 2:8: SELECT * not allowed in queries without FROM clause"),
        (
            "select -",
            "line 1:9: mismatched input '<EOF>'. Expecting:",
        ),
    ],
)
def test_should_throw_sql_failed_when_query_with_error_sql_syntax(
    canner_client: Client, input_sql_query: str, expected: str
):
    # Arrange
    try:
        # Act
        query=canner_client.gen_query(input_sql_query, cache_refresh=True)
        query.wait_for_finish(timeout=300)

        # Assert error message if not throw error but status is FAILED
        assert query.status == SqlQueryStatus.FAILED
        # The error message will change follow by SQL Engine cherry-pick commits from Trino, so we could only check part of error message
        assert expected in query.error['message']
    except Exception as error:
        # Assert exception message if getting the failed when calling gen_query
        # The error message will change follow by SQL Engine cherry-pick commits from Trino, so we could only check part of error message
        assert (expected in str(error.args[1])), f"should be throw error with message that contains  {expected} sub-content"



class TestQueryWithIterator(object):
    def test_should_count_correct_when_query_large_data_with_loop(
        self,
        canner_client: Client,
    ):
        expected = 37435
        sql_sql = f"select * from tpch.tiny.lineitem limit {expected}"
        query = canner_client.gen_query(sql_sql, cache_refresh=True)
        query.wait_for_finish(timeout=300)

        assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
        assert query.row_count > 0, "should have row_count"
        count = 0
        for row in query:
            assert len(row) == 2, "should format as [columns, data]"
            count += 1
        # Assert
        assert count == expected, f"should get {expected} lines"

    def test_should_count_correct_when_query_large_data_with_list_comprehension(
        self,
        canner_client: Client,
    ):
        expected = 37435
        sql_sql = f"select * from tpch.tiny.lineitem limit {expected}"
        query = canner_client.gen_query(sql_sql, cache_refresh=True)
        query.wait_for_finish(timeout=300)

        assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
        assert query.row_count > 0, "should have row_count"
        count = len([row for row in query])
        # Assert
        assert count == expected, f"should get {expected} lines"

    def test_should_count_correct_when_query_small_data_with_loop(
        self,
        canner_client: Client,
    ):
        expected = 100
        sql_sql = f"select * from tpch.tiny.lineitem limit {expected}"
        query = canner_client.gen_query(sql_sql, cache_refresh=True)
        query.wait_for_finish(timeout=300)

        assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
        assert query.row_count > 0, "should have row_count"
        count = 0
        for row in query:
            assert len(row) == 2, "should format as [columns, data]"
            count += 1
        # Assert
        assert count == expected, f"should get {expected} lines"

    def test_should_count_correct_when_query_small_data_with_list_comprehension(
        self,
        canner_client: Client,
    ):
        expected = 100
        sql_sql = f"select * from tpch.tiny.lineitem limit {expected}"
        query = canner_client.gen_query(sql_sql, cache_refresh=True)
        query.wait_for_finish(timeout=300)

        assert query.status == SqlQueryStatus.FINISHED, "status must be finished"
        assert query.row_count > 0, "should have row_count"
        count = len([row for row in query])
        # Assert
        assert count == expected, f"should get {expected} lines"

    def test_should_all_df_when_query_with_df_format(self, canner_client: Client):
        # Arrange
        sql_query = "select * from tpch.tiny.lineitem limit 100"
        query = canner_client.gen_query(
            sql_query,
            cache_refresh=True,
            data_format="df",
        )
        query.wait_for_finish(timeout=300)

        # Act
        is_all_dataframe = [isinstance(row, pd.DataFrame) for row in query]

        # Assert
        assert all(is_all_dataframe) == True, "should be format as data frame"
