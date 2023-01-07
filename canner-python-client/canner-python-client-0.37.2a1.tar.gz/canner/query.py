from typing import Any, Dict, Union, Optional

from pandas.core.frame import DataFrame
from canner.logging import *
from canner.utils import *
from canner.payloads import *
from canner.exceptions import handle_exception, CannerError, CannerErrorStatus
from canner.request import CannerRequest
from canner.dto import SqlQueryResult, SqlQueryStatus
from canner.adapters.query_reader import ParquetQueryReader, ApiFetchQueryReader


__all__ = ["Query"]


class Query(object):
    def __init__(
        self,
        request: CannerRequest,
        workspace_id: str,
        sql: str,
        cache_refresh: bool,
        cache_ttl: int,
        data_format: str,
        page_limit: int = 5000,
        fetch_by: str = "storage",
    ):
        self._workspace_id = workspace_id
        self._request = request
        self._sql = sql
        self._page_limit = page_limit
        self._fetch_by = fetch_by
        self._columns: Optional[Union[dict, list]] = None
        self.data_format = data_format

        sql_query = self.___create_sql_query(
            sql,
            workspace_id,
            cache_refresh,
            cache_ttl,
        )
        self.__update_query_info(sql_query)

    @property
    def id(self) -> str:
        return self._id

    @property
    def row_count(self) -> int:
        """
        row count will shows the correct value until `status` is `FINISHED`.
        If `status` not be `FINISHED`, the row count return `-1`.
        """
        return -1 if self._status != SqlQueryStatus.FINISHED else self._row_count

    @property
    def status(self) -> SqlQueryStatus:
        return self._status

    @property
    def statement_id(self) -> Optional[str]:
        return self._statement_id

    @property
    def columns(self) -> Union[list, dict, None]:
        return self._columns

    @property
    def error(self) -> Dict[str, any]:
        return self._error

    def __ensure_query_finished(self):
        if self._status != SqlQueryStatus.FINISHED:
            self.wait_for_finish()

    def __update_query_info(self, sql_query: SqlQueryResult):
        self._id = sql_query.id
        self._status = SqlQueryStatus(sql_query.status)
        self._error = sql_query.error
        self._row_count = sql_query.row_count
        self._columns = sql_query.columns
        self._statement_id = sql_query.statementId

    def __iter__(self):
        row, offest, page = 0, 0, 1
        # ensure query status finished
        self.__ensure_query_finished()
        # prepare storage urls by creating parquet reader and
        parquet_reader = ParquetQueryReader(self._id, self._workspace_id, self._request)
        # fetch data of first page
        page_result = parquet_reader.read(self._page_limit, offest)

        while (page - 1) * self._page_limit + row < self._row_count:
            if row == len(page_result.data):
                offest = self._page_limit * page
                # fetch data of next page and reset index row = 0
                page_result = parquet_reader.read(self._page_limit, offest)
                row, page = 0, page + 1
            elif row < len(page_result.data):
                formatted_data = self.__transfer_format(
                    self.columns, [page_result.data[row]], self.data_format
                )
                yield formatted_data
                row += 1
            else:
                break

    @handle_exception
    def ___create_sql_query(
        self, sql: str, workspace_id: str, cache_refresh: bool, cache_ttl: int
    ) -> SqlQueryResult:
        payload = CreateSqlQueryPayload().build(
            sql,
            workspace_id,
            cache_refresh,
            cache_ttl,
        )
        resp = self._request.graphql_exec(payload)
        result = resp.get("createSqlQuery")
        result = SqlQueryResult(**result)
        if SqlQueryStatus(result.status) == SqlQueryStatus.FAILED:
            raise CannerError(
                CannerErrorStatus.SQL_SYNTAX_FAILED.name,
                result.error["message"],
            )
        return result

    @handle_exception
    def __get_sql_query(self) -> SqlQueryResult:
        response = self._request.graphql_exec(SqlQueryPayload().build(self._id))
        result = response.get("sqlQuery")
        return SqlQueryResult(**result)

    @handle_exception
    def delete_statement(self):
        if self._statement_id is None:
            return
        self._request.graphql_exec(DeleteStatementPayload().build(self._statement_id))
        # update query information
        sql_query = self.__get_sql_query()
        self.__update_query_info(sql_query)

    @handle_exception
    def get_sql_result(self, limit, offset) -> Union[Any, list]:
        if self._fetch_by == "storage":
            return self.__read_sql_result_by_storage(limit, offset)
        else:
            return self.__read_sql_result_by_restful(limit, offset)

    def __read_sql_result_by_storage(self, limit, offset) -> list:
        parquet_reader = ParquetQueryReader(self._id, self._workspace_id, self._request)
        output = parquet_reader.read(limit, offset)
        # Fetch metadata again for getting correct row count after query finished
        sql_query = self.__get_sql_query()
        self.__update_query_info(sql_query)
        # if parquet column has value, then used parquet format columns field, otherwise keep original column field (because no data, so keep original column field information)
        if output.columns:
            self._columns = output.columns
        return output.data

    def __read_sql_result_by_restful(self, limit, offset):
        output_data = []
        api_fetch_reader = ApiFetchQueryReader(
            self._id, self._page_limit, self._request
        )
        output_data = api_fetch_reader.read(limit, offset)
        # Fetch metadata again for getting correct row count after query finished
        sql_query = self.__get_sql_query()
        self.__update_query_info(sql_query)
        return output_data

    @handle_exception
    def wait_for_finish(self, timeout=120, period=1):
        def check_status_and_update_info():
            if self._status not in [SqlQueryStatus.FINISHED, SqlQueryStatus.FAILED]:
                sql_query = self.__get_sql_query()
                self.__update_query_info(sql_query)
                return False
            return True

        wait_until(check_status_and_update_info, timeout, period)

    @handle_exception
    def __transfer_format(
        self, columns: Union[list, Any, None], data: Union[list, Any], format: str
    ) -> Union[Any, list, DataFrame]:
        try:
            return data_factory(data_format=format, columns=columns, data=data)
        except Exception:
            raise CannerError(
                CannerErrorStatus.DATA_INCORRECT.name,
                CannerErrorStatus.DATA_INCORRECT.value,
            )

    @handle_exception
    def get_all(self):
        # ensure query finished and could get full row count
        self.__ensure_query_finished()
        query_data = self.get_sql_result(self._row_count, 0)
        return self.__transfer_format(self.columns, query_data, self.data_format)

    @handle_exception
    def get_first(self, limit=1):
        query_data = self.get_sql_result(limit, 0)
        return self.__transfer_format(self.columns, query_data, self.data_format)

    @handle_exception
    def get_last(self, limit=1):
        # ensure query finished and could get full row count
        self.__ensure_query_finished()
        offset = self._row_count - limit
        query_data = self.get_sql_result(limit, offset)
        return self.__transfer_format(self.columns, query_data, self.data_format)

    @handle_exception
    def get(self, limit, offset):
        query_data = self.get_sql_result(limit, offset)
        return self.__transfer_format(self.columns, query_data, self.data_format)
