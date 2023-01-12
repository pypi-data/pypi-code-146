import json
from typing import Dict

from deepdriver.sdk.artifact import Artifacts, ArtifactEntry
from deepdriver.sdk.data_types.run import get_run
from deepdriver import logger
from deepdriver import util


# dictionary 형태의 데이터, image, table, chart 등을 log 함수를 통해 서버로 전송
@util.login_required
@util.init_required
def log(data: Dict) -> bool:
    return get_run().log(data)

# image, table, dictionary 형태의 데이터를 log_artifact 를 통해 서버로 전송
@util.login_required
@util.init_required
def upload_artifact(artifact: Artifacts) -> bool:
    return get_run().upload_artifact(artifact)

@util.login_required
@util.init_required
def get_artifact(name: str, type: str, tag: str="", team_name: str="", exp_name: str="") -> Artifacts:
    if team_name =="":
        team_name =get_run().team_name

    if exp_name =="":
        exp_name =get_run().exp_name

    result, result_msg,  artifact_id, artifact_record = get_run().get_artifact(name, type, tag, team_name, exp_name)
    if result == "fail" :
        if result_msg =="not exist" :
            logger.info("artifact is created!")
            return Artifacts(name, type)
        else:
            raise ValueError(result_msg)
    logger.info("artifact is got! \n artifact id :{%d}"%(artifact_id))
    entry_list = []
    for entry in artifact_record.artifact_entry:
        entry_list.append(ArtifactEntry(entry.path, "", entry.size, entry.digest, status="ADD", lfs_yn=entry.lfsYN, repo_tag=entry.repoTag, type=entry.type, metadata=entry.metadata, key=entry.key))
    return Artifacts(artifact_record.name, artifact_record.type,
        id=artifact_id,
        desc=artifact_record.description,
        meta_data=json.loads(artifact_record.metadata),
        entry_list=entry_list,
    )

# Interface.py의 finish()함수를 호출할때 하기의 summary정보를 dictionary 형태로 넘겨준다
@util.init_required
def finish() -> bool:
    return get_run().finish()


# config 업데이트
@util.login_required
@util.init_required
def update() -> bool:
    from deepdriver import config
    return config.update()

# alert 전송
@util.login_required
@util.init_required
def alert(alert_msg:str) -> bool:
    return get_run().alert(alert_msg)