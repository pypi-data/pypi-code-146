import time
from canner.request import CannerRequest
from canner.payloads import SqlResultPaginationPayload


class ApiFetchQueryReader(object):
    def __init__(self, query_id: str, page_limit: int, request: CannerRequest) -> None:
        self._query_id = query_id
        self._page_limit = page_limit
        self._request = request
        self._payload = SqlResultPaginationPayload()

    def read(self, limit: int, offset: int) -> list:
        # If the source limit largest fetch
        output_data = []

        if limit > self._page_limit:
            page_number = 0
            while page_number * self._page_limit < limit:
                page_offest = page_number * self._page_limit
                response = self._request.graphql_exec(
                    self._payload.build(self._query_id, self._page_limit, page_offest)
                )
                result = response.get("sqlResultPagination")
                output_data.extend(result["result"])
                page_number += 1
                # sleep to prevent server refused connection as retry too many times
                time.sleep(1)
        else:
            response = self._request.graphql_exec(
                self._payload.build(self._query_id, limit, offset)
            )
            result = response.get("sqlResultPagination")
            output_data = result["result"]
        return output_data