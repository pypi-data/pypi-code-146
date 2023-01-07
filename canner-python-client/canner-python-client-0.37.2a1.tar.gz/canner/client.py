# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import csv
from io import StringIO
from typing import Optional
import pandas as pd
import canner.workspace
import canner.exceptions
import canner.utils
import nest_asyncio

nest_asyncio.apply()

__all__ = ["bootstrap", "Client"]


def bootstrap(*args, **kwargs):
    return Client(*args, **kwargs)


class Client(object):
    def __init__(
        self,
        endpoint: str,
        workspace_id: str,
        replaceLocalhostString: Optional[str] = None,
        headers: Optional[dict] = None,
        token: Optional[str] = None,
    ):
        endpoint = endpoint.rstrip("/")
        if token != None:
            if not headers:
                headers = {"Authorization": f"Token {token}"}
            else:
                headers["Authorization"] = f"Token {token}"
        # Create workspace
        self.workspace = canner.workspace.Workspace(
            endpoint=endpoint,
            headers=headers,
            workspace_id=workspace_id,
            replaceLocalhostString=replaceLocalhostString,
        )

    # SQL
    def use_saved_query(
        self, title, cache_refresh=False, cache_ttl=86400, data_format="list"
    ):
        query = self.workspace.saved_query.get(title)
        return self.gen_query(
            sql=query["sql"],
            cache_refresh=cache_refresh,
            cache_ttl=cache_ttl,
            data_format=data_format,
        )

    def list_saved_query(self):
        return self.workspace.saved_query.list_title()

    def gen_query(
        self,
        sql,
        cache_refresh=False,
        cache_ttl=86400,
        data_format="list",
        fetch_by="storage",
    ):
        # "cache_refresh" is true means not cached data.
        query = self.workspace.gen_query(
            sql,
            cache_refresh=cache_refresh,
            cache_ttl=cache_ttl,
            data_format=data_format,
            fetch_by=fetch_by,
        )
        return query

    # files
    def list_file(self, recursive: bool = True):
        """
        Args:
            recursive (bool): recursive list sub folder files
        """
        return self.workspace.file.list_absolute_path(recursive)

    def delete_file(self, absolute_path):
        return self.workspace.file.delete(absolute_path)

    def get_binary(self, absolute_path):
        return self.workspace.file.get_content(absolute_path)

    def put_binary(self, absolute_path, data):
        return self.workspace.file.put(absolute_path, data)

    # wrappers
    def _get_csv_wrapper(self, absolute_path, encoding="utf-8"):
        return self.workspace.file.get_csv_wrapper(absolute_path, encoding=encoding)

    def _get_json_wrapper(self, absolute_path, encoding="utf-8"):
        return self.workspace.file.get_json_wrapper(absolute_path, encoding=encoding)

    def _get_image_wrapper(self, absolute_path):
        return self.workspace.file.get_image_wrapper(absolute_path)

    # csv
    def get_csv(self, absolute_path, encoding="utf-8"):
        return self._get_csv_wrapper(absolute_path, encoding).to_list()

    def get_pandas_csv(self, absolute_path, encoding="utf-8", *args, **kwargs):
        return self._get_csv_wrapper(absolute_path, encoding).to_pandas(*args, **kwargs)

    def put_csv(self, absolute_path, data, encoding="utf-8", *args, **kwargs):
        if isinstance(data, pd.DataFrame):
            return self.put_pandas_csv(absolute_path, data, encoding, *args, **kwargs)
        return self.put_csv_str(absolute_path, data, encoding, *args, **kwargs)

    def put_csv_str(self, absolute_path, data, encoding="utf-8", *args, **kwargs):
        str_io = StringIO()
        csv_writer = csv.writer(str_io, *args, **kwargs)
        csv_writer.writerows(data)
        value = str_io.getvalue().encode(encoding)
        return self.put_binary(absolute_path=absolute_path, data=value)

    def put_pandas_csv(self, absolute_path, data, encoding="utf-8"):
        data = data.to_csv(index=False).encode(encoding)
        return self.put_binary(absolute_path=absolute_path, data=data)

    # json
    def get_json(self, absolute_path, encoding="utf-8"):
        return self._get_json_wrapper(absolute_path, encoding).to_json()

    def get_pandas_json(self, absolute_path, encoding="utf-8", *args, **kwargs):
        return self._get_json_wrapper(absolute_path, encoding).to_pandas(
            *args, **kwargs
        )

    def put_json(self, absolute_path, data, encoding="utf-8"):
        if isinstance(data, pd.DataFrame):
            return self.put_pandas_json(absolute_path, data, encoding)
        else:
            return self.put_json_str(absolute_path, data, encoding)

    def put_json_str(self, absolute_path, data, encoding="utf-8"):
        data = json.dumps(data).encode(encoding)
        return self.put_binary(absolute_path=absolute_path, data=data)

    def put_pandas_json(self, absolute_path, data, encoding="utf-8"):
        data = data.to_json()
        self.put_json_str(absolute_path=absolute_path, data=data, encoding=encoding)

    # image
    def get_pil_image(self, absolute_path):
        return self._get_image_wrapper(absolute_path).to_pil()

    def get_np_image(self, absolute_path):
        return self._get_image_wrapper(absolute_path).to_np()
