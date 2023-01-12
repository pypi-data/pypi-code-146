from typing import Dict

from deepdriver import logger
from deepdriver.sdk.data_types.run import Run


class Config:

    def __init__(self, init_dict: Dict = None) -> None:
        pass

    # 하이퍼 파리미터와 같은 config 값 update
    def update(self) -> None:
        from deepdriver import interface
        from deepdriver.sdk.data_types.run import get_run
        # 서버로 config() 전송
        logger.debug("config update..")
        run: Run = get_run()
        return interface.update_config(run.run_id, run.team_name, run.exp_name, self.Items())


    def __setitem__(self, idx):
        pass

    def __getitem__(self, idx, value):
        pass

    def __contains__(self, name):
        pass

    def get(self, key: str):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return None

    def Items(self):
        return list(self.__dict__.items())

    def keys(self) -> list:
        return list(self.__dict__.keys())

    def values(self) -> list:
        return list(self.__dict__.values())
