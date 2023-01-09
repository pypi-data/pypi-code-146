from typing import Dict
import warnings
from ... import Model, ModelServer
from ...utils import failed_response_with_break, success_response

try:
    import pandas as pd
    import lightgbm as lgb
    from lightgbm import Booster
except ImportError as ipt_e:
    warnings.warn(
        "import lightgbm or pandas were error, "
        "please install this pkg manually or use command: pip install 'python-metaai[lightgbm]'"
    )
    raise ipt_e

MODEL_EXTENSIONS = ".bst"


class LightGBMModel(Model):
    def __init__(self, name: str, nthread: int, booster: Booster = None):
        super().__init__(name)
        self.name = name
        self.nthread = nthread
        if booster is not None:
            self._booster = booster
            self.ready = True

    def load(self) -> bool:

        self._booster = lgb.Booster(
            params={"nthread": self.nthread}, model_file=self.model_path
        )
        self.ready = True
        return self.ready

    def predict(self, request: Dict) -> Dict:
        try:
            # dfs = []
            # for input in request["instances"]:
            #     dfs.append(pd.DataFrame(input, columns=self._booster.feature_name()))
            # inputs = pd.concat(dfs, axis=0)
            #
            # result = self._booster.predict(inputs)
            # return success_response({"predictions": result.tolist()})
            inputs = pd.DataFrame(
                request["instances"], columns=self._booster.feature_name()
            )
            result = self._booster.predict(inputs)
            return success_response({"predictions": result.tolist()})
        except Exception as e:
            failed_response_with_break(message=str(e))


if __name__ == "__main__":

    model = LightGBMModel(name="custom", nthread=-1)

    ModelServer.start(model)
