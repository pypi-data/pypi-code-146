import json
import logging
import requests
from  urllib.parse import ParseResult
from typing import Dict

from deepdriver.sdk import util
from deepdriver import logger
import deepdriver.version as version
URL_LOGIN = "/api/client/auth"
URL_CREATE = "/api/client/experiment/create"
URL_CREATE_HPO = "/api/client/experiment/create/hpo"
URL_GET_HPO = "/api/client/experiment/get/hpo"
URL_FINISH = "/api/client/run/finish"



jwt_key: str = None

def set_jwt_key(jwt_key_: str) -> None:
    global jwt_key
    jwt_key = jwt_key_

def get_jwt_key() -> str:
    global jwt_key
    return jwt_key

# 서버의 login api 를 호출하여 API key 값을 서버로 전송하고 결과로서 jwt key 를 받는다.
# 받은 jwt key 는 메모리에 저장해 두어서 추후 서버와 통신시 헤더에 실어서 보낼 수 있도록 한다.
def login(http_host: str , api_key: str) -> Dict:
    data = {
        "key": api_key
    }
    url = ParseResult(scheme="http",netloc=http_host, path=URL_LOGIN, params='', query='', fragment='').geturl()
    rsp = post(url, data)
    logger.debug("login() " + rsp["message"])
    if rsp["result"] == "success":
        set_jwt_key(rsp["token"])
    return rsp

def init(http_host: str ,exp_name: str="", team_name: str="", run_name: str="", config: Dict=None) -> Dict:
    # Interface.py의 init 함수 호출시,
    # config 값을 넘겨주어 rest api의 인자인 config의 _custom 필드에 key, value값을 각각 넣어주도록 한다
    _custom = [{"key": k, "value": v} for k, v in config.items()] if config else []

    # sysInfo값을 넘겨주어 rest api의 인자인 sysInfo필드에 넣어주도록 한다
    sys_info = {
        "os": util.get_os(),
        "python": util.get_python_version(),
        "gpu": util.get_gpu(),
        "gpuCount": util.get_gpu_count(),
        "cpuCount": util.get_cpu_count(),
        "hostname": util.get_hostname(),
    }

    # Interface.py의 init 함수 호출 후 응답받은 데이터로 부터 실험환경 이름과 팀이름, 실행이름, 실행ID, 대쉬보드URL을 가져와 Run 객체에 설정하고 반환한다.
    data = {
        "teamName": team_name,
        "expName": exp_name,
        "runName": run_name,
        "config": {"cliVer": version.__version__, "pythonVer": util.get_python_version(), "_custom": _custom},
        "sysInfo": sys_info,
        "createRun": "Y",
    }
    url = ParseResult(scheme="http",netloc=http_host, path=URL_CREATE, params='', query='', fragment='').geturl()
    rsp = post(url, data)
    logger.debug("init() response : " + rsp["message"])
    return rsp

def create_hpo(http_host:str, exp_name: str="", team_name: str="", hpo_config: Dict=None) -> Dict:

    data ={
        "teamName": team_name,
        "expName": exp_name,
        "config":  {"cliVer": version.__version__, "pythonVer": util.get_python_version(), "hpoConfig": hpo_config},
        "sysInfo": {
            "os": util.get_os(),
            "python": util.get_python_version(),
            "gpu": util.get_gpu(),
            "gpuCount": util.get_gpu_count(),
            "cpuCount": util.get_cpu_count(),
            "hostname": util.get_hostname(),
        },
    }
    url = ParseResult(scheme="http", netloc=http_host, path=URL_CREATE_HPO, params='', query='', fragment='').geturl()
    rsp = post(url, data)
    logger.debug("create_hpo() response : " + rsp["message"])
    return rsp


def get_hpo(http_host:str, exp_name: str="", team_name: str="") -> Dict:
    data = {
        "teamName": team_name,
        "expName": exp_name,
    }
    url = ParseResult(scheme="http", netloc=http_host, path=URL_GET_HPO, params='', query='', fragment='').geturl()
    rsp = post(url, data)
    logger.debug("get_hpo() response : " + rsp["message"])
    return rsp


def finish(http_host: str ,data: Dict) -> Dict:
    url = ParseResult(scheme="http",netloc=http_host, path=URL_FINISH, params='', query='', fragment='').geturl()
    rsp = post(url, data)
    logger.debug("finish() " + rsp["message"])
    return rsp

def post(url: str, data: Dict) -> Dict:
    logger.debug(f"REST[POST] to [{url}] : data=[{json.dumps(data)}], headers=[{get_headers()}")
    rsp = requests.post(url, headers=get_headers(), data=json.dumps(data))
    if rsp.status_code not in [200, 201]:
        logger.error(f"post({url}) failed({rsp.status_code})")
        raise Exception(f"request.post() failed({rsp.text if rsp.text else rsp.status_code})", rsp)
    return dict(json.loads(rsp.text))

def get_headers():
    jwt_key = get_jwt_key()
    headers = {
        "Content-Type": "application/json",
    }
    if jwt_key:
        headers["Authorization"] = f"Bearer {jwt_key}"
    return headers
