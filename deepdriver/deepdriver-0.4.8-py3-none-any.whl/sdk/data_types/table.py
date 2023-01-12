import hashlib
import json
import os
from pathlib import Path

from assertpy import assert_that
from typing import Dict, Tuple, TYPE_CHECKING
from deepdriver import logger
from deepdriver.sdk.data_types.dataFrame import DataFrame
from deepdriver.sdk.data_types.media import LOG_TYPE_TABLE, Media
from deepdriver.sdk.data_types.run import Run
from deepdriver.sdk.interface import interface


class Table(Media):

    def __init__(self, data: DataFrame) -> None:
        super().__init__(log_type=LOG_TYPE_TABLE)

        assert_that(data).is_not_none()
        self.data = data

    @classmethod
    def from_file(cls, path: str):
        assert_that(str).is_not_none()
        with open(path) as f:
            data = json.load(f)
        return cls(data=DataFrame(columns=data['data']['columns'], data=data['data']['data']))

    def __str__(self):
        return self.data.dataframe.__str__()

    def __repr__(self):
        # return "1"
        return self.data.dataframe.__repr__()

    def _repr_html_(self):
        # return "1"
        return self.data.dataframe._repr_html_()

    def to_dict(self):
        return {
            "data": self.data.to_dict(),
        }

    def to_json(self, key_name: str) -> str:
        assert_that(key_name).is_not_none()

        return json.dumps({
            "log_type": self.log_type,
            "path": self.get_path(key_name),
            "cols": len(self.data.dataframe.columns),
            "rows": len(self.data.dataframe),
        })



    # 실제 파일 서버로 전송
    # Run.log에 Image 객체가 기록된 경우 Image 의 값을 올리기 위한 함수
    # table내용을 json으로 변환하여 파일로 저장후 전송
    def upload_file(self, run: Run, key_name: str) -> None:
        # Table의 data인 deepdriver.dataframe으로부터 column과 data를 가져와서 json형태의 파일로 저장
        local_path = self.get_local_path(run.run_id, key_name)
        digest, size = self.file_dump(local_path)

        # 저장한 파일을 Interface.py의 upoad_file을 호출하여 전송
        root_path = self.get_root_path(run.run_id)
        path = self.get_path(key_name)
        logger.debug(f"file upload[table] : local_path=[{local_path}], root_path=[{root_path}], path=[{path}]")

        interface.upload_file(upload_type="RUN", local_path=local_path, root_path=root_path, path=path,
                              run_id=run.run_id, artifact_id=0, last_file_yn="Y", teamName=run.team_name,
                              expName=run.exp_name, run_name=run.run_name, artifact_name="", artifact_type="",
                              artifact_digest="", entry_digest=digest, entry_list=[], file_index=0)

    def file_dump(self, path: str) -> Tuple[str, str]:
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(self.to_dict(), f)

        with open(path, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
            f.seek(0, os.SEEK_END)
            size = f.tell()
        return digest, size

    def get_root_path(self, run_id: int) -> str:
        return os.path.join(str(run_id), "media")

    def get_local_dir_path(self, run_id: int) -> str:
        return os.path.join(".", "deepdriver", "run", self.get_root_path(run_id))

    def get_path(self, key_name: str) -> str:
        return f"{key_name}.TABLE.json"

    def get_local_path(self, run_id: int, key_name: str) -> str:
        return os.path.join(self.get_local_dir_path(str(run_id)), self.get_path(key_name))
