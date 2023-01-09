from typing import Dict
import warnings

from ... import Model, ModelServer
from ...utils import success_response, failed_response_with_break

try:
    import numpy as np
    from xgboost import XGBModel
    import xgboost as xgb
except ImportError as ipt_e:
    warnings.warn(
        "import numpy or xgboost were error, "
        "please manually install this pkg or use: pip install 'python-metaai[xgboost]'"
    )


class XGBoostModel(Model):
    def __init__(self, name: str, nthread: int, booster: XGBModel = None):
        super().__init__(name)
        self.name = name
        self.nthread = nthread
        if booster is not None:
            self._booster = booster
            self.ready = True

    def load(self) -> bool:

        self._booster = xgb.Booster(
            params={"nthread": self.nthread}, model_file=self.model_path
        )
        self.ready = True
        return self.ready

    def predict(self, request: Dict) -> Dict:
        try:
            dmatrix = xgb.DMatrix(np.array(request["instances"]), nthread=self.nthread)
            result: xgb.DMatrix = self._booster.predict(dmatrix)
            return success_response({"predictions": result.tolist()})
        except Exception as e:
            failed_response_with_break(message=str(e))


if __name__ == "__main__":
    model = XGBoostModel(name="custom", nthread=-1)

    ModelServer.start(model)
