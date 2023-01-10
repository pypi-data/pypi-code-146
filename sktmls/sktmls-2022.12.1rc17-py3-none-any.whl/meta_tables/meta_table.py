from typing import Dict, Any, List

import pandas
from dateutil import parser

from sktmls import MLSClient, MLSRuntimeENV, MLSENV, MLSResponse, MLSClientError

MLS_META_API_URL = "/api/v1/meta_tables"


class MetaTable:
    """
    MLS 메타 테이블 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 메타 테이블 고유 ID
            - name: (str) 메타 테이블 이름
            - description: (str) 메타 테이블 설명
            - schema: (dict) 메타 아이템 스키마
            - items: (list) 포함된 메타 아이템 리스트
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시
            - user: (str) 메타 테이블 소유 계정명

        ## Returns
        `sktmls.meta_tables.MetaTable`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.schema = kwargs.get("schema")
        self.items = kwargs.get("items")
        self.created_at = parser.parse(kwargs.get("created_at"))
        self.updated_at = parser.parse(kwargs.get("updated_at"))
        self.user = kwargs.get("user")

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MetaItem:
    """
    MLS 메타 아이템 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 메타 아이템 고유 ID
            - name: (str) 메타 아이템 이름
            - values: (dict) 메타 아이템 정보

        ## Returns
        `sktmls.meta_tables.MetaItem`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.values = kwargs.get("values")

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MetaTableClient(MLSClient):
    """
    MLS 메타 테이블과 메타 아이템 관련 기능들을 제공하는 클라이언트입니다.
    """

    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        username: str = None,
        password: str = None,
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        아래의 환경 변수가 정의된 경우 해당 파라미터를 생략 가능합니다.

        - $MLS_ENV: env
        - $MLS_RUNTIME_ENV: runtime_env
        - $MLS_USERNAME: username
        - $MLS_PASSWORD: password

        ## Returns
        `sktmls.meta_tables.MetaTableClient`

        ## Example

        ```python
        meta_table_client = MetaTableClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """

        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_meta_table(self, name: str, schema: Dict[str, Dict], description: str = None) -> MetaTable:
        """
        메타 테이블을 생성합니다.

        ## Args

        - name: (str) 메타 테이블 이름
        - schema: (dict) 메타 아이템 스키마
        - description: (optional) (str) 메타 테이블 설명

        ## Returns
        `sktmls.meta_tables.MetaTable`

        - id: (int) 생성된 메타 테이블 고유 ID
        - name: (str) 생성된 메타 테이블 이름
        - description: (str) 생성된 메타 테이블 설명
        - schema: (dict) 생성된 메타 아이템 스키마
        - items: (list) 포함된 메타 아이템 리스트
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시
        - user: (str) 메타 테이블 소유 계정명

        ## Example

        ```python
        meta_table = meta_table_client.create_meta_table(
            name="my_meta_table",
            schema={
                "meta_item_schema1": {"type": "string"},
                "meta_item_schema2": {"type": "number"}
            },
            description="This is my table"
        )
        ```
        """

        data = {
            "name": name,
            "schema": schema,
        }
        if description:
            data["description"] = description

        return MetaTable(**self._request(method="POST", url=MLS_META_API_URL, data=data).results)

    def update_meta_table(
        self, meta_table: MetaTable, name: str = None, schema: Dict[str, Dict] = None, description: str = None
    ) -> MetaTable:
        """
        메타 테이블 정보를 수정합니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 테이블 객체
        - name: (optional) (str) 메타 테이블 이름
        - schema: (optional) (dict) 메타 아이템 스키마
        - description: (optional) (str) 메타 테이블 설명

        ## Returns
        `sktmls.meta_tables.MetaTable`

        - id: (int) 수정된 메타 테이블 고유 ID
        - name: (str) 수정된 메타 테이블 이름
        - description: (str) 수정된 메타 테이블 설명
        - schema: (dict) 수정된 메타 아이템 스키마
        - items: (list) 포함된 메타 아이템 리스트
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시
        - user: (str) 메타 테이블 소유 계정명

        ## Example

        ```python
        meta_table = meta_table_client.update_meta_table(
            meta_table=meta_table,
            name="my_meta_table",
            schema={
                "meta_item_schema3": {"type": "string"},
                "meta_item_schema4": {"type": "number"}
            },
            description="This is my updated table"
        )
        ```
        """
        assert type(meta_table) == MetaTable

        data = {"name": meta_table.name, "schema": meta_table.schema}
        if meta_table.description is not None:
            data["description"] = meta_table.description

        if name:
            data["name"] = name
        if schema:
            data["schema"] = schema
        if description is not None:
            data["description"] = description

        meta_table.reset(**self._request(method="PUT", url=f"{MLS_META_API_URL}/{meta_table.id}", data=data).results)

        return meta_table

    def get_meta_table(self, id: int = None, name: str = None) -> MetaTable:
        """
        메타 테이블 정보를 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (optional) (int) 메타 테이블 고유 ID
        - name: (optional) (str) 메타 테이블 이름

        ## Returns
        `sktmls.meta_tables.MetaTable`

        - id: (int) 메타 테이블 고유 ID
        - name: (str) 메타 테이블 이름
        - description: (str) 메타 테이블 설명
        - schema: (dict) 메타 아이템 스키마
        - items: (list) 포함된 메타 아이템 리스트
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시
        - user: (str) 메타 테이블 소유 계정명

        ## Example

        ```python
        meta_table_by_id = meta_table_client.get_meta_table(id=3)
        meta_table_by_name = meta_table_client.get_meta_table(name="my_table")
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        meta_tables = self.list_meta_tables(id=id, name=name)
        if len(meta_tables) == 0:
            raise MLSClientError(code=404, msg="메타 테이블이 없습니다.")
        elif len(meta_tables) > 1:
            raise MLSClientError(code=409, msg="메타 테이블이 여러개 존재합니다.")
        return meta_tables[0]

    def get_meta_table_dataframe(self, id: int = None, name: str = None) -> pandas.core.frame.DataFrame:
        """
        메타 테이블 정보를 가져와서 `pandas.core.frame.DataFrame` 형태로 반환합니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (optional) (int) 메타 테이블 고유 ID
        - name: (optional) (str) 메타 테이블 이름

        ## Returns
        `pandas.core.frame.DataFrame`

        ## Example

        ```python
        meta_table_df_by_id = meta_table_client.get_meta_table_dataframe(id=3)
        meta_table_df_by_name = meta_table_client.get_meta_table_dataframe(name="my_table")
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        results = self.get_meta_table(id=id, name=name).get()
        items = results.get("items")

        if items:
            key = pandas.DataFrame.from_records(items)["name"]
            values = pandas.DataFrame.from_records(pandas.DataFrame.from_records(items)["values"])

            return pandas.concat([key, values], axis=1)

    def list_meta_tables(self, **kwargs) -> List[MetaTable]:
        """
        메타 테이블 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 메타 테이블 고유 ID
            - name: (str) 메타 테이블 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.meta_tables.MetaTable`)

        - id: (int) 메타 테이블 고유 ID
        - name: (str) 메타 테이블 이름
        - description: (str) 메타 테이블 설명
        - schema: (dict) 메타 아이템 스키마
        - items: (list) 포함된 메타 아이템 리스트
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시
        - user: (str) 메타 테이블 소유 계정명

        ## Example

        ```python
        all_my_meta_tables = meta_table_client.list_meta_tables()
        ```
        """

        response = self._request(method="GET", url=f"{MLS_META_API_URL}", params=kwargs).results

        return [MetaTable(**meta_table) for meta_table in response]

    def meta_table_exists(self, id: int = None, name: str = None) -> bool:
        """
        메타 테이블이 존재하는 지 확인합니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (optional) (int) 메타 테이블 고유 ID
        - name: (optional) (str) 메타 테이블 이름

        ## Returns
        `bool`

        ## Example

        ```python
        meta_table_client.meta_table_exists(name="my_table")
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        meta_tables = self.list_meta_tables(id=id, name=name)
        if len(meta_tables) == 0:
            return False
        return True

    def delete_meta_table(self, meta_table: MetaTable) -> MLSResponse:
        """
        메타 테이블을 삭제합니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 테이블 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        meta_table_client.delete_meta_table(meta_table)
        ```
        """
        assert type(meta_table) == MetaTable

        return self._request(method="DELETE", url=f"{MLS_META_API_URL}/{meta_table.id}")

    def create_meta_item(self, meta_table: MetaTable, item_name: str, item_dict: Dict[str, Any]) -> MetaItem:
        """
        메타 아이템을 생성합니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 아이템이 포함될 메타 테이블 객체
        - item_name: (str) 메타 아이템 이름
        - item_dict: (dict) 메타 아이템 정보

        ## Returns
        `sktmls.meta_tables.MetaItem`

        - id: (int) 메타 아이템 고유 ID
        - name: (str) 메타 아이템 이름
        - values: (dict) 메타 아이템 정보

        ## Example

        ```python
        my_meta_item1 = meta_table_client.create_meta_item(
            meta_table=my_meta_table,
            item_name="my_meta_item1",
            item_dict={
                "meta_item_schema1": "string_value",
                "meta_item_schema2": 100
            }
        )
        ```
        """
        assert type(meta_table) == MetaTable

        data = {"name": item_name, "values": item_dict}

        return MetaItem(
            **self._request(method="POST", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items", data=data).results
        )

    def update_meta_item(
        self,
        meta_table: MetaTable,
        meta_item: MetaItem,
        item_name: str = None,
        item_dict: Dict[str, Any] = None,
    ) -> MetaItem:
        """
        메타 아이템을 수정합니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 테이블 객체
        - meta_item: (`sktmls.meta_tables.MetaItem`) 메타 아이템 객체
        - item_name: (optional) (str) 메타 아이템 이름
        - item_dict: (optional) (dict) 메타 아이템 정보

        ## Returns:
        `sktmls.meta_tables.MetaItem`

        - id: (int) 메타 아이템 고유 ID
        - name: (str) 메타 아이템 이름
        - values: (dict) 메타 아이템 정보

        ## Example

        ```python
        my_meta_item1 = meta_table_client.update_meta_item(
            meta_table=my_meta_table,
            meta_item=my_meta_item1,
            item_name="my_meta_item1",
            item_dict={
                "meta_item_schema1": "another_string_value",
                "meta_item_schema2": 200
            }
        )
        ```
        """
        assert type(meta_table) == MetaTable
        assert type(meta_item) == MetaItem

        data = meta_item.get()
        if item_name:
            data["name"] = item_name
        if item_dict:
            data["values"] = item_dict

        meta_item.reset(
            **self._request(
                method="PUT", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items/{meta_item.id}", data=data
            ).results
        )

        return meta_item

    def list_meta_items(self, meta_table: MetaTable, **kwargs) -> List[MetaItem]:
        """
        메타 테이블에 포함된 메타 아이템 리스트를 가져옵니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 테이블 객체
        - kwargs: (optional) (dict) 쿼리 조건
          - id: (int) 메타 아이템 고유 ID
          - name: (str) 메타 아이템 이름
          - query: (str) 검색 문자
          - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.meta_tables.MetaItem`)

        - id: (int) 메타 아이템 고유 ID
        - name: (str) 메타 아이템 이름
        - values: (dict) 메타 아이템 정보

        ## Example

        ```python
        all_meta_items_in_table = meta_table_client.list_meta_items(meta_table=my_meta_table)
        ```
        """
        assert type(meta_table) == MetaTable

        response = self._request(
            method="GET", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items", params=kwargs
        ).results

        return [MetaItem(**meta_item) for meta_item in response]

    def get_meta_item(self, meta_table: MetaTable, id: int = None, name: str = None) -> MetaItem:
        """
        메타 아이템 정보를 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 테이블 객체
        - id: (optional) (int) 메타 아이템 고유 ID
        - name: (optional) (str) 메타 아이템 이름

        ## Returns
        `sktmls.meta_tables.MetaItem`

        - id: (int) 메타 아이템 고유 ID
        - name: (str) 메타 아이템 이름
        - values: (dict) 메타 아이템 정보

        ## Example

        ```python
        meta_item_by_id = meta_table_client.get_meta_item(meta_table=my_meta_table, id=10)
        meta_item_by_name = meta_table_client.get_meta_item(meta_table=my_meta_table, name="my_item")
        ```
        """
        assert type(meta_table) == MetaTable
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        meta_items = self.list_meta_items(meta_table, id=id, name=name)
        if len(meta_items) == 0:
            raise MLSClientError(code=404, msg="메타 아이템이 없습니다.")
        elif len(meta_items) > 1:
            raise MLSClientError(code=409, msg="메타 아이템이 여러개 존재합니다.")
        return meta_items[0]

    def delete_meta_item(self, meta_table: MetaTable, meta_item: MetaItem) -> MLSResponse:
        """
        메타 아이템을 메타 테이블에서 삭제합니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 테이블 객체
        - meta_item: (`sktmls.meta_tables.MetaItem`) 메타 아이템 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        meta_table_client.delete_meta_item(meta_table=my_meta_table, meta_item=my_meta_item)
        ```
        """
        assert type(meta_table) == MetaTable
        assert type(meta_item) == MetaItem

        return self._request(method="DELETE", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items/{meta_item.id}")

    def create_meta_items(self, meta_table: MetaTable, items_dict: Dict[str, Any]) -> List[MetaItem]:
        """
        메타 아이템 여러 개를 생성/수정 합니다. 추가 할 `item_name`이 존재 시 수정, 미존재 시 생성 합니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 아이템이 포함될 메타 테이블 객체
        - items_dict: (dict) Bulk로 추가할 메타 아이템 정보

        ## Returns
        list(`sktmls.meta_tables.MetaItem`)

        - id: (int) 메타 아이템 고유 ID
        - name: (str) 메타 아이템 이름
        - values: (dict) 메타 아이템 정보

        ## Example

        ```python
        my_meta_item1 = meta_table_client.create_meta_items(
            meta_table=my_meta_table,
            items_dict={
                "item_1" : {
                    "value_1" : "a1", "value_2" : "b1"
                },
                "item_2" : {
                    "value_1" : "a2", "value_2" : "b2"
                },
                "item_3" : {
                    "value_1" : "a3", "value_2" : "b3"
                }
            }
        )
        ```
        """
        assert type(meta_table) == MetaTable
        assert len(items_dict) <= 1000, "Bulk로 추가할 meta_items은 한번에 최대 1,000건 까지 지원합니다."

        data = {"items": items_dict}

        response = self._request(method="POST", url=f"{MLS_META_API_URL}/{meta_table.id}/bulk", data=data).results
        return [MetaItem(**meta_item) for meta_item in response]

    def create_meta_items_by_dataframe(
        self, meta_table: MetaTable, meta_items: pandas.core.frame.DataFrame, item_name: str
    ) -> List[MetaItem]:
        """
        메타 아이템 여러 개를 Pandas DataFrame을 이용하여 생성/수정 합니다. 추가 할 `item_name`이 존재 시 수정, 미존재 시 생성 합니다.

        ## Args

        - meta_table: (`sktmls.meta_tables.MetaTable`) 메타 아이템이 포함될 메타 테이블 객체
        - meta_items: (`pandas.core.frame.DataFrame`) Bulk로 추가할 메타 아이템 Pandas DataFrame
        - item_name: (str) meta_items 컬럼 중 meta_item의 이름이 될 컬럼명

        ## Returns
        list(`sktmls.meta_tables.MetaItem`)

        - id: (int) 메타 아이템 고유 ID
        - name: (str) 메타 아이템 이름
        - values: (dict) 메타 아이템 정보

        ## Example

        ```python
        my_meta_table = meta_table_client.get_meta_table(name="my_meta_table")

        meta_items = pandas.DataFrame({"name": ["item_1", "item_2", "item_3"], "value_1": ["a1", "a2", "a3"], "value_2": ["b1", "b2", "b3"]})

        my_meta_items = meta_table_client.create_meta_items_by_dataframe(
            meta_table=my_meta_table,
            meta_items=meta_items,
            item_name="name"
        )
        ```
        """
        assert type(meta_table) == MetaTable
        assert type(meta_items) == pandas.core.frame.DataFrame
        assert meta_items.shape[0] <= 1000, "Bulk로 추가할 meta_items은 한번에 최대 1,000건 까지 지원합니다."

        meta_items.set_index([item_name], drop=True, inplace=True)
        items_dict = meta_items.to_dict(orient="index")

        data = {"items": items_dict}

        response = self._request(method="POST", url=f"{MLS_META_API_URL}/{meta_table.id}/bulk", data=data).results
        return [MetaItem(**meta_item) for meta_item in response]
