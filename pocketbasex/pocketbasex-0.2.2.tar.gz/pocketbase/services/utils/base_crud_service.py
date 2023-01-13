from __future__ import annotations

from abc import ABC
from urllib.parse import quote

from pocketbase.models.utils.base_model import BaseModel
from pocketbase.models.utils.list_result import ListResult
from pocketbase.services.utils.base_service import BaseService


class BaseCrudService(BaseService, ABC):
    def decode(self, data: dict) -> BaseModel:
        """Response data decoder"""

    def _get_full_list(
        self, 
        base_path: str,
        batch: int = 200, 
        expand: str = None,
        filter: str = None,
        sort: str = None,
        query: dict = None,
        headers: dict = None,
    ) -> list[BaseModel]:
        result: list[BaseModel] = []

        def request(result: list[BaseModel], page: int) -> list:
            list = self._get_list(
                base_path,
                page=page,
                per_page=batch,
                expand=expand,
                filter=filter,
                sort=sort,
                query=query,
                headers=headers,
            )
            items = list.items
            total_items = list.total_items
            result += items
            if len(items) > 0 and total_items > len(result):
                return request(result, page + 1)
            return result

        return request(result, 1)

    # https://github.com/pocketbase/dart-sdk/blob/cb04918f918de8b5815212bb1a52941fc6fe0e10/lib/src/services/base_crud_service.dart#L56
    def _get_list(
        self,
        base_path: str,
        *,
        page: int = 1, 
        per_page: int = 30,
        expand: str = None,
        filter: str = None,
        sort: str = None,
        query: dict = None,
        headers: dict = None,
    ) -> ListResult:
        query = query or {}
        headers = headers or {}
        enriched_query = query.copy()
        enriched_query.update({"page": page, "perPage": per_page, "expand": expand, "filter": filter, "sort": sort})
        response_data = self.client.send(
            base_path, {"method": "GET", "params": enriched_query, "headers": headers}
        )
        items: list[BaseModel] = []
        if "items" in response_data:
            response_data["items"] = response_data["items"] or []
            for item in response_data["items"]:
                items.append(self.decode(item))
        return ListResult(
            response_data.get("page", 1),
            response_data.get("perPage", 0),
            response_data.get("totalItems", 0),
            response_data.get("totalPages", 0),
            items,
        )

    def _get_one(self, base_path: str, id: str, query_params: dict = {}) -> BaseModel:
        return self.decode(
            self.client.send(
                f"{base_path}/{quote(id)}", {"method": "GET", "params": query_params}
            )
        )

    def _create(
        self, base_path: str, body_params: dict = {}, query_params: dict = {}
    ) -> BaseModel:
        return self.decode(
            self.client.send(
                base_path,
                {"method": "POST", "params": query_params, "body": body_params},
            )
        )

    def _update(
        self, base_path: str, id: str, body_params: dict = {}, query_params: dict = {}
    ) -> BaseModel:
        return self.decode(
            self.client.send(
                f"{base_path}/{quote(id)}",
                {"method": "PATCH", "params": query_params, "body": body_params},
            )
        )

    def _delete(self, base_path: str, id: str, query_params: dict = {}) -> bool:
        self.client.send(
            f"{base_path}/{quote(id)}", {"method": "DELETE", "params": query_params}
        )
        return True
