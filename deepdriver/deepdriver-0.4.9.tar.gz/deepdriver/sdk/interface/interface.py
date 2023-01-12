from __future__ import annotations
from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Tuple, TYPE_CHECKING, Union
from urllib.parse import urlsplit, urlparse

import grpc

from deepdriver import logger
from deepdriver.sdk import util
from deepdriver.sdk.interface import http_interface
from deepdriver.sdk.interface.grpc_interface_pb2 import *
from deepdriver.sdk.interface.grpc_interface_pb2_grpc import ResourceStub

if TYPE_CHECKING:
    from deepdriver.sdk.artifact import Artifact

stub: ResourceStub = None

def set_stub(stub_: ResourceStub) -> None:
    global stub
    stub = stub_


def get_stub() -> ResourceStub:
    global stub
    return stub

grpc_host : str = "127.0.0.1:19051"

def set_grpc_host(grpc_host_: str) -> None:
    global grpc_host
    grpc_host = grpc_host_

def get_grpc_host() -> str:
    global grpc_host
    return grpc_host

http_host = "127.0.0.1:9011"

def set_http_host(http_host_: str) -> None:
    global http_host
    if http_host_.upper().startswith("HTTP"):
        http_host  = urlparse(http_host_).netloc
    else:
        http_host = http_host_


def get_http_host() -> str:
    global http_host
    return http_host

def get_http_host_ip() -> str:
    global http_host
    return urlsplit('//' + http_host).hostname


def update_config(run_id: int, team_name: str, exp_name: str, config_item_dict: list):
    def makeItem(item):
        key, value = item
        if isinstance(value, int):
            if value > 2 ** 32 - 1:  # check type long
                configItem = ConfigItem(key=key, valueAsLong=value)
            else:
                configItem = ConfigItem(key=key, valueAsInt=value)
        elif isinstance(value, str):
            configItem = ConfigItem(key=key, valueAsString=value)
        elif isinstance(value, float):
            configItem = ConfigItem(key=key, valueAsFloat=value)
        elif isinstance(value, bool):
            configItem = ConfigItem(key=key, valueAsBool=value)
        elif isinstance(value, dict) or isinstance(value, list):
            configItem = ConfigItem(key=key, valueAsString=json.dumps(value))
        return configItem

    # client 정보 추가
    import deepdriver.version as version
    config_item_dict.append(('cliVer', version.__version__))
    config_item_dict.append(('pythonVer', util.get_python_version()))


    item = map(makeItem, config_item_dict)
    rsp: UpdateConfigResponse = get_stub().update_config(UpdateConfigRequest(
        runId=run_id,
        item=item,
        teamName=team_name,
        expName=exp_name,
        authorization=f"Bearer {http_interface.get_jwt_key()}",
    ))

    return rsp.rsp_result.result == "success"


def send_alert(run_id: int, team_name: str, exp_name: str, alert_msg: str):
    rsp: SendAlertResponse = get_stub().send_alert(SendAlertRequest(
        runId=run_id,
        teamName=team_name,
        expName=exp_name,
        alertMessage=alert_msg,
    ))

    return rsp.rsp_result.result == "success"

def upload_log(run_id: int, team_name: str, exp_name: str, log_step: int, item_dict: Dict[str, Union[int, str, float, bool]]) -> bool:
    item_list = []

    def makeItem(item):
        key, value = item
        if isinstance(value, int):
            if value > 2 ** 32 - 1:  # check type long
                logItem = LogItem(key=key, valueAsLong=value)
            else:
                logItem = LogItem(key=key, valueAsInt=value)
        elif isinstance(value, str):
            logItem = LogItem(key=key, valueAsString=value)
        elif isinstance(value, float):
            logItem = LogItem(key=key, valueAsFloat=value)
        elif isinstance(value, bool):
            logItem = LogItem(key=key, valueAsBool=value)
        else:
            raise Exception("value는 int, str, float, bool 타입만 가능합니다.")
        return logItem

    item = map(makeItem, item_dict.items())

    # item = [LogItem(key=key, value=str(value)) for key, value in item_dict.items()]
    rsp: UploadLogResponse = get_stub().upload_log(UploadLogRequest(
        item=item,
        step=LogStep(num=log_step),
        run=RunInfo(run_id=run_id),
        teamName=team_name,
        expName=exp_name,
        authorization=f"Bearer {http_interface.get_jwt_key()}",
    ))
    return rsp.rsp_result.result == "success"


