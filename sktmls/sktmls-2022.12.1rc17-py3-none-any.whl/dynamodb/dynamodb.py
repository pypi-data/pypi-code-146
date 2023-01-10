import gzip
import json
from time import time
from typing import Dict, Any

import boto3
import simplejson
from boto3.dynamodb.types import Binary

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError

MLS_DYNAMODB_API_URL = "/api/v1/dynamodb"

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")


class DynamoDBClient(MLSClient):
    """
    DynamoDB 관련 기능들을 제공하는 클라이언트입니다.
    """

    def __init__(
        self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None, username: str = None, password: str = None
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.dynamodb.DynamoDBClient`

        ## Example

        ```python
        dynamodb_client = DynamoDBClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def get_item(self, table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
        """
        주어진 Dynamodb 테이블의 특정 아이템을 조회합니다

        ## Args

        - table_name: (str) 테이블 명
        - key: (dict) 조회할 아이템의 key 값

        ## Returns

        (dict) 해당 아이템 값

        ## Example

        ```python
        item = dynamodb_client.get_item(table_name="sample_table", key={"item_id": "sample"})
        ```
        """
        if self._MLSClient__runtime_env == MLSRuntimeENV.MMS:
            table = dynamodb.Table(table_name)
            response = table.get_item(Key=key)
            item = response.get("Item")
            if not item:
                raise MLSClientError(code=404, msg="아이템이 존재하지 않습니다.")
            if (
                (table_name.startswith("user-profile") or table_name.startswith("profile-"))
                and not table_name.endswith("nogzip")
                and "values" in item
            ):
                values = json.loads(gzip.decompress(item["values"].value).decode())
                partition_key = "user_id" if table_name.startswith("user-profile") else "id"
                item = {partition_key: item[partition_key], **values}
            return {"item": json.loads(simplejson.dumps(item, use_decimal=True))}

        return self._request(
            method="POST", url=MLS_DYNAMODB_API_URL, data={"type": "get", "table_name": table_name, "body": key}
        ).results

    def put_item(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        주어진 Dynamodb 테이블에 특정 아이템을 추가합니다

        ## Args

        - table_name: (str) 테이블 명
        - item: (dict) 추가할 아이템 값

        ## Returns

        (dict) 추가한 아이템 값

        ## Example
        ```python
        dynamodb_client.put_item(
            table_name="sample_table",
            item={"item_id": "sample", "sample_attribute": "sample_value"}
        )
        ```
        """
        if self._MLSClient__runtime_env == MLSRuntimeENV.MMS:
            table = dynamodb.Table(table_name)

            try:
                gzipped = False
                if (
                    table_name.startswith("user-profile") or table_name.startswith("profile-")
                ) and not table_name.endswith("nogzip"):
                    gzipped = True
                    partition_key = "user_id" if table_name.startswith("user-profile") else "id"
                    compressed = gzip.compress(simplejson.dumps(item, use_decimal=True).encode())
                    item = {partition_key: item[partition_key], "values": Binary(compressed)}

                if table_name.startswith("user-profile") or table_name.startswith("profile-"):
                    item["ttl"] = int(time() + 90 * 24 * 60 * 60)
                else:
                    item["ttl"] = int(time() + 30 * 24 * 60 * 60)
                if gzipped:
                    response = table.put_item(Item=item)
                else:
                    response = table.put_item(Item=simplejson.loads(json.dumps(item), use_decimal=True))

                return response["ResponseMetadata"]
            except Exception:
                raise MLSClientError(code=404, msg="테이블이 존재하지 않습니다.")

        return self._request(
            method="POST", url=MLS_DYNAMODB_API_URL, data={"type": "put", "table_name": table_name, "body": item}
        ).results

    def update_item(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        주어진 Dynamodb 테이블의 특정 아이템을 수정합니다

        ## Args

        - table_name: (str) 테이블 명
        - item: (dict) 수정할 아이템 값

        ## Returns

        (dict) 수정한 아이템 값

        ## Example

        ```python
        dynamodb_client.update_item(
            table_name="sample_table",
            item={"item_id": "sample", "sample_attribute": "sample_value_updated", "add_new_field": "added_field_value"}
        )
        ```
        """
        if self._MLSClient__runtime_env == MLSRuntimeENV.MMS:
            if "id" in item:
                partition_key = "id"
            elif "user_id" in item:
                partition_key = "user_id"
            else:
                partition_key = "item_id"
            updated_item = self.get_item(table_name, {partition_key: item[partition_key]})["item"]
            updated_item.update(item)
            return self.put_item(table_name, updated_item)

        return self._request(
            method="POST", url=MLS_DYNAMODB_API_URL, data={"type": "update", "table_name": table_name, "body": item}
        ).results

    def delete_item(self, table_name: str, key: Dict[str, Any]) -> MLSResponse:
        """
        주어진 Dynamodb 테이블의 특정 아이템을 삭제합니다

        ## Args

        - table_name: (str) 테이블 명
        - key: (dict) 삭제할 아이템의 key 값

        ## Returns

        `sktmls.MLSResponse`

        ## Example

        ```python
        dynamodb_client.delete_item(
            table_name="sample_table",
            item={"item_id": "sample"}
        )
        ```
        """
        return self._request(
            method="POST", url=MLS_DYNAMODB_API_URL, data={"type": "delete", "table_name": table_name, "body": key}
        )
