import re
from typing import Dict, Callable
from urllib.parse import urljoin

import optuna
from optuna.exceptions import DuplicatedStudyError

import deepdriver
from deepdriver import logger
from deepdriver import util
from deepdriver.sdk.config import Config
from deepdriver.sdk.data_types.experiment import set_experiment, Experiment, get_experiment
from deepdriver.sdk.data_types.run import set_run, Run, get_run
from deepdriver.sdk.interface import interface



@util.login_required
def init(exp_name: str = "", team_name: str = "", run_name: str = "", config: Dict = None) -> Run:
    """ # 실행과 실험환경을 만드는 함수 """
    # team_name 변수 vailidation
    if team_name:
        pattern = re.compile('[^a-zA-Z0-9._]+')
        if pattern.findall(exp_name):
            logger.info("init() failed : team_name은 숫자(number), 영문자(alphabet), 언더바(_), 온점(.)만 가능합니다.")
            return None

    rsp = interface.init(exp_name, team_name, run_name, config)
    run_url = urljoin(f"http://{interface.get_http_host_ip()}:9111", rsp['runUrl'])
    run = Run(rsp["teamName"], rsp["expName"], rsp["runName"], rsp["runId"], run_url)
    logger.info("DeepDriver initialized\n"
                f"Team Name={rsp['teamName']}\n"
                f"Exp Name={rsp['expName']}\n"
                f"Run Name={rsp['runName']}\n"
                f"Run URL={run_url}"
                )
    set_run(run)

    # init config
    deepdriver.config = Config()
    if config:
        for key, value in config.items():
            setattr(deepdriver.config, key, value)

    return run


@util.login_required
def create_hpo(exp_name: str = "", team_name: str = "", remote: bool = False, hpo_config: Dict = None) -> (bool, int):
    # hpo_config['parameters']를 REST API스펙에 맞게 key-value 형식으로 변환
    if hpo_config and 'parameters' in hpo_config:
        parameters_dict = hpo_config['parameters']
        key_value_parameters_list = []
        for key, value in parameters_dict.items():
            key_value_dict = {
                "key": key,
                "value": {
                    next(iter(value.keys())): next(iter(value.values()))
                }
            }
            key_value_parameters_list.append(key_value_dict)
        hpo_config['parameters'] = key_value_parameters_list

    rsp = interface.create_hpo(exp_name, team_name, hpo_config)
    logger.info("HPO initialized\n"
                f"Team Name={rsp['teamName']}\n"
                f"Exp Name={rsp['expName']}\n"
                f"Exp Url={rsp['expUrl']}"
                )
    set_experiment(Experiment(exp_name=rsp['expName'], team_name=rsp['teamName']))
    # optuna 최적화 실행
    if not remote:
        def get_optuna_sampler(hpo_config: dict) -> optuna.samplers.BaseSampler:
            type = hpo_config['method']

            if type.lower() == "random":
                return optuna.samplers.RandomSampler()
            elif type.lower() == "grid":
                search_space = {}
                for item in hpo_config['parameters']:
                    key_ = item['key']
                    value_ = list(item['value'].values())[0]
                    search_space[key_] = value_
                logger.debug(f"search_space : {search_space}")
                return optuna.samplers.GridSampler(search_space)
            elif type.lower() == "bayesian":
                return optuna.samplers.TPESampler()

        team_name_ =  team_name or  get_experiment().team_name  # team 이름이 입력되지 않은경우 run에 설정된 team 이름을 사용
        try:
            optuna.create_study(study_name=team_name_ + "_" + exp_name,
                                storage="postgresql://hpo:hpo@ce-postg.bokchi.com:5432/hpo",  # TODO : 변경예정
                                direction=hpo_config['metric']['goal'],
                                sampler=get_optuna_sampler(hpo_config),
                                )
        except DuplicatedStudyError:
            logger.info("optuna study aleady exist !")
        except Exception:
            logger.info("please check url ")

    return rsp['result'], rsp['expId']


@util.login_required
def run_hpo(exp_name: str = "", team_name: str = "", remote: bool = False, hpo_config: Dict = None,
            func: Callable = None, count: int = 10, artifact: Dict = None, job_count: int = 0) -> bool:

    result1, hpoConfig = get_hpo(exp_name=exp_name, team_name=team_name)
    result2, study = load_hpo(exp_name=exp_name, team_name=team_name)
    result3 = run_optimize(exp_name=exp_name, team_name=team_name, func=func, config=hpoConfig, count=count,
                           study=study)

    return True


@util.login_required
def get_hpo(exp_name: str = "", team_name: str = "") -> (bool, Dict):
    team_name_ = team_name or get_experiment().team_name
    rsp = interface.get_hpo(exp_name, team_name_)
    return rsp['result'], rsp['hpoConfig']


@util.login_required
def load_hpo(exp_name: str = "", team_name: str = "") -> (bool, optuna.study.study.Study):
    team_name_ =  team_name or  get_experiment().team_name
    try:
        study = optuna.load_study(study_name=team_name_ + "_" + exp_name,
                                  storage="postgresql://hpo:hpo@ce-postg.bokchi.com:5432/hpo")
    except Exception as e:
        logger.exception(e)
        return False, None
    return True, study


@util.login_required
def run_optimize(exp_name: str = "", team_name: str = "", func: Callable = None, config: Dict = {},
                 count: int = 10, study: optuna.study.study.Study = None) -> bool:
    def get_wrapped_func(exp_name, team_name, func, config):
        return lambda trial: objective(trial, exp_name, team_name, func, config)

    def objective(trial, exp_name, team_name, func, config):
        deepdriver.init(exp_name=exp_name)
        get_config(trial, config)
        y = func()
        deepdriver.log({"x": deepdriver.config.x, "y": y})
        deepdriver.finish()
        return y

    def get_config(trial, config):
        # to-do config 의 parameters 내용을 조건에  따라 하기와 같은 코드로 변환
        # {"key": "x" , "value" : {"range":[-10.0,10.0]} } 조건의 경우 하기와 같이
        deepdriver.config.x = trial.suggest_float("x", -10, 10)
        # {"key": "y" , "value" : {"range":[-10,10]} }조건의 경우 하기와 같이
        # deepdriver.config.y = trial.suggest_int("x", -10, 10)
        # {"key": "classifier" , "value" : {"values":['SVC','RandomForest']} } 조건의 경우 하기와 같이
        ##deepdriver.config.classifier= trial.suggest_categorical('classifier', ['SVC', 'RandomForest'])

    team_name_ =  team_name or  get_experiment().team_name
    try:
        study = study.optimize(get_wrapped_func(exp_name, team_name_, func, config), n_trials=count)
    except Exception as e:
        logger.exception(e)
        return False, None
    return True, study