CHUNK_SIZE = 1024 * 1024  # 1MB


def load_file(upload_type: str, local_path: str, root_path: str, path: str, run_id: int, artifact_id: int,
              last_file_yn: str, team_name: str, exp_name: str, run_name: str, artifact_name: str, artifact_type: str,
              artifact_digest: str, entry_digest: str, entry_list: List[ArtifactEntry],
              file_index: int) -> UploadFileRequest:
    if sys.platform.startswith('win32'):
        # 윈도우인 경우 Path Seperator를 리눅스 형식으로 강제로 변경함
        root_path = root_path.replace("\\", "/")
        path = path.replace("\\", "/")
    logger.debug(f"root_path: [{root_path}], path:[{path}] ")
    yield UploadFileRequest(
        uploadType=upload_type,
        file=FileRecord(file=FileItem(
            filepath=FilePath(
                path=path,
                root_path=root_path,
            )
        )),
        artifact_id=artifact_id,
        run_id=run_id,
        artifactName=artifact_name,
        artifactType=artifact_type,
        digest=entry_digest,
        last_file_yn=last_file_yn,
        authorization=f"Bearer {http_interface.get_jwt_key()}",
        teamName=team_name,
        expName=exp_name,
        runName=run_name,
        total_file_info=TotalFileInfo(
            digest=artifact_digest,
            entry=entry_list,
        ),
    )
    with open(local_path, "rb") as file:
        uploaded_size = 0
        total_size = os.stat(local_path).st_size
        while True:

            chunk_bytes = file.read(CHUNK_SIZE)
            uploaded_size += len(chunk_bytes)
            util.print_progress(uploaded_size, total_size, f'Uploading: [{local_path}]',
                                f"[{file_index + 1}/{1 if len(entry_list) == 0 else len(entry_list)}")
            if len(chunk_bytes) == 0:  # Reached EOF
                util.print_progress(total_size, total_size, f'Uploading: [{local_path}]',
                                    f"[{file_index + 1}/{1 if len(entry_list) == 0 else len(entry_list)}]")  # 100%
                return
            yield UploadFileRequest(
                file=FileRecord(file=FileItem(
                    contents=chunk_bytes
                )),
                artifact_id=artifact_id,
                run_id=run_id,
                artifactName=artifact_name,
                artifactType=artifact_type,
                digest=entry_digest,
                last_file_yn=last_file_yn,
                authorization=f"Bearer {http_interface.get_jwt_key()}",
                teamName=team_name,
                expName=exp_name,
                runName=run_name,
                total_file_info=TotalFileInfo(
                    digest=artifact_digest,
                    entry=entry_list,
                ),
            )


def upload_file(upload_type: str, local_path: str, root_path: str, path: str, run_id: int, artifact_id: int,
                last_file_yn: str, teamName: str, expName: str, run_name: str, artifact_name: str, artifact_type: str,
                artifact_digest: str, entry_digest: str, entry_list: List[ArtifactEntry], file_index: int) -> bool:
    logger.debug(
        f"upload_file() : {locals()}")

    rsp: UploadFileResponse = get_stub().upload_file(
        load_file(upload_type, local_path, root_path, path, run_id, artifact_id, last_file_yn, teamName, expName,
                  run_name, artifact_name, artifact_type, artifact_digest, entry_digest, entry_list, file_index))
    return rsp.rsp_result.result == "success"


def save_file(file_path: str, file_index: int, total_file_count: int, file_size: int, rsps) -> None:
    logger.debug(f"save_file() : file_path:[{file_path}]")

    with open(file_path, "wb") as file:
        downloaded_size = 0
        for rsp in rsps:
            chunk = bytes(rsp.contents)
            downloaded_size += len(chunk)
            util.print_progress(downloaded_size, file_size, f'Downloading: [{file_path}]',
                                f"[{file_index + 1}/{total_file_count}]")
            if len(chunk) == 0:
                raise Exception("empty chunk")
            file.write(chunk)
    util.print_progress(file_size, file_size, f'Downloading: [{file_path}]',
                        f"[{file_index + 1}/{total_file_count}]")  # 100%
    return None


