import hashlib
import json
import os
from pathlib import Path
from typing import Dict

from assertpy import assert_that
from typing import Dict, Tuple, TYPE_CHECKING
from deepdriver import logger
from deepdriver.sdk.data_types.dataFrame import DataFrame
from deepdriver.sdk.data_types.run import Run
from deepdriver.sdk.interface import interface

TYPE_HISTOGRAM = "histogram"
TYPE_LINE = "line"
TYPE_SCATTER = "scatter"
TYPE_CONFUSION_MATRIX = "confusion_matrix"
TYPE_ROC_CURVE = "roc_curve"


class Chart:

    def __init__(self, data: DataFrame, chart_type: str, data_fields: Dict, label_fields: Dict = None) -> None:
        assert_that(data).is_not_none()
        assert_that(chart_type).is_not_none()
        assert_that(data_fields).is_not_none()

        self.data = data
        self.log_type = "chart"
        self.chart_type = chart_type
        self.data_fields = data_fields
        self.label_fields = label_fields if label_fields else {}

    @classmethod
    def from_file(cls, path: str):
        assert_that(str).is_not_none()
        with open(path) as f:
            data = json.load(f)
        df = DataFrame(columns=data['data']['columns'], data=data['data']['data'])
        return cls(chart_type=data['chart_type'], data=df, data_fields=data['data_fields'], label_fields=data['label_fields'])

    def to_dict(self):
        return {
            "data": self.data.to_dict(),
            "log_type": self.log_type,
            "chart_type": self.chart_type,
            "data_fields": self.data_fields,
            "label_fields": self.label_fields,
        }

    def to_json(self, key_name: str) -> str:
        assert_that(key_name).is_not_none()


        return json.dumps({
            "log_type": self.log_type,
            "chart_type": self.chart_type,
            "data_fields": self.data_fields,
            "label_fields": self.label_fields,
            "path": self.get_path(key_name),
        })

    def upload_file(self, run: Run, key_name: str) -> None:
        local_path = self.get_local_path(run.run_id, key_name)
        digest, size = self.file_dump(local_path)

        # 서버로 파일 전송
        root_path = self.get_root_path(run.run_id)
        path = self.get_path(key_name)
        logger.debug(f"file upload[chart] : local_path=[{local_path}], root_path=[{root_path}], path=[{path}]")

        interface.upload_file(upload_type="RUN", local_path=local_path, root_path=root_path, path=path,
                              run_id=run.run_id, artifact_id=0, last_file_yn="Y", teamName=run.team_name,
                              expName=run.exp_name, run_name=run.run_name,
                              artifact_name="", artifact_type="", artifact_digest="", entry_digest=digest,
                              entry_list=[], file_index=0)


    def file_dump(self, path: str) -> Tuple[str, str]:
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(self.to_dict(), f)

        with open(path, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
            f.seek(0, os.SEEK_END)
            size = f.tell()
        return digest, size


    def get_path(self, key_name: str) -> str:
        return f"{key_name}.CHART.json"

    def get_local_dir_path(self, run_id: int) -> str:
        return os.path.join(".", "deepdriver", "run", self.get_root_path(run_id))

    def get_root_path(self, run_id: int) -> str:
        return os.path.join(str(run_id), "chart")

    def get_local_path(self, run_id: int, key_name: str) -> str:
        return os.path.join(self.get_local_dir_path(str(run_id)), self.get_path(key_name))
