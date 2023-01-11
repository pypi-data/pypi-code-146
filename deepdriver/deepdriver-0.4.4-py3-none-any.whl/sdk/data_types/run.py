from __future__ import annotations

import time
from assertpy import assert_that
from typing import Dict, Tuple, TYPE_CHECKING
from deepdriver import logger
from deepdriver.sdk import util
from deepdriver.sdk.interface import interface
from deepdriver.sdk.interface.grpc_interface_pb2 import *
if TYPE_CHECKING:
    from deepdriver.sdk.artifact import Artifact

run: Run = None

def set_run(run_: Run) -> None:
    global run
    run = run_

def get_run() -> Run:
    global run
    return run

class Run:

    def __init__(self, team_name: str, exp_name: str, run_name: str, run_id: int=0, run_url: str="") -> None:
        assert_that(team_name).is_not_none()
        assert_that(exp_name).is_not_none()
        assert_that(run_name).is_not_none()

        self.team_name = team_name
        self.exp_name = exp_name
        self.run_name = run_name
        self.run_id = run_id
        self.run_url = run_url
        self.run_start_time = time.time()

        # 로그 스텝(Run.log로 기록 될 때마다 1씩 증가)
        self.log_step = 0

        self.lastData = {}

    # Dictionary 형태의 데이터를 기반으로 서버로 전송하는 함수
    def log(self, data: Dict) -> bool:
        assert_that(data).is_not_none()

        # item에 key값이 “timestamp” 이고 value가 현재시각 (time.time())인 item도 추가
        # item에 로그의 key value값의 쌍이 들어가도록 item을 추가ex) log({“loss” :0.03, “acc” :0.97}) -> key가 loss 이고 value가 0.03인 item과 key가 acc이고 value가 0.97인 item이 추가됨


        from deepdriver.sdk.data_types.image import Image
        from deepdriver.sdk.data_types.table import Table
        from deepdriver.sdk.chart.chart import Chart

        for key, value in data.items():
            # TODO: Image, Chart등 다른 데이터 형식도 추가해야함
            if isinstance(value, Table):
                data[key] = value.to_json(key)
                logger.debug(f"Table을 str(json)로 변환 변환 : {data[key]}")
                value.upload_file(self, key)
            elif isinstance(value, Image):
                data[key] = value.to_json(key)
                logger.debug(f"Image를 str(json)로 변환 변환 : {data[key]}")
                value.upload_file(self, key)
            elif isinstance(value, Chart):
                data[key] = value.to_json(key)
                logger.debug(f"Chart를 str(json)로 변환 변환 : {data[key]}")
                value.upload_file(self, key)


        data["timestamp"] = time.time()

        # Item의 key, value에 각각 하기의 정보를 넣는다
        data["system.cpu"] = util.get_system_cpu()
        data["system.disk"] = util.get_system_disk()
        data["system.memory"] = util.get_system_memory()
        data["system.proc.cpu.threads"] = util.get_system_proc_cpu_threads()
        data["system.proc.memory.rssMB"] = util.get_system_proc_memory_rss_mb()
        data["system.proc.memory.percent"] = util.get_system_proc_memory_percent()
        data["system.proc.memory.availableMB"] = util.get_system_memory_available_mb()

        self.log_step += 1
        succeeded = interface.upload_log(self.run_id, self.team_name, self.exp_name, self.log_step, data)

        # 마지막으로 사용된 data 를 보관
        for key, value in data.items():
            self.lastData[key] = value

        return succeeded

    # Artifact 객체를 기반으로 서버로 전송하는 함수
    def upload_artifact(self, artifact: Artifact) -> bool:
        assert_that(artifact).is_not_none()
        return artifact.upload()

    def get_artifact(self, name: str, type: str, tag: str="", team_name: str="", exp_name: str="") -> Tuple(int, ArtifactRecord):
        assert_that(name).is_not_none()
        assert_that(type).is_not_none()

        # 아티팩트의 이름과 타입을 서버로 전송하여 아티팩트 사용기록을 남기고 아티팩트 관련 정보를 받아온다
        # Tag 미지정시 서버에서 최신 버전의 아티팩트의 정보를 받아온다
        # 팀이름과 실험환경 미지정시 run에 설정된 정보로 팀과 실험환경을 판단하여 하위 아티팩트를 받아온다
        # 서버로부터 응답으로 아티팩트 ID 및 ArtifactRecord정보를 전달 받아서 Artifact 객체에 설정한다
        return interface.use_artifact(name, type, tag, team_name, exp_name, self.run_id)

    def finish(self) -> bool:
        _custom = [{"key": k, "value": v} for k, v in self.lastData.items()]
        data = {
            "runId": self.run_id,
            "summary": {
                "_runtime": time.time()-self.run_start_time,
                "_step": self.log_step,
                "_custom": _custom,
            },
        }
        resp = interface.finish(data)
        return resp["result"] == "success"


    def alert(self, alert_msg:str):
        return interface.send_alert(self.run_id, self.team_name, self.exp_name, alert_msg)