def download_file(path: str, artifact_id: int, local_path: str, team_name: str, exp_name: str, artifact_name: str,
                  artifact_type: str, versioning: str, lfs_yn: str, repo_tag: str, file_index: int,
                  total_file_count: int,
                  file_size: int):
    # TODO 응답에 digest 값을 받아 추후 각 파일에 대한 정합성 체크시 활용한다.

    logger.debug(
        f"download_file() : {locals()}")

    save_file(local_path, file_index, total_file_count, file_size, get_stub().download_file(DownloadFileRequest(
        path=path,
        artifact_id=artifact_id,
        authorization=f"Bearer {http_interface.get_jwt_key()}",
        teamName=team_name,
        expName=exp_name,
        artifactName=artifact_name,
        artifactType=artifact_type,
        versioning=versioning,
        repoTag=repo_tag,
        lfsYN=lfs_yn,

    )))


def upload_artifact(run_id: int, artifact: Artifact, artifact_digest: str, teamName: str, expName: str,
                    entry_list: List[ArtifactEntry]) -> int:
    logger.debug(f"""
            upload_artifact(): ( 
                "run_id":"{run_id}",
                "type":"{artifact.type}",
                "name":"{artifact.name}",
                "digest":"{artifact_digest}",
                "description":"{artifact.desc}",
                "versioning":"{artifact.versioning}",
                "metadata":"{json.dumps(artifact.meta_data)}",
                "teamName":"{teamName}",
                "expName":"{expName}",
                "artifact_entry":"{entry_list}",
            )""")

    rsp: UploadArtifactResponse = get_stub().upload_artifact(UploadArtifactRequest(
        artifact=ArtifactRecord(
            run_id=run_id,
            type=artifact.type,
            name=artifact.name,
            digest=artifact_digest,
            description=artifact.desc,
            versioning=artifact.versioning,
            metadata=json.dumps(artifact.meta_data),
            teamName=teamName,
            expName=expName,
            artifact_entry=entry_list,
        ),
        authorization=f"Bearer {http_interface.get_jwt_key()}",
    ))
    return rsp.artifact_id if rsp.rsp_result.result == "success" else None


def use_artifact(name: str, type: str, tag: str, team_name: str, exp_name: str, run_id: int) -> Tuple[int,
                                                                                                      ArtifactRecord]:
    logger.debug(f"""
        use_artifact(): ( 
            "artifact_name":"{name}",
            "artifact_type":"{type}",
            "artifact_tag":"{tag}",
            "team_name":"{team_name}",
            "exp_name":"{exp_name}",
            "run_id":"{run_id}",
            "authorization": "Bearer {http_interface.get_jwt_key()}"
        )""")

    try:
        rsp: UseArtifactResponse = get_stub().use_artifact(UseArtifactRequest(
            artifact_name=name,
            artifact_type=type,
            artifact_tag=tag,
            team_name=team_name,
            exp_name=exp_name,
            run_id=run_id,
            authorization=f"Bearer {http_interface.get_jwt_key()}",
        ))
    except grpc.RpcError as e:
        logger.exception("Network Error")
        return "fail", "network error", -1, None
    return rsp.rsp_result.result, rsp.rsp_result.message, rsp.artifact_id, rsp.artifact


def download_artifact():
    pass


def login(key: str) -> bool:
    rsp = http_interface.login(get_http_host(), key)
    if rsp["result"] == "success":

        grpc_url = get_grpc_host()

        if grpc_url is None:
            grpc_url = rsp["grpcHost"]
        # grpc stub 생성
        channel = grpc.insecure_channel(grpc_url)
        stub = ResourceStub(channel)
        set_stub(stub)
    return rsp["result"] == "success"


def init(exp_name: str = "", team_name: str = "", run_name: str = "", config: Dict = None) -> Dict:
    return http_interface.init(get_http_host(), exp_name, team_name, run_name, config)

def create_hpo(exp_name: str = "", team_name: str = "", hpo_config: Dict = None) -> Dict:
    return http_interface.create_hpo(get_http_host(), exp_name, team_name, hpo_config)

def get_hpo(exp_name: str = "", team_name: str = "") -> Dict:
    return http_interface.get_hpo(get_http_host(), exp_name, team_name)

def finish(data: Dict) -> Dict:
    return http_interface.finish(get_http_host(), data)



